import os
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate'
}

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
OUTPUT_CSV = os.path.join(DATA_DIR, 'indian_fake_news_corpus.csv')

NON_LATIN_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u0900-\u0D7F]')

def clean_text(text):
    if not text:
        return ""
    # Strip HTML tags
    clean = BeautifulSoup(str(text), 'html.parser').get_text(separator=' ', strip=True)
    # Remove multiple spaces/newlines
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def is_strictly_english(title, body):
    if not title or len(title) < 10:
        return False
    if NON_LATIN_PATTERN.search(str(title)):
        return False
    if len(NON_LATIN_PATTERN.findall(str(body))) > 3:
        return False
    return True

def normalize_key(title):
    """Normalize string for strict deduplication (lowercased, alphanumeric only)."""
    return re.sub(r'[^a-z0-9]', '', title.lower())

def fetch_fake_news(target_count=250):
    """Fetches clean English fake news debunks from AltNews and Factly with deduplication."""
    records = []
    seen_keys = set()
    print(f"\n[1/2] Fetching verified Fake/Debunked news (target: {target_count})...")
    
    # AltNews pages
    for p in range(1, 35):
        if len(records) >= target_count:
            break
        url = f"https://www.altnews.in/feed/?paged={p}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
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
                
                pub_date = item.pubDate.text.strip() if item.pubDate else ''
                try:
                    dt = datetime.strptime(pub_date[:16], '%a, %d %b %Y')
                    date_str = dt.strftime('%Y-%m-%d')
                except Exception:
                    date_str = pub_date[:10]

                records.append({
                    'headline': title,
                    'article_text': desc if desc else title,
                    'source_domain': 'altnews.in',
                    'publish_date': date_str,
                    'claim_verdict': 'False',
                    'label': 1
                })
                if len(records) >= target_count:
                    break
            print(f"  ✓ AltNews Page {p}: total unique fake = {len(records)}")
            time.sleep(0.2)
        except Exception as e:
            print(f"  ✗ AltNews Page {p} error: {e}")
            
    print(f"  -> Total Unique Fake records collected: {len(records)}")
    return records[:target_count]

def fetch_real_news(target_count=250):
    """Fetches clean English verified real news from NDTV, The Hindu, Indian Express, and Business Standard."""
    records = []
    seen_keys = set()
    print(f"\n[2/2] Fetching verified Real news from NDTV, The Hindu, Indian Express, and Business Standard (target: {target_count})...")
    
    real_sources = [
        # NDTV Feeds
        ('NDTV India News', 'ndtv.com', 'https://feeds.feedburner.com/ndtvnews-india-news', 30),
        ('NDTV Top Stories', 'ndtv.com', 'https://feeds.feedburner.com/ndtvnews-top-stories', 25),
        ('NDTV Trending News', 'ndtv.com', 'https://feeds.feedburner.com/ndtvnews-trending-news', 20),
        # The Hindu Feeds
        ('The Hindu National', 'thehindu.com', 'https://www.thehindu.com/news/national/feeder/default.rss', 60),
        ('The Hindu Business', 'thehindu.com', 'https://www.thehindu.com/business/feeder/default.rss', 40),
        # Indian Express Feeds
        ('Indian Express India', 'indianexpress.com', 'https://indianexpress.com/section/india/feed/', 60),
        ('Indian Express Cities', 'indianexpress.com', 'https://indianexpress.com/section/cities/feed/', 40),
        # Business Standard
        ('Business Standard', 'business-standard.com', 'https://www.business-standard.com/rss/latest.rss', 25)
    ]
    
    for source_name, domain, url, limit in real_sources:
        if len(records) >= target_count:
            break
        print(f"  Fetching from {source_name}...")
        try:
            r = requests.get(url, headers=HEADERS, timeout=12)
            if r.status_code != 200:
                continue
            soup = BeautifulSoup(r.text, 'xml')
            items = soup.find_all('item')[:limit]
            
            for item in items:
                if len(records) >= target_count:
                    break
                title = clean_text(item.title.text if item.title else '')
                desc = clean_text(item.description.text if item.description else '')
                
                if not is_strictly_english(title, desc):
                    continue
                    
                key = normalize_key(title)
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                
                pub_date = item.pubDate.text.strip() if item.pubDate else ''
                try:
                    dt = datetime.strptime(pub_date[:16], '%a, %d %b %Y')
                    date_str = dt.strftime('%Y-%m-%d')
                except Exception:
                    date_str = pub_date[:10]

                records.append({
                    'headline': title,
                    'article_text': desc if desc else title,
                    'source_domain': domain,
                    'publish_date': date_str,
                    'claim_verdict': 'Verified Real',
                    'label': 0
                })
            print(f"  ✓ {source_name}: unique real collected so far = {len(records)}")
            time.sleep(0.2)
        except Exception as e:
            print(f"  ✗ Error fetching {source_name}: {e}")

    print(f"  -> Total Unique Real records collected: {len(records)}")
    return records[:target_count]

def scale_and_balance_dataset(target_per_class=250):
    os.makedirs(DATA_DIR, exist_ok=True)
    
    fake_records = fetch_fake_news(target_count=target_per_class)
    real_records = fetch_real_news(target_count=target_per_class)
    
    # Exact 50/50 balance
    min_count = min(len(fake_records), len(real_records))
    fake_records = fake_records[:min_count]
    real_records = real_records[:min_count]
    
    combined = fake_records + real_records
    df = pd.DataFrame(combined)
    
    # Final global deduplication pass
    df['norm_key'] = df['headline'].apply(normalize_key)
    df.drop_duplicates(subset=['norm_key'], keep='first', inplace=True)
    df.drop(columns=['norm_key'], inplace=True)
    
    # Sequential ID
    df.reset_index(drop=True, inplace=True)
    df['id'] = range(1, len(df) + 1)
    
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    
    print("\n" + "=" * 65)
    print(f"🎯 DATASET UPDATED IN sec_prototype: {len(df)} TOTAL ROWS")
    print("=" * 65)
    print("Class Balance:")
    print(df['label'].value_counts().rename(index={1: 'Fake (1)', 0: 'Real (0)'}))
    print("\nVerified Sources Breakdown (Including NDTV):")
    print(df['source_domain'].value_counts())
    print("\nDate Range:")
    print(f"  From {df['publish_date'].min()} to {df['publish_date'].max()}")
    print("=" * 65)
    print(f"📁 Output file: {OUTPUT_CSV}")

if __name__ == '__main__':
    scale_and_balance_dataset(target_per_class=250)
