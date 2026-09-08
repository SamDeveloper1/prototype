"""
Scale Fake News Corpus to 10,000 Rows (5,000 Real, 5,000 Fake)
=============================================================
Sources:
  [Fake News (5,000 rows)]
    - IIIT-Delhi Verified Constraint Misinformation Dataset
    - Alt News (altnews.in)
    - BOOM Live (boomlive.in)
    - Factly (factly.in)
    - Newschecker (newschecker.in)
    - Quint WebQoof (thequint.com)
  [Real News (5,000 rows)]
    - Press Information Bureau (PIB Government Releases)
    - The Hindu (thehindu.com)
    - NDTV (ndtv.com)
    - The Indian Express (indianexpress.com)
    - Business Standard (business-standard.com)
"""

import os
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SPLITS_DIR = os.path.join(DATA_DIR, 'splits')
OUTPUT_CSV = os.path.join(DATA_DIR, 'indian_fake_news_corpus.csv')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

# Regex to detect non-Latin scripts (Devanagari, Telugu, Tamil, Arabic/Urdu, etc.)
NON_LATIN_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u0900-\u0D7F]')

def clean_text(text):
    if not text or pd.isna(text):
        return ""
    # Strip HTML tags
    clean = BeautifulSoup(str(text), 'html.parser').get_text(separator=' ', strip=True)
    # Remove excessive whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def is_strictly_english(title, body):
    if not title or len(str(title).strip()) < 8:
        return False
    # No non-Latin characters in title
    if NON_LATIN_PATTERN.search(str(title)):
        return False
    # Allow maximum 3 stray non-Latin symbols in body
    if len(NON_LATIN_PATTERN.findall(str(body))) > 3:
        return False
    return True

def normalize_key(title):
    """Normalized alphanumeric key for strict deduplication."""
    return re.sub(r'[^a-z0-9]', '', str(title).lower())

# =====================================================================
# 1. IIIT-DELHI VERIFIED KAGGLE / CONSTRAINT DATASET
# =====================================================================
def fetch_iiit_delhi_constraint():
    """
    Loads verified Indian/Pandemic misinformation from the official
    IIIT-Delhi AAAI Constraint benchmark.
    """
    records_fake = []
    records_real = []
    print("\n[Source 1] Loading IIIT-Delhi Verified Misinformation Benchmark...")
    
    urls = [
        'https://raw.githubusercontent.com/diptamath/covid_fake_news/main/data/Constraint_Train.csv',
        'https://raw.githubusercontent.com/diptamath/covid_fake_news/main/data/Constraint_Val.csv'
    ]
    
    seen_keys = set()
    for u in urls:
        try:
            df = pd.read_csv(u)
            for _, row in df.iterrows():
                text = clean_text(row.get('tweet', ''))
                raw_label = str(row.get('label', '')).strip().lower()
                
                if len(text) < 25:
                    continue
                if not is_strictly_english(text[:60], text):
                    continue
                
                key = normalize_key(text[:80])
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                
                # First sentence / 12 words as headline
                parts = text.split('. ')
                headline = parts[0] if len(parts[0]) > 15 else text[:90]
                
                record = {
                    'headline': headline[:160],
                    'article_text': text,
                    'source_domain': 'iiitd_constraint',
                    'publish_date': '2020-2021',
                    'claim_verdict': 'False' if raw_label == 'fake' else 'Verified Real',
                    'label': 1 if raw_label == 'fake' else 0
                }
                
                if raw_label == 'fake':
                    records_fake.append(record)
                elif raw_label == 'real':
                    records_real.append(record)
        except Exception as e:
            print(f"  ✗ Error loading {u}: {e}")
            
    print(f"  ✓ IIIT-Delhi: {len(records_fake)} Fake claims, {len(records_real)} Real records extracted.")
    return records_fake, records_real

