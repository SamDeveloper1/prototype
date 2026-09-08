# Session Summary & Resumption Guide

**Last Updated**: September 8, 2026  
**Active Conversation ID**: `472dd7ce-d976-48d4-8177-d76b09e609fd`  
**Previous Session Reference**: `a8bff3dc-b714-46c2-b27c-bde318b85390`  

---

## 🔗 How to Resume This Conversation Anytime

### Method 1: Terminal Command
Run this command in your terminal to jump straight back into this session with all history preserved:
```bash
agy --conversation=472dd7ce-d976-48d4-8177-d76b09e609fd
```
Or resume your latest session:
```bash
agy -c
```

### Method 2: Direct UI Link
👉 **[Click Here to Resume Conversation (472dd7ce-d976-48d4-8177-d76b09e609fd)](conversation://472dd7ce-d976-48d4-8177-d76b09e609fd)**

---

---

## 📋 Comprehensive Status of What Has Been Built

### 1. Project Architecture (`sec_prototype/`)
* **Git Repository**: Initialized on branch `main` with clean commit history.
* **Legacy Prototype (`fake_news/`)**: Completely preserved and untouched.
* **Production Standards**: Clean `.gitignore` (ignoring `.zip`, `.pt`, `venv/`, `.DS_Store`), pinned `requirements.txt`, `.env.example`, and team `README.md`.

---

### 2. Dataset 1: Indian Fake News Corpus (Scaling to 10,000 Rows)
* **Target Size**: **10,000 rows** (5,000 Real, 5,000 Fake — 50/50 balance).
* **Parameters**: `headline`, `article_text`, `label` (0: Real, 1: Fake).
* **Time Horizon & Scope**: Last 5 years (2019–2024/2026), 100% Indian-centric English.
* **Confirmed Fake News Sources (5,000 rows)**:
  1. IIIT-Delhi Verified Dataset (from Kaggle benchmark)
  2. Alt News (`altnews.in`) — Automated Python scraper
  3. BOOM Live (`boomlive.in`) — Automated Python scraper
  4. Factly (`factly.in`) — Automated Python scraper
  5. Newschecker (`newschecker.in`) — Automated Python scraper
  6. Quint WebQoof (`thequint.com/news/webqoof`) — Automated Python scraper
* **Confirmed Real News Sources (5,000 rows)**:
  1. Press Information Bureau (PIB) (`pib.gov.in`) — Official GoI releases
  2. The Hindu (`thehindu.com`)
  3. NDTV (`ndtv.com`)
  4. The Indian Express (`indianexpress.com`)
  5. Business Standard (`business-standard.com`)

---

### 3. Dataset 2: Academic-Safe Hate Speech & Hostility Corpus (10,000 Rows Completed)
* **File**: [`sec_prototype/data/indian_hate_speech_corpus.csv`](file:///Users/samarth/Desktop/Final%20Year%20stuff/Final_year_project/sec_prototype/data/indian_hate_speech_corpus.csv)
* **Total Records**: **Exactly 10,000 Rows**
* **Class Balance**: **5,000 Safe (`0`)** & **5,000 Hostile / Targeted Hate (`1`)** (50% / 50%).
* **Multi-Source Balanced Distribution**:
  - `iit_kgp_hatexplain`: 4,446 rows (IIT Kharagpur AAAI-2021 multi-annotator benchmark)
  - `cyberbullying_tweets`: 3,900 rows (Targeted hostility benchmark)
  - `curated_academic`: 999 rows (Sanitized baseline)
  - `ethos_benchmark`: 655 rows (Ethos academic benchmark)
* **Target Community Annotations**:
  - `religion`: 1,546 rows
  - `gender`: 1,130 rows
  - `ethnicity`: 899 rows
  - `age`: 496 rows
  - `general` / `Hostile`: 1,610 rows
  - `none` (Safe comments): 4,319 rows
* **Sanitization (100% College / Examiner Safe)**:
  - Strict zero-curse filter purged all crude street vulgarity, sexual slurs, and abusive profanity.
* **Stratified Splits in `sec_prototype/data/splits/`**:
  - `hate_train.csv`: 8,000 rows (80%)
  - `hate_val.csv`: 1,000 rows (10%)
  - `hate_test.csv`: 1,000 rows (10%)

---

---

## 4. Machine Learning Models Trained & Benchmarked (Completed)

* **Script**: [`sec_prototype/src/train_ml_models.py`](file:///Users/samarth/Desktop/Final%20Year%20stuff/Final_year_project/sec_prototype/src/train_ml_models.py)
* **Jupyter Notebook**: [`sec_prototype/notebooks/train_ml_models.ipynb`](file:///Users/samarth/Desktop/Final%20Year%20stuff/Final_year_project/sec_prototype/notebooks/train_ml_models.ipynb)
* **Models Trained**: Naive Bayes, Logistic Regression, Linear SVM (Calibrated), Random Forest.
* **Feature Extraction**: N-Gram TF-IDF Vectorizer (Unigrams + Bigrams, 10,000 features).
* **Saved Weights**: Saved to [`sec_prototype/models/`](file:///Users/samarth/Desktop/Final%20Year%20stuff/Final_year_project/sec_prototype/models/) (13 files including `.joblib` and `ml_benchmark_results.json`).

### Task 1: Fake News Detection Benchmark (1,000 Test Samples)
| Model | Accuracy | Precision | Recall | F1-Score | Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Linear SVM** | **92.90%** | **91.65%** | **94.40%** | **93.00%** | ⭐ **Best Model (Saved as default)** |
| Logistic Regression | 92.60% | 90.04% | 95.80% | 92.83% | Production Ready |
| Random Forest | 92.50% | 90.94% | 94.40% | 92.64% | Robust Ensemble |
| Multinomial Naive Bayes | 88.80% | 86.88% | 91.40% | 89.08% | Fast Baseline |

### Task 2: Hate Speech Detection Benchmark (1,000 Test Samples)
| Model | Accuracy | Precision | Recall | F1-Score | Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Naive Bayes** | **70.40%** | **67.59%** | **78.40%** | **72.59%** | ⭐ **Best ML Baseline** |
| Linear SVM | 72.00% | 71.40% | 73.40% | 72.39% | Solid Linear Boundary |
| Logistic Regression | 71.60% | 71.77% | 71.20% | 71.49% | Calibrated Probabilities |
| Random Forest | 73.70% | 79.26% | 64.20% | 70.94% | High Precision |

---

---

## 5. FastAPI Backend & Modular Controllers (Completed)

* **Entry Point**: [`sec_prototype/main.py`](file:///Users/samarth/Desktop/Final%20Year%20stuff/Final_year_project/sec_prototype/main.py)
* **Controllers Directory**: [`sec_prototype/controllers/`](file:///Users/samarth/Desktop/Final%20Year%20stuff/Final_year_project/sec_prototype/controllers/)
  * `fake_news_controller.py`: Input validation (text vs URL), web scraping, TF-IDF inference, returns verdict + confidence.
  * `hate_speech_controller.py`: Input validation, text sanitization, inference, returns verdict + confidence.
  * `scraper_utils.py`: URL parsing, OpenGraph title extraction, DOM paragraph parsing.
* **Routes Implemented**:
  * `POST /predict_fakenews`: Handles text and article URLs.
  * `POST /predict_hatespeech`: Handles text input for hate speech.
  * `POST /predict_hatespeech_media`: Handles audio (`.mp3`, `.wav`, etc.) and video (`.mp4`, `.mov`, etc.) via Whisper `base` + `ffmpeg`.
  * `GET /health` & `GET /docs` (Interactive Swagger documentation)
* **Test Verification**:
  * Fake News Claim: 98.5% confidence (`Fake News`)
  * Real News Sample: 81.0% confidence (`Real News`)
  * Hostile Text: 74.8% confidence (`Hate Speech / Hostile`)
  * Safe Text: 55.6% confidence (`Safe / Non-Hate`)
  * Empty payload validation: Returns clean `422 Unprocessable Entity`
  * Media Endpoint: Successfully tested with audio and video inputs.

---

## 6. Multimodal Audio & Video Transcription (Completed)

* **Module**: [`sec_prototype/controllers/media_utils.py`](file:///Users/samarth/Desktop/Final%20Year%20stuff/Final_year_project/sec_prototype/controllers/media_utils.py)
* **Features**:
  * OpenAI Whisper (`base` model, ~74M parameters) cached in memory on startup.
  * Native `ffmpeg` integration for audio extraction (converts video tracks to 16kHz mono audio).
  * Supports Audio (`.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`) and Video (`.mp4`, `.mov`, `.mkv`, `.webm`).
  * Automatic temporary file cleanup after transcription and inference.

---

## 7. Deep Learning Transformer Pipeline for RTX 3050 (4GB VRAM) (Completed)

* **Guide**: [`sec_prototype/DL_COLLABORATION_GUIDE.md`](file:///Users/samarth/Desktop/Final%20Year%20stuff/Final_year_project/sec_prototype/DL_COLLABORATION_GUIDE.md)
* **Training Script**: [`sec_prototype/src/train_dl_models.py`](file:///Users/samarth/Desktop/Final%20Year%20stuff/Final_year_project/sec_prototype/src/train_dl_models.py)
* **Jupyter Notebook**: [`sec_prototype/notebooks/train_deep_learning_gpu.ipynb`](file:///Users/samarth/Desktop/Final%20Year%20stuff/Final_year_project/sec_prototype/notebooks/train_deep_learning_gpu.ipynb)
* **GPU Requirements**: [`sec_prototype/requirements-gpu.txt`](file:///Users/samarth/Desktop/Final%20Year%20stuff/Final_year_project/sec_prototype/requirements-gpu.txt)
* **Optimized Settings for 4GB VRAM**:
  * FP16 Mixed Precision (`fp16=True`)
  * Batch Size = 8, Gradient Accumulation = 2 (effective batch size 16)
  * Max Sequence Length = 256 tokens (prevents OOM)
  * Evaluation on unseen test split with confusion matrix plot and JSON metrics export.

---

## 🎯 Immediate Next Steps When You Resume

1. **Push to Remote Git**:
   - Run `git push origin main` in terminal so teammate can clone from `https://github.com/SamDeveloper1/prototype.git`.
2. **Support Teammate on Step 13 (Next.js Frontend)**:
   - Provide exact request/response schemas for `/predict_fakenews`, `/predict_hatespeech`, and `/predict_hatespeech_media`.
3. **Step 16 — Automated Test Suite (`tests/test_api.py`)**:
   - Add unit tests with pytest & FastAPI TestClient.



