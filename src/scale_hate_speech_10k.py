"""
Scale Hate Speech & Hostility Corpus to 10,000 Rows (5,000 Safe, 5,000 Hostile)
=============================================================================
Sources:
  1. IIT Kharagpur HateXplain Benchmark (AAAI 2021) - 3-Annotator Majority Voting
  2. Cyberbullying & Targeted Hostility Benchmark (2021) - Religion, Ethnicity, Gender, Age
  3. Ethos Academic Hate Speech Benchmark (2020) - Zero vulgarity, identity-based
  4. Curated Academic Baseline (HASOC/Ethos verified samples)

Features:
  - id: Unique integer
  - headline: Context / short summary / first sentence
  - article_text: Full comment / tweet / speech text
  - target_community: religion, gender, ethnicity, age, none
  - source_domain: Source provenance
  - label: 0 (Safe / Constructive), 1 (Hate Speech / Hostile)
"""

import os
import re
import json
import warnings
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SPLITS_DIR = os.path.join(DATA_DIR, 'splits')
OUTPUT_CSV = os.path.join(DATA_DIR, 'indian_hate_speech_corpus.csv')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

NON_LATIN_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u0900-\u0D7F]')

# Academic safety filter: Purge crude sexual street slurs and extreme profanity to protect college presentations
VULGAR_WORDS = [
    'fuck', 'fucking', 'fucker', 'motherfucker', 'bitch', 'whore', 'slut',
    'cunt', 'pussy', 'dick', 'cock', 'asshole', 'bastard', 'chutiya',
    'bhosdike', 'madarchod', 'behenchod', 'gaand', 'randi', 'harami'
]
VULGAR_REGEX = re.compile(r'\b(' + '|'.join(VULGAR_WORDS) + r')\b', re.IGNORECASE)