# =====================================================================
# 2. FAKE NEWS SCRAPERS (AltNews, BOOM Live, Factly, Newschecker, Quint)
# =====================================================================
def scrape_altnews_archives(max_pages=75):
    """Scrapes Alt News paginated RSS feeds."""
    records = []
    seen_keys = set()
    print(f"\n[Source 2] Scraping Alt News Archives (up to {max_pages} pages)...")
    for p in range(1, max_pages + 1):
        try:
            url = f"https://www.altnews.in/feed/?paged={p}"
            r = requests.get(url, headers=HEADERS, timeout=8)
            if r.status_code != 200:
                break
            soup = BeautifulSoup(r.text, 'xml')
            items = soup.find_all('item')
            if not items:
                break
            for item in items:
                title = clean_text(item.title.text if item.title else '')
                desc = clean_text(item.description.text if item.description else '')
                if not is_strictly_english(title, desc):
                    continue
                key = normalize_key(title)
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                pub_date = item.pubDate.text.strip() if item.pubDate else '2023-2024'
                records.append({
                    'headline': title,
                    'article_text': desc if len(desc) > 30 else title,
                    'source_domain': 'altnews.in',
                    'publish_date': pub_date[:16],
                    'claim_verdict': 'False',
                    'label': 1
                })
            time.sleep(0.1)
        except Exception:
            break
    print(f"  ✓ Alt News: {len(records)} debunks collected.")
    return records

def scrape_factly_archives(max_pages=75):
    """Scrapes Factly paginated RSS feeds."""
    records = []
    seen_keys = set()
    print(f"\n[Source 3] Scraping Factly Fake News Archives (up to {max_pages} pages)...")
    for p in range(1, max_pages + 1):
        try:
            url = f"https://factly.in/category/fake-news/feed/?paged={p}"
            r = requests.get(url, headers=HEADERS, timeout=8)
            if r.status_code != 200:
                url = f"https://factly.in/feed/?paged={p}"
                r = requests.get(url, headers=HEADERS, timeout=8)
                if r.status_code != 200:
                    break
            soup = BeautifulSoup(r.text, 'xml')
            items = soup.find_all('item')
            if not items:
                break
            for item in items:
                title = clean_text(item.title.text if item.title else '')
                desc = clean_text(item.description.text if item.description else '')
                if not is_strictly_english(title, desc):
                    continue
                key = normalize_key(title)
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                pub_date = item.pubDate.text.strip() if item.pubDate else '2023-2024'
                records.append({
                    'headline': title,
                    'article_text': desc if len(desc) > 30 else title,
                    'source_domain': 'factly.in',
                    'publish_date': pub_date[:16],
                    'claim_verdict': 'False',
                    'label': 1
                })
            time.sleep(0.1)
        except Exception:
            break
    print(f"  ✓ Factly: {len(records)} debunks collected.")
    return records

def scrape_boomlive_feed():
    """Scrapes BOOM Live English debunk feed."""
    records = []
    seen_keys = set()
    print("\n[Source 4] Scraping BOOM Live Fact-Checks...")
    endpoints = [
        'https://www.boomlive.in/feeds/rss.xml',
        'https://www.boomlive.in/fast-check/feed'
    ]
    for url in endpoints:
        try:
            r = requests.get(url, headers=HEADERS, timeout=8)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'xml')
                items = soup.find_all('item')
                for item in items:
                    title = clean_text(item.title.text if item.title else '')
                    desc = clean_text(item.description.text if item.description else '')
                    if not is_strictly_english(title, desc):
                        continue
                    key = normalize_key(title)
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)
                    records.append({
                        'headline': title,
                        'article_text': desc if len(desc) > 30 else title,
                        'source_domain': 'boomlive.in',
                        'publish_date': item.pubDate.text[:16] if item.pubDate else '2023-2024',
                        'claim_verdict': 'False',
                        'label': 1
                    })
        except Exception:
            continue
    print(f"  ✓ BOOM Live: {len(records)} debunks collected.")
    return records

