"""
Machine Learning Training & Benchmark Pipeline
==============================================
Tasks:
  1. Fake News Detection (10,000 balanced rows)
  2. Hate Speech & Hostility Detection (10,000 balanced rows)

Models Implemented:
  - Multinomial Naive Bayes
  - Logistic Regression
  - Linear SVM (Calibrated for probability confidence scores)
  - Random Forest Classifier

Features:
  - N-Gram TF-IDF Vectorization (Unigrams + Bigrams)
  - Rigorous Evaluation on Test Set (Accuracy, Precision, Recall, F1, Confusion Matrix)
  - Automated Export of Trained Weights (.joblib) to models/
  - Generation of Structured Benchmark Comparison JSON
"""

import os
import json
import time
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SPLITS_DIR = os.path.join(DATA_DIR, 'splits')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

def prepare_text_series(df):
    """Combines headline and article_text into a single input feature."""
    headline = df['headline'].fillna('').astype(str)
    article = df['article_text'].fillna('').astype(str)
    # Combine headline and body with space
    combined = (headline + " " + article).str.strip()
    return combined

def train_and_evaluate_task(task_name, train_file, test_file, label_names):
    print("\n" + "=" * 75)
    print(f" TRAINING ML MODELS FOR TASK: {task_name.upper()}")
    print("=" * 75)
    
    # 1. Load Data
    print(f"Loading data from {SPLITS_DIR}...")
    train_df = pd.read_csv(train_file)
    test_df = pd.read_csv(test_file)
    
    print(f"  • Train set: {len(train_df):,} samples | Class distribution: {dict(train_df['label'].value_counts())}")
    print(f"  • Test set:  {len(test_df):,} samples  | Class distribution: {dict(test_df['label'].value_counts())}")
    
    X_train_raw = prepare_text_series(train_df)
    y_train = train_df['label'].values
    
    X_test_raw = prepare_text_series(test_df)
    y_test = test_df['label'].values
    
    # 2. Fit TF-IDF Vectorizer
    print("\n[Step 1] Fitting N-Gram TF-IDF Vectorizer (unigrams + bigrams, max 10,000 features)...")
    vectorizer = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        stop_words='english'
    )
    
    t0 = time.time()
    X_train_vec = vectorizer.fit_transform(X_train_raw)
    X_test_vec = vectorizer.transform(X_test_raw)
    vec_time = time.time() - t0
    print(f"  ✓ Vectorization complete in {vec_time:.2f}s. Vocabulary size: {len(vectorizer.vocabulary_):,}")
    
    # Save vectorizer
    vec_path = os.path.join(MODELS_DIR, f"{task_name}_tfidf_vectorizer.joblib")
    joblib.dump(vectorizer, vec_path)
    print(f"  ✓ Saved vectorizer to: {vec_path}")
    
    # 3. Define Models to Train
    # CalibratedClassifierCV wraps LinearSVC with Platt scaling so it provides predict_proba for the web UI
    models = {
        "Naive Bayes": MultinomialNB(alpha=0.1),
        "Logistic Regression": LogisticRegression(C=1.0, max_iter=1000, random_state=42),
        "Linear SVM": CalibratedClassifierCV(LinearSVC(C=1.0, random_state=42)),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    }
    
    task_results = {}
    best_model_name = None
    best_f1 = -1.0
    
    # 4. Train & Evaluate Each Model
    for name, clf in models.items():
        print(f"\n--- Training {name} ---")
        t_start = time.time()
        clf.fit(X_train_vec, y_train)
        train_time = time.time() - t_start
        
        # Test predictions
        t_pred = time.time()
        y_pred = clf.predict(X_test_vec)
        eval_time = time.time() - t_pred
        
        # Calculate Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='binary')
        rec = recall_score(y_test, y_pred, average='binary')
        f1 = f1_score(y_test, y_pred, average='binary')
        cm = confusion_matrix(y_test, y_pred).tolist()
        
        print(f"  ✓ Training Time: {train_time:.2f}s | Inference Time (1,000 samples): {eval_time*1000:.1f}ms")
        print(f"  ✓ Accuracy:  {acc * 100:.2f}%")
        print(f"  ✓ Precision: {prec * 100:.2f}%")
        print(f"  ✓ Recall:    {rec * 100:.2f}%")
        print(f"  ✓ F1-Score:  {f1 * 100:.2f}%")
        print(f"  Confusion Matrix (TN, FP / FN, TP):\n    {cm[0]}\n    {cm[1]}")
        
        # Save individual model
        slug = name.lower().replace(" ", "_")
        model_save_path = os.path.join(MODELS_DIR, f"{task_name}_{slug}.joblib")
        joblib.dump(clf, model_save_path)
        
        task_results[name] = {
            "accuracy": round(acc * 100, 2),
            "precision": round(prec * 100, 2),
            "recall": round(rec * 100, 2),
            "f1_score": round(f1 * 100, 2),
            "confusion_matrix": cm,
            "train_time_sec": round(train_time, 3),
            "model_path": model_save_path
        }
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            
    # Mark and save overall best model as default for serving
    best_slug = best_model_name.lower().replace(" ", "_")
    best_src = os.path.join(MODELS_DIR, f"{task_name}_{best_slug}.joblib")
    best_dst = os.path.join(MODELS_DIR, f"{task_name}_best_model.joblib")
    best_clf = joblib.load(best_src)
    joblib.dump(best_clf, best_dst)
    
    print(f"\n ⭐ BEST MODEL FOR {task_name.upper()}: {best_model_name} (F1: {best_f1 * 100:.2f}%)")
    print(f"    Saved as production default: {best_dst}")
    
    return task_results

def run_ml_benchmark():
    overall_benchmark = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "tasks": {}
    }
    
    # Task 1: Fake News Detection
    fake_news_train = os.path.join(SPLITS_DIR, 'train.csv')
    fake_news_test = os.path.join(SPLITS_DIR, 'test.csv')
    if os.path.exists(fake_news_train) and os.path.exists(fake_news_test):
        res_fn = train_and_evaluate_task(
            task_name="fake_news",
            train_file=fake_news_train,
            test_file=fake_news_test,
            label_names=["Real News", "Fake News"]
        )
        overall_benchmark["tasks"]["fake_news"] = res_fn
    else:
        print(f"Fake news split files not found in {SPLITS_DIR}!")

    # Task 2: Hate Speech Detection
    hate_train = os.path.join(SPLITS_DIR, 'hate_train.csv')
    hate_test = os.path.join(SPLITS_DIR, 'hate_test.csv')
    if os.path.exists(hate_train) and os.path.exists(hate_test):
        res_hate = train_and_evaluate_task(
            task_name="hate_speech",
            train_file=hate_train,
            test_file=hate_test,
            label_names=["Safe", "Hostile"]
        )
        overall_benchmark["tasks"]["hate_speech"] = res_hate
    else:
        print(f"Hate speech split files not found in {SPLITS_DIR}!")
        
    # Save Benchmark Metrics JSON
    benchmark_json_path = os.path.join(MODELS_DIR, 'ml_benchmark_results.json')
    with open(benchmark_json_path, 'w', encoding='utf-8') as f:
        json.dump(overall_benchmark, f, indent=2)
        
    print("\n" + "=" * 75)
    print(f" ALL ML MODELS TRAINED & BENCHMARKED SUCCESSFULLY!")
    print(f" Benchmark results saved to: {benchmark_json_path}")
    print(f" Model weights saved in:      {MODELS_DIR}/")
    print("=" * 75)

if __name__ == '__main__':
    run_ml_benchmark()