def clean_text(text):
    if not text or pd.isna(text):
        return ""
    # Remove HTML
    clean = BeautifulSoup(str(text), 'html.parser').get_text(separator=' ', strip=True)
    # Remove usernames, URLs, and excessive spaces
    clean = re.sub(r'http\S+|www\S+', '', clean)
    clean = re.sub(r'@\w+', '', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def is_academic_safe(text):
    """Ensures text has no non-Latin script and no crude street profanity."""
    if not text or len(text) < 15:
        return False
    if NON_LATIN_PATTERN.search(text):
        return False
    if VULGAR_REGEX.search(text):
        return False
    return True

def normalize_key(text):
    """Generates unique alphanumeric fingerprint for strict deduplication."""
    return re.sub(r'[^a-z0-9]', '', str(text).lower()[:100])

# =====================================================================
# 1. IIT KHARAGPUR HATEXPLAIN BENCHMARK (AAAI 2021)
# =====================================================================
def fetch_iit_kgp_hatexplain():
    records_hostile = []
    records_safe = []
    print("\n[Source 1] Fetching IIT Kharagpur HateXplain Benchmark (AAAI 2021)...")
    url = 'https://raw.githubusercontent.com/punyajoy/HateXplain/master/Data/dataset.json'
    
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        data = json.loads(r.text)
        print(f"  Downloaded {len(data):,} raw posts. Processing 3-annotator majority votes...")
        
        seen_keys = set()
        for post_id, info in data.items():
            tokens = info.get('post_tokens', [])
            text = clean_text(" ".join(tokens))
            
            if not is_academic_safe(text):
                continue
                
            key = normalize_key(text)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            
            # Majority voting resolution across 3 annotators
            labels = [a.get('label', '').lower() for a in info.get('annotators', [])]
            hate_votes = sum(1 for l in labels if l in ['hatespeech', 'hate speech', 'offensive'])
            safe_votes = sum(1 for l in labels if l == 'normal')
            
            if hate_votes >= 2:
                final_label = 1
            elif safe_votes >= 2:
                final_label = 0
            else:
                # Discard ambiguous 1-1-1 ties
                continue
                
            # Extract target community
            all_targets = []
            for a in info.get('annotators', []):
                for t in a.get('target', []):
                    if t and t.lower() != 'none':
                        all_targets.append(t.lower())
                        
            target_comm = 'general'
            if all_targets:
                joined_targets = " ".join(all_targets)
                if any(w in joined_targets for w in ['muslim', 'hindu', 'jew', 'christian', 'islam', 'religion']):
                    target_comm = 'religion'
                elif any(w in joined_targets for w in ['women', 'woman', 'men', 'gender', 'homosexual', 'trans']):
                    target_comm = 'gender'
                elif any(w in joined_targets for w in ['african', 'arab', 'asian', 'black', 'white', 'immigrant', 'caste', 'race']):
                    target_comm = 'ethnicity'
            elif final_label == 0:
                target_comm = 'none'

            headline = text.split('. ')[0] if len(text.split('. ')[0]) > 15 else text[:80]
            
            rec = {
                'headline': headline[:150],
                'article_text': text,
                'target_community': target_comm,
                'source_domain': 'iit_kgp_hatexplain',
                'label': final_label
            }
            
            if final_label == 1:
                records_hostile.append(rec)
            else:
                records_safe.append(rec)
                
        print(f"  ✓ IIT-Kharagpur HateXplain: {len(records_hostile):,} Hostile, {len(records_safe):,} Safe extracted.")
    except Exception as e:
        print(f"  ✗ Error fetching HateXplain: {e}")
        
    return records_hostile, records_safe

# =====================================================================
# 2. CYBERBULLYING & TARGETED HOSTILITY BENCHMARK (2021)
# =====================================================================
def fetch_cyberbullying_benchmark():
    records_hostile = []
    records_safe = []
    print("\n[Source 2] Fetching Cyberbullying & Targeted Hostility Benchmark (2021)...")
    url = 'https://raw.githubusercontent.com/jayantverma2809/Cyberbullying-Tweet-Recognition-App/main/cyberbullying_tweets.csv'
    
    try:
        df = pd.read_csv(url, on_bad_lines='skip')
        print(f"  Loaded {len(df):,} records. Filtering and normalizing...")
        
        seen_keys = set()
        for _, row in df.iterrows():
            text = clean_text(row.get('tweet_text', ''))
            cb_type = str(row.get('cyberbullying_type', '')).strip().lower()
            
            if not is_academic_safe(text):
                continue
                
            key = normalize_key(text)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            
            if cb_type == 'not_cyberbullying':
                final_label = 0
                target_comm = 'none'
            else:
                final_label = 1
                target_comm = cb_type if cb_type in ['religion', 'gender', 'ethnicity', 'age'] else 'general'
                
            headline = text.split('. ')[0] if len(text.split('. ')[0]) > 15 else text[:80]
            
            rec = {
                'headline': headline[:150],
                'article_text': text,
                'target_community': target_comm,
                'source_domain': 'cyberbullying_tweets',
                'label': final_label
            }
            
            if final_label == 1:
                records_hostile.append(rec)
            else:
                records_safe.append(rec)
                
        print(f"  ✓ Cyberbullying Benchmark: {len(records_hostile):,} Hostile, {len(records_safe):,} Safe extracted.")
    except Exception as e:
        print(f"  ✗ Error fetching Cyberbullying dataset: {e}")
        
    return records_hostile, records_safe

# =====================================================================
# 3. ETHOS ACADEMIC HATE SPEECH BENCHMARK (2020)
# =====================================================================
def fetch_ethos_benchmark():
    records_hostile = []
    records_safe = []
    print("\n[Source 3] Fetching Ethos Academic Benchmark (2020)...")
    url = 'https://raw.githubusercontent.com/intelligence-csd-auth-gr/Ethos-Hate-Speech-Dataset/master/ethos/ethos_data/Ethos_Dataset_Binary.csv'
    
    try:
        df = pd.read_csv(url, sep=';', on_bad_lines='skip')
        seen_keys = set()
        for _, row in df.iterrows():
            text = clean_text(row.get('comment', ''))
            try:
                score = float(row.get('isHate', 0))
            except Exception:
                score = 0
                
            if not is_academic_safe(text):
                continue
                
            key = normalize_key(text)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            
            final_label = 1 if score >= 0.5 else 0
            target_comm = 'general' if final_label == 1 else 'none'
            
            headline = text.split('. ')[0] if len(text.split('. ')[0]) > 15 else text[:80]
            
            rec = {
                'headline': headline[:150],
                'article_text': text,
                'target_community': target_comm,
                'source_domain': 'ethos_benchmark',
                'label': final_label
            }
            
            if final_label == 1:
                records_hostile.append(rec)
            else:
                records_safe.append(rec)
                
        print(f"  ✓ Ethos: {len(records_hostile):,} Hostile, {len(records_safe):,} Safe extracted.")
    except Exception as e:
        print(f"  ✗ Error fetching Ethos: {e}")
        
    return records_hostile, records_safe

# =====================================================================
# 4. UNIFIED COMPILATION & BALANCING (TARGET: 10,000 ROWS)
# =====================================================================
def run_hate_speech_scaling(target_total=10000):
    target_per_class = target_total // 2
    print("=" * 70)
    print(f"SCALING INDIAN HATE SPEECH CORPUS TO {target_total:,} BALANCED ROWS")
    print(f"Target: {target_per_class:,} Safe (0) & {target_per_class:,} Hostile/Hate (1)")
    print("=" * 70)
    
    # 1. Load prior verified records from existing file
    existing_hostile = []
    existing_safe = []
    if os.path.exists(OUTPUT_CSV):
        try:
            curr_df = pd.read_csv(OUTPUT_CSV)
            print(f"Loaded existing corpus ({len(curr_df)} rows). Preserving prior clean records...")
            for _, r in curr_df.iterrows():
                raw_text = clean_text(r.get('article_text') if pd.notna(r.get('article_text')) else r.get('text', ''))
                if not raw_text or not is_academic_safe(raw_text):
                    continue
                headline = clean_text(r.get('headline', ''))
                if not headline:
                    headline = raw_text.split('. ')[0] if len(raw_text.split('. ')[0]) > 15 else raw_text[:80]
                
                row_dict = {
                    'headline': headline[:150],
                    'article_text': raw_text,
                    'target_community': r.get('target_community') or r.get('category') or 'general',
                    'source_domain': r.get('source_domain') or 'curated_academic',
                    'label': int(r.get('label', 0))
                }
                if row_dict['label'] == 1:
                    existing_hostile.append(row_dict)
                else:
                    row_dict['target_community'] = 'none'
                    existing_safe.append(row_dict)
        except Exception as e:
            print(f"  Note: existing corpus load notice: {e}")

    # 2. Fetch from post-2019 benchmarks
    hatex_hostile, hatex_safe = fetch_iit_kgp_hatexplain()
    cb_hostile, cb_safe = fetch_cyberbullying_benchmark()
    ethos_hostile, ethos_safe = fetch_ethos_benchmark()
    
    all_hostile = existing_hostile + hatex_hostile + cb_hostile + ethos_hostile
    all_safe = existing_safe + hatex_safe + cb_safe + ethos_safe
    
    # 3. Deduplicate Hostile
    print("\nDeduplicating and normalizing Hostile candidate pool...")
    dedup_hostile = []
    seen_hostile_keys = set()
    for row in all_hostile:
        text_val = row.get('article_text', '')
        key = normalize_key(text_val)
        if key and key not in seen_hostile_keys:
            seen_hostile_keys.add(key)
            dedup_hostile.append(row)
            
    # 4. Deduplicate Safe
    print("Deduplicating and normalizing Safe candidate pool...")
    dedup_safe = []
    seen_safe_keys = set()
    for row in all_safe:
        text_val = row.get('article_text', '')
        key = normalize_key(text_val)
        if key and key not in seen_safe_keys:
            seen_safe_keys.add(key)
            dedup_safe.append(row)
            
    # 5. Multi-source balanced quota selection
    hostile_df = pd.DataFrame(dedup_hostile)
    safe_df = pd.DataFrame(dedup_safe)
    
    # Stratified multi-source sampling
    selected_hostile_list = []
    selected_safe_list = []
    
    # Target quotas per source domain
    quotas = {
        'curated_academic': 500,
        'ethos_benchmark': 350,
        'iit_kgp_hatexplain': 2200,
        'cyberbullying_tweets': 1950
    }
    
    # Collect Hostile by quota
    for src, q in quotas.items():
        sub = hostile_df[hostile_df['source_domain'] == src]
        take = min(q, len(sub))
        selected_hostile_list.append(sub.sample(n=take, random_state=42) if len(sub) >= take else sub)
        
    collected_hostile = pd.concat(selected_hostile_list).drop_duplicates(subset=['article_text'])
    if len(collected_hostile) < target_per_class:
        rem = target_per_class - len(collected_hostile)
        unused = hostile_df[~hostile_df['article_text'].isin(collected_hostile['article_text'])]
        collected_hostile = pd.concat([collected_hostile, unused.head(rem)])
    collected_hostile = collected_hostile.head(target_per_class)
    
    # Collect Safe by quota
    for src, q in quotas.items():
        sub = safe_df[safe_df['source_domain'] == src]
        take = min(q, len(sub))
        selected_safe_list.append(sub.sample(n=take, random_state=42) if len(sub) >= take else sub)
        
    collected_safe = pd.concat(selected_safe_list).drop_duplicates(subset=['article_text'])
    if len(collected_safe) < target_per_class:
        rem = target_per_class - len(collected_safe)
        unused = safe_df[~safe_df['article_text'].isin(collected_safe['article_text'])]
        collected_safe = pd.concat([collected_safe, unused.head(rem)])
    collected_safe = collected_safe.head(target_per_class)
    
    df = pd.concat([collected_hostile, collected_safe]).sample(frac=1, random_state=42).reset_index(drop=True)
    df['id'] = range(1, len(df) + 1)
    
    # Standard columns
    cols = ['id', 'headline', 'article_text', 'target_community', 'source_domain', 'label']
    for c in cols:
        if c not in df.columns:
            df[c] = 'none' if c == 'target_community' else ''
    df = df[cols]
    
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    print(f"\n Successfully saved {len(df):,} balanced rows to:")
    print(f"  --> {OUTPUT_CSV}")
    print("\nSource domain distribution:")
    print(df['source_domain'].value_counts())
    print("\nTarget community distribution:")
    print(df['target_community'].value_counts())
    print("\nClass distribution:")
    print(df['label'].value_counts())
    
    # 6. Generate Stratified Splits
    os.makedirs(SPLITS_DIR, exist_ok=True)
    train_df, test_val_df = train_test_split(df, test_size=0.20, random_state=42, stratify=df['label'])
    val_df, test_df = train_test_split(test_val_df, test_size=0.50, random_state=42, stratify=test_val_df['label'])
    
    train_df.to_csv(os.path.join(SPLITS_DIR, 'hate_train.csv'), index=False, encoding='utf-8')
    val_df.to_csv(os.path.join(SPLITS_DIR, 'hate_val.csv'), index=False, encoding='utf-8')
    test_df.to_csv(os.path.join(SPLITS_DIR, 'hate_test.csv'), index=False, encoding='utf-8')
    
    print(f"\n Stratified splits created in {SPLITS_DIR}:")
    print(f"  • hate_train.csv: {len(train_df):,} rows (80%)")
    print(f"  • hate_val.csv:   {len(val_df):,} rows (10%)")
    print(f"  • hate_test.csv:  {len(test_df):,} rows (10%)")

if __name__ == '__main__':
    run_hate_speech_scaling(target_total=10000)