def scrape_newschecker_feed():
    """Scrapes Newschecker Indian Fact-Checks."""
    records = []
    seen_keys = set()
    print("\n[Source 5] Scraping Newschecker India Feed...")
    urls = [
        'https://newschecker.in/feed/',
        'https://newschecker.in/category/fact-checks/feed/'
    ]
    for url in urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=8)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'xml')
                items = soup.find_all('item')
                for item in items:
                    title = clean_text(item.title.text if item.title else '')
                    desc = clean_text(item.description.text if item.description else '')
                    if not is_strictly_english(title, desc):
                        continue
                    key = normalize_key(title)
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)
                    records.append({
                        'headline': title,
                        'article_text': desc if len(desc) > 30 else title,
                        'source_domain': 'newschecker.in',
                        'publish_date': item.pubDate.text[:16] if item.pubDate else '2023-2024',
                        'claim_verdict': 'False',
                        'label': 1
                    })
        except Exception:
            continue
    print(f"  ✓ Newschecker: {len(records)} debunks collected.")
    return records

def scrape_quint_webqoof():
    """Scrapes Quint WebQoof debunk vertical."""
    records = []
    seen_keys = set()
    print("\n[Source 6] Scraping Quint WebQoof Fact-Checks...")
    urls = [
        'https://www.thequint.com/rss/webqoof.xml',
        'https://www.thequint.com/news/webqoof'
    ]
    for url in urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=8)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'xml' if 'xml' in url else 'html.parser')
                items = soup.find_all('item') if 'xml' in url else soup.find_all('article')
                for item in items:
                    title_tag = item.find('title') if 'xml' in url else item.find(['h2', 'h3'])
                    title = clean_text(title_tag.text if title_tag else '')
                    desc_tag = item.find('description') if 'xml' in url else item.find('p')
                    desc = clean_text(desc_tag.text if desc_tag else '')
                    if not is_strictly_english(title, desc):
                        continue
                    key = normalize_key(title)
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)
                    records.append({
                        'headline': title,
                        'article_text': desc if len(desc) > 30 else title,
                        'source_domain': 'thequint.com/webqoof',
                        'publish_date': '2023-2024',
                        'claim_verdict': 'False',
                        'label': 1
                    })
        except Exception:
            continue
    print(f"  ✓ Quint WebQoof: {len(records)} debunks collected.")
    return records

# =====================================================================
# 3. REAL NEWS SCRAPERS (PIB, The Hindu, NDTV, Express, Business Standard)
# =====================================================================
def scrape_the_hindu_feed():
    records = []
    seen_keys = set()
    print("\n[Source 7] Scraping The Hindu National News...")
    urls = [
        "https://www.thehindu.com/news/national/feeder/default.rss",
        "https://www.thehindu.com/business/feeder/default.rss",
        "https://www.thehindu.com/sci-tech/feeder/default.rss"
    ]
    for u in urls:
        try:
            r = requests.get(u, headers=HEADERS, timeout=8)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'xml')
                for item in soup.find_all('item'):
                    title = clean_text(item.title.text if item.title else '')
                    desc = clean_text(item.description.text if item.description else '')
                    key = normalize_key(title)
                    if key in seen_keys or not is_strictly_english(title, desc):
                        continue
                    seen_keys.add(key)
                    records.append({
                        'headline': title,
                        'article_text': desc if len(desc) > 30 else title,
                        'source_domain': 'thehindu.com',
                        'publish_date': item.pubDate.text[:16] if item.pubDate else '2024',
                        'claim_verdict': 'Verified Real',
                        'label': 0
                    })
        except Exception:
            continue
    print(f"  ✓ The Hindu: {len(records)} real news records.")
    return records

def scrape_ndtv_feed():
    records = []
    seen_keys = set()
    print("\n[Source 8] Scraping NDTV India News...")
    urls = [
        "https://feeds.feedburner.com/ndtvnews-india-news",
        "https://feeds.feedburner.com/ndtvnews-top-stories"
    ]
    for u in urls:
        try:
            r = requests.get(u, headers=HEADERS, timeout=8)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'xml')
                for item in soup.find_all('item'):
                    title = clean_text(item.title.text if item.title else '')
                    desc = clean_text(item.description.text if item.description else '')
                    key = normalize_key(title)
                    if key in seen_keys or not is_strictly_english(title, desc):
                        continue
                    seen_keys.add(key)
                    records.append({
                        'headline': title,
                        'article_text': desc if len(desc) > 30 else title,
                        'source_domain': 'ndtv.com',
                        'publish_date': item.pubDate.text[:16] if item.pubDate else '2024',
                        'claim_verdict': 'Verified Real',
                        'label': 0
                    })
        except Exception:
            continue
    print(f"  ✓ NDTV: {len(records)} real news records.")
    return records

