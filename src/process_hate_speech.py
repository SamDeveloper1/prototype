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

# Strict prefix regex: catches any base word or inflected/plural form (e.g. fucked, shitty, assholes, etc.)
ZERO_CURSE_REGEX = re.compile(
    r'\b(fuck\w*|shit\w*|bitch\w*|cunt\w*|dick\w*|pussy\w*|whore\w*|slut\w*|cock\w*|'
    r'ass\w*|dumbass\w*|bastard\w*|rap\w*|tits?|boobs?|penis|vagina|nigg\w*|kill yourself)\b|'
    r'(madarch\w*|bhench\w*|behench\w*|bhosd\w*|bsdk|choot\w*|chut\w*|lund\w*|lauda\w*|loda\w*|gaand\w*|\bgand\b|'
    r'randi\w*|ghasti\w*|phudi\w*|tawaif\w*|chinaal\w*|jhantu\w*|tatte\w*|katve\w*|kutiya\w*|\bkutta\w*|harami\w*|chutiya\w*)',
    re.IGNORECASE
)

def clean_social_text(raw_text):
    if not isinstance(raw_text, str):
        return ""
    text = raw_text
    if '\\x' in text:
        try:
            text = text.encode('latin1').decode('unicode_escape', errors='ignore')
        except Exception:
            pass
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#(\w+)', r'\1', text)
    text = re.sub(r'&amp;|&lt;|&gt;|&quot;|&#39;', ' ', text)
    text = text.replace('“', '\"').replace('”', '\"').replace('’', '\'').replace('‘', '\'')
    text = re.sub(r'^(RT\s*:?\s*)+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def is_academic_safe(text):
    """Ensures text is clean, at least 25 chars, and contains ZERO vulgar/profane words."""
    if not text or len(text) < 25:
        return False
    if ZERO_CURSE_REGEX.search(text):
        return False
    return True

def build_academic_safe_hate_speech_corpus(target_per_class=500):
    print("=" * 70)
    print("🛡️ BUILDING 100% ZERO-CURSE ACADEMIC HATE SPEECH CORPUS")
    print("=" * 70)
    
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SPLITS_DIR, exist_ok=True)
    
    # 1. Fetch HASOC Official English Benchmark (Train + Test)
    print("\n[1/3] Downloading official HASOC benchmark...")
    url_hasoc_train = "https://raw.githubusercontent.com/roushan-raj/HASOC-2020/master/Dataset/Train%20Data/hasoc_2020_en_train.xlsx"
    url_hasoc_test = "https://raw.githubusercontent.com/roushan-raj/HASOC-2020/master/Dataset/Test%20Data/english_test_1509.csv"
    
    req_tr = urllib.request.Request(url_hasoc_train, headers=HEADERS)
    req_te = urllib.request.Request(url_hasoc_test, headers=HEADERS)
    
    with urllib.request.urlopen(req_tr, timeout=15) as r1, urllib.request.urlopen(req_te, timeout=15) as r2:
        df_tr = pd.read_excel(io.BytesIO(r1.read()))
        df_te = pd.read_csv(io.BytesIO(r2.read()))
        df_hasoc = pd.concat([df_tr, df_te], ignore_index=True)
        
    df_hasoc['clean_text'] = df_hasoc['text'].apply(clean_social_text)
    df_hasoc = df_hasoc[df_hasoc['clean_text'].apply(is_academic_safe)].copy()
    df_hasoc.drop_duplicates(subset=['clean_text'], inplace=True)
    
    hasoc_hate = df_hasoc[df_hasoc['task1'] == 'HOF']['clean_text'].tolist()
    hasoc_clean = df_hasoc[df_hasoc['task1'] == 'NOT']['clean_text'].tolist()
    print(f"  ✓ Sanitized HASOC: {len(hasoc_hate)} Hostile, {len(hasoc_clean)} Safe Clean")
    
    # 2. Fetch Ethos Academic Toxicity Benchmark
    print("\n[2/3] Downloading Ethos academic benchmark...")
    url_ethos = "https://raw.githubusercontent.com/intelligence-csd-auth-gr/Ethos-Hate-Speech-Dataset/master/ethos/ethos_data/Ethos_Dataset_Binary.csv"
    req_e = urllib.request.Request(url_ethos, headers=HEADERS)
    with urllib.request.urlopen(req_e, timeout=15) as r:
        df_ethos = pd.read_csv(io.BytesIO(r.read()), sep=';')
        
    df_ethos['clean_text'] = df_ethos['comment'].apply(clean_social_text)
    df_ethos = df_ethos[df_ethos['clean_text'].apply(is_academic_safe)].copy()
    df_ethos.drop_duplicates(subset=['clean_text'], inplace=True)
    
    ethos_hate = df_ethos[df_ethos['isHate'] >= 0.5]['clean_text'].tolist()
    ethos_clean = df_ethos[df_ethos['isHate'] < 0.5]['clean_text'].tolist()
    print(f"  ✓ Sanitized Ethos: {len(ethos_hate)} Hostile, {len(ethos_clean)} Safe Clean")
    
    # 3. Assemble and Balance Dataset
    print("\n[3/3] Balancing to exact 500 Hate / 500 Clean (1,000 total rows)...")
    final_hate_texts = (hasoc_hate + ethos_hate)[:target_per_class]
    final_clean_texts = (hasoc_clean + ethos_clean)[:target_per_class]
    
    hate_records = [{'text': t, 'category': 'Hostile / Cyberbullying', 'label': 1} for t in final_hate_texts]
    clean_records = [{'text': t, 'category': 'Safe / Constructive', 'label': 0} for t in final_clean_texts]
    
    master_df = pd.DataFrame(hate_records + clean_records)
    # Shuffle deterministically
    master_df = master_df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    master_df.insert(0, 'id', range(1, len(master_df) + 1))
    
    # Save Master Corpus
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
    
    print("\n" + "=" * 70)
    print(f"🎉 100% ZERO-CURSE CORPUS READY: {len(master_df)} TOTAL ROWS")
    print("=" * 70)
    print("Class Balance:")
    print(master_df['label'].value_counts().rename(index={1: 'Hostile / Cyberbullying (1)', 0: 'Safe / Constructive (0)'}))
    print(f"\nNull Check: {master_df.isnull().sum().to_dict()}")
    print("\nSplits Generated in data/splits/:")
    print(f"  • hate_train.csv: {len(train_df)} rows (80%)")
    print(f"  • hate_val.csv:   {len(val_df)} rows (10%)")
    print(f"  • hate_test.csv:  {len(test_df)} rows (10%)")
    print("=" * 70)
    print(f"📁 Master file: {OUTPUT_CSV}")

if __name__ == '__main__':
    build_academic_safe_hate_speech_corpus(target_per_class=500)
