import os
import re
import io
import urllib.request
import pandas as pd
from sklearn.model_selection import train_test_split

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
OUTPUT_CSV = os.path.join(DATA_DIR, 'indian_hate_speech_corpus.csv')
SPLITS_DIR = os.path.join(DATA_DIR, 'splits')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def clean_tweet_text(raw_text):
    """
    Cleans raw Twitter artifacts:
    - Decodes unicode escape sequences (like \\xe2\\x80\\xa6)
    - Removes URLs (https://t.co/...)
    - Removes @usernames
    - Removes leading RT / retweets
    - Replaces smart quotes/dashes
    - Keeps clean Roman script / English / Hinglish letters
    """
    if not isinstance(raw_text, str):
        return ""
        
    text = raw_text
    # Handle literal escaped bytes if present (e.g. \\xe2\\x80\\xa6)
    if '\\x' in text:
        try:
            text = text.encode('latin1').decode('unicode_escape', errors='ignore')
        except Exception:
            pass
            
    # Strip URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Strip user mentions
    text = re.sub(r'@\w+', '', text)
    # Convert hashtags to plain text (#India -> India)
    text = re.sub(r'#(\w+)', r'\1', text)
    # Strip HTML entities
    text = re.sub(r'&amp;|&lt;|&gt;|&quot;|&#39;', ' ', text)
    # Normalize quotes and dashes
    text = text.replace('“', '\"').replace('”', '\"').replace('’', '\'').replace('‘', '\'')
    # Remove leading Retweet marker (RT :)
    text = re.sub(r'^(RT\s*:?\s*)+', '', text, flags=re.IGNORECASE)
    # Remove non-ASCII characters while preserving valid Roman letters and standard punctuation
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Collapse multiple whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_key(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

def fetch_and_process_hate_speech(target_per_class=1000):
    print("=" * 65)
    print("🚀 BUILDING INDIAN & HINGLISH TWITTER HATE SPEECH CORPUS")
    print("=" * 65)
    
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SPLITS_DIR, exist_ok=True)
    
    # 1. Download Hinglish Offensive Twitter (HOT) Dataset
    print("\n[1/3] Fetching Indian Hinglish Twitter dataset...")
    hot_url = "https://raw.githubusercontent.com/jim1992/capstone-Hinglish-NLP/master/HOT_dataset.csv"
    req_hot = urllib.request.Request(hot_url, headers=HEADERS)
    with urllib.request.urlopen(req_hot, timeout=15) as resp:
        df_hot = pd.read_csv(io.BytesIO(resp.read()))
        
    print(f"  ✓ Raw HOT dataset downloaded: {len(df_hot)} rows")
    
    # Clean text and overwrite 'text' column
    df_hot['clean_text'] = df_hot['text'].apply(clean_tweet_text)
    # Filter out short noise (< 15 characters)
    df_hot = df_hot[df_hot['clean_text'].str.len() >= 15].copy()
    # Deduplicate
    df_hot['norm_key'] = df_hot['clean_text'].apply(normalize_key)
    df_hot.drop_duplicates(subset=['norm_key'], keep='first', inplace=True)
    
    # Map binary label: score 0.0 -> Clean (0), score 1.0 or 2.0 -> Hate/Toxic (1)
    df_hot['label'] = df_hot['score'].apply(lambda s: 0 if float(s) == 0.0 else 1)
    df_hot['language'] = 'hinglish'
    
    hate_df = df_hot[df_hot['label'] == 1][['clean_text', 'language', 'label']].copy()
    clean_df = df_hot[df_hot['label'] == 0][['clean_text', 'language', 'label']].copy()
    
    print(f"  ✓ Cleaned HOT data: {len(hate_df)} Hate samples, {len(clean_df)} Clean samples")
    
    # 2. Supplement clean samples if needed
    clean_needed = target_per_class - len(clean_df)
    if clean_needed > 0:
        print(f"\n[2/3] Fetching {clean_needed} supplementary verified clean tweets from HASOC benchmark...")
        hasoc_url = "https://raw.githubusercontent.com/roushan-raj/HASOC-2020/master/Dataset/Train%20Data/hasoc_2020_en_train.xlsx"
        req_hasoc = urllib.request.Request(hasoc_url, headers=HEADERS)
        with urllib.request.urlopen(req_hasoc, timeout=15) as resp:
            df_hasoc = pd.read_excel(io.BytesIO(resp.read()))
            
        df_hasoc_clean = df_hasoc[df_hasoc['task1'] == 'NOT'].copy()
        df_hasoc_clean['clean_text'] = df_hasoc_clean['text'].apply(clean_tweet_text)
        df_hasoc_clean = df_hasoc_clean[df_hasoc_clean['clean_text'].str.len() >= 15].copy()
        df_hasoc_clean['norm_key'] = df_hasoc_clean['clean_text'].apply(normalize_key)
        df_hasoc_clean.drop_duplicates(subset=['norm_key'], keep='first', inplace=True)
        df_hasoc_clean['label'] = 0
        df_hasoc_clean['language'] = 'en-IN'
        
        supp_clean = df_hasoc_clean.head(clean_needed)[['clean_text', 'language', 'label']]
        final_clean = pd.concat([clean_df, supp_clean], ignore_index=True)
    else:
        final_clean = clean_df.head(target_per_class)
        
    final_hate = hate_df.head(target_per_class)
    final_clean = final_clean.head(target_per_class)
    
    # 3. Assemble Golden Master Dataset
    print("\n[3/3] Assembling golden balanced corpus...")
    master_df = pd.concat([final_hate, final_clean], ignore_index=True)
    
    # Rename clean_text to text
    master_df = master_df.rename(columns={'clean_text': 'text'})
    
    # Deterministic shuffle
    master_df = master_df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    master_df.insert(0, 'id', range(1, len(master_df) + 1))
    
    # Ensure exact columns: id, text, language, label
    master_df = master_df[['id', 'text', 'language', 'label']]
    
    # Save master CSV
    master_df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    
    # 4. Generate Stratified Splits (80% Train, 10% Val, 10% Test)
    train_val_df, test_df = train_test_split(
        master_df,
        test_size=0.10,
        stratify=master_df['label'],
        random_state=42
    )
    train_df, val_df = train_test_split(
        train_val_df,
        test_size=0.10 / 0.90,
        stratify=train_val_df['label'],
        random_state=42
    )
    
    train_df.to_csv(os.path.join(SPLITS_DIR, 'hate_train.csv'), index=False)
    val_df.to_csv(os.path.join(SPLITS_DIR, 'hate_val.csv'), index=False)
    test_df.to_csv(os.path.join(SPLITS_DIR, 'hate_test.csv'), index=False)
    
    print("\n" + "=" * 65)
    print(f"🎉 CORPUS & SPLITS GENERATED: {len(master_df)} TOTAL ROWS")
    print("=" * 65)
    print("Class Balance:")
    print(master_df['label'].value_counts().rename(index={1: 'Hate/Offensive (1)', 0: 'Clean/Non-Hate (0)'}))
    print("\nLanguage Breakdown:")
    print(master_df['language'].value_counts())
    print(f"\nNull Check: {master_df.isnull().sum().to_dict()}")
    print("\nSplits Generated in data/splits/:")
    print(f"  • hate_train.csv: {len(train_df)} rows (80%)")
    print(f"  • hate_val.csv:   {len(val_df)} rows (10%)")
    print(f"  • hate_test.csv:  {len(test_df)} rows (10%)")
    print("=" * 65)
    print(f"📁 Master file: {OUTPUT_CSV}")

if __name__ == '__main__':
    fetch_and_process_hate_speech(target_per_class=1000)