def scrape_indian_express_feed():
    records = []
    seen_keys = set()
    print("\n[Source 9] Scraping The Indian Express...")
    urls = [
        "https://indianexpress.com/section/india/feed/",
        "https://indianexpress.com/section/business/feed/"
    ]
    for u in urls:
        try:
            r = requests.get(u, headers=HEADERS, timeout=8)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'xml')
                for item in soup.find_all('item'):
                    title = clean_text(item.title.text if item.title else '')
                    desc = clean_text(item.description.text if item.description else '')
                    key = normalize_key(title)
                    if key in seen_keys or not is_strictly_english(title, desc):
                        continue
                    seen_keys.add(key)
                    records.append({
                        'headline': title,
                        'article_text': desc if len(desc) > 30 else title,
                        'source_domain': 'indianexpress.com',
                        'publish_date': item.pubDate.text[:16] if item.pubDate else '2024',
                        'claim_verdict': 'Verified Real',
                        'label': 0
                    })
        except Exception:
            continue
    print(f"  ✓ Indian Express: {len(records)} real news records.")
    return records

def scrape_business_standard_feed():
    records = []
    seen_keys = set()
    print("\n[Source 10] Scraping Business Standard...")
    urls = [
        "https://www.business-standard.com/rss/latest.rss",
        "https://www.business-standard.com/rss/economy-policy-102.rss"
    ]
    for u in urls:
        try:
            r = requests.get(u, headers=HEADERS, timeout=8)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'xml')
                for item in soup.find_all('item'):
                    title = clean_text(item.title.text if item.title else '')
                    desc = clean_text(item.description.text if item.description else '')
                    key = normalize_key(title)
                    if key in seen_keys or not is_strictly_english(title, desc):
                        continue
                    seen_keys.add(key)
                    records.append({
                        'headline': title,
                        'article_text': desc if len(desc) > 30 else title,
                        'source_domain': 'business-standard.com',
                        'publish_date': item.pubDate.text[:16] if item.pubDate else '2024',
                        'claim_verdict': 'Verified Real',
                        'label': 0
                    })
        except Exception:
            continue
    print(f"  ✓ Business Standard: {len(records)} real news records.")
    return records

def fetch_pib_releases():
    """Fetches official Press Information Bureau releases."""
    records = []
    seen_keys = set()
    print("\n[Source 11] Scraping PIB Government Releases...")
    # Scrape PIB English press release feed / releases
    try:
        url = "https://pib.gov.in/RssMain.aspx?ModId=6&LangId=1"
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'xml')
            for item in soup.find_all('item'):
                title = clean_text(item.title.text if item.title else '')
                desc = clean_text(item.description.text if item.description else '')
                key = normalize_key(title)
                if key in seen_keys or not is_strictly_english(title, desc):
                    continue
                seen_keys.add(key)
                records.append({
                    'headline': title,
                    'article_text': desc if len(desc) > 30 else title,
                    'source_domain': 'pib.gov.in',
                    'publish_date': item.pubDate.text[:16] if item.pubDate else '2024',
                    'claim_verdict': 'Verified Real',
                    'label': 0
                })
    except Exception as e:
        print(f"  ✗ PIB notice: {e}")
    print(f"  ✓ PIB: {len(records)} official releases collected.")
    return records

# =====================================================================
# 4. UNIFIED MERGER & STRATIFIED SPLITS
# =====================================================================
def run_scaling_pipeline(target_total=10000):
    target_per_class = target_total // 2
    print("=" * 70)
    print(f"SCALING INDIAN FAKE NEWS DATASET TO {target_total:,} ROWS")
    print(f"Target: {target_per_class:,} Fake News (1) & {target_per_class:,} Real News (0)")
    print("=" * 70)
    
    # Existing dataset
    existing_fake = []
    existing_real = []
    if os.path.exists(OUTPUT_CSV):
        try:
            curr_df = pd.read_csv(OUTPUT_CSV)
            print(f"Loaded existing corpus ({len(curr_df)} rows). Preserving prior verified records.")
            for _, r in curr_df.iterrows():
                row_dict = r.to_dict()
                if row_dict.get('label') == 1:
                    existing_fake.append(row_dict)
                else:
                    existing_real.append(row_dict)
        except Exception:
            pass

    # Collect Fake sources
    iiitd_fake, iiitd_real = fetch_iiit_delhi_constraint()
    altnews_fake = scrape_altnews_archives(max_pages=85)
    factly_fake = scrape_factly_archives(max_pages=85)
    boom_fake = scrape_boomlive_feed()
    newschecker_fake = scrape_newschecker_feed()
    quint_fake = scrape_quint_webqoof()
    
    all_fake_candidates = (
        existing_fake +
        altnews_fake +
        factly_fake +
        boom_fake +
        newschecker_fake +
        quint_fake +
        iiitd_fake
    )
    
    # Collect Real sources
    hindu_real = scrape_the_hindu_feed()
    ndtv_real = scrape_ndtv_feed()
    express_real = scrape_indian_express_feed()
    bs_real = scrape_business_standard_feed()
    pib_real = fetch_pib_releases()
    
    all_real_candidates = (
        existing_real +
        hindu_real +
        ndtv_real +
        express_real +
        bs_real +
        pib_real +
        iiitd_real
    )
    
    # Deduplicate Fake
    print("\nDeduplicating and normalizing Fake candidates...")
    dedup_fake = []
    seen_fake_keys = set()
    for row in all_fake_candidates:
        key = normalize_key(row['headline'])
        if key and key not in seen_fake_keys:
            seen_fake_keys.add(key)
            dedup_fake.append(row)
            
    # Deduplicate Real
    print("Deduplicating and normalizing Real candidates...")
    dedup_real = []
    seen_real_keys = set()
    for row in all_real_candidates:
        key = normalize_key(row['headline'])
        if key and key not in seen_real_keys:
            seen_real_keys.add(key)
            dedup_real.append(row)
            
    print(f"\nAvailable Pool: {len(dedup_fake):,} unique Fake | {len(dedup_real):,} unique Real")
    
    # Balance to exact count
    final_count_per_class = min(target_per_class, len(dedup_fake), len(dedup_real))
    selected_fake = dedup_fake[:final_count_per_class]
    selected_real = dedup_real[:final_count_per_class]
    
    combined = selected_fake + selected_real
    df = pd.DataFrame(combined)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df['id'] = range(1, len(df) + 1)
    
    # Reorder columns
    cols = ['id', 'headline', 'article_text', 'source_domain', 'publish_date', 'claim_verdict', 'label']
    df = df[[c for c in cols if c in df.columns]]
    
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    print(f"\n Successfully saved {len(df):,} balanced rows to:")
    print(f"  --> {OUTPUT_CSV}")
    print("\nSource domain distribution:")
    print(df['source_domain'].value_counts())
    print("\nClass distribution:")
    print(df['label'].value_counts())
    
    # Generate Stratified Splits
    os.makedirs(SPLITS_DIR, exist_ok=True)
    train_df, test_val_df = train_test_split(df, test_size=0.20, random_state=42, stratify=df['label'])
    val_df, test_df = train_test_split(test_val_df, test_size=0.50, random_state=42, stratify=test_val_df['label'])
    
    train_df.to_csv(os.path.join(SPLITS_DIR, 'train.csv'), index=False, encoding='utf-8')
    val_df.to_csv(os.path.join(SPLITS_DIR, 'val.csv'), index=False, encoding='utf-8')
    test_df.to_csv(os.path.join(SPLITS_DIR, 'test.csv'), index=False, encoding='utf-8')
    
    print(f"\n Stratified splits created in {SPLITS_DIR}:")
    print(f"  • train.csv: {len(train_df):,} rows (80%)")
    print(f"  • val.csv:   {len(val_df):,} rows (10%)")
    print(f"  • test.csv:  {len(test_df):,} rows (10%)")

if __name__ == '__main__':
    run_scaling_pipeline(target_total=10000)
