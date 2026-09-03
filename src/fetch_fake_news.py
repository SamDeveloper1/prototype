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

# Non-Latin script pattern (catches Arabic/Urdu, Telugu, Devanagari, Tamil, etc.)
NON_LATIN_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u0900-\u0D7F]')

def is_strictly_english(title, body):
    """Ensures that headline and text are in English and contain no regional scripts."""
    if NON_LATIN_PATTERN.search(str(title)):
        return False
    if len(NON_LATIN_PATTERN.findall(str(body))) > 3:
        return False
    return True

def fetch_altnews_rss(pages=5):
    """Fetches recent debunked stories in English from AltNews."""
    records = []
    print(f"Fetching AltNews RSS ({pages} pages)...")
    for p in range(1, pages + 1):
        try:
            url = f"https://www.altnews.in/feed/?paged={p}"
            r = requests.get(url, headers=HEADERS, timeout=12)
            if r.status_code != 200:
                break
            soup = BeautifulSoup(r.text, 'xml')
            items = soup.find_all('item')
            if not items:
                break
            for item in items:
                title = item.title.text.strip() if item.title else ''
                desc = item.description.text.strip() if item.description else ''
                clean_desc = BeautifulSoup(desc, 'html.parser').get_text(separator=' ', strip=True)
                
                if not is_strictly_english(title, clean_desc):
                    continue

                pub_date = item.pubDate.text.strip() if item.pubDate else ''
                try:
                    dt = datetime.strptime(pub_date[:16], '%a, %d %b %Y')
                    date_str = dt.strftime('%Y-%m-%d')
                except Exception:
                    date_str = pub_date[:10]

                records.append({
                    'headline': title,
                    'article_text': clean_desc,
                    'source_domain': 'altnews.in',
                    'publish_date': date_str,
                    'claim_verdict': 'False',
                    'label': 1
                })
            print(f"  ✓ AltNews Page {p}: {len(items)} items processed ({len(records)} English accepted)")
            time.sleep(0.3)
        except Exception as e:
            print(f"  ✗ AltNews Page {p} error: {e}")
    return records

def fetch_factly_rss(pages=5):
    """Fetches recent debunked stories in English from Factly."""
    records = []
    print(f"Fetching Factly RSS ({pages} pages)...")
    for p in range(1, pages + 1):
        try:
            url = f"https://factly.in/feed/?paged={p}"
            r = requests.get(url, headers=HEADERS, timeout=12)
            if r.status_code != 200:
                break
            soup = BeautifulSoup(r.text, 'xml')
            items = soup.find_all('item')
            if not items:
                break
            for item in items:
                title = item.title.text.strip() if item.title else ''
                desc = item.description.text.strip() if item.description else ''
                clean_desc = BeautifulSoup(desc, 'html.parser').get_text(separator=' ', strip=True)
                
                if not is_strictly_english(title, clean_desc):
                    continue

                pub_date = item.pubDate.text.strip() if item.pubDate else ''
                try:
                    dt = datetime.strptime(pub_date[:16], '%a, %d %b %Y')
                    date_str = dt.strftime('%Y-%m-%d')
                except Exception:
                    date_str = pub_date[:10]

                records.append({
                    'headline': title,
                    'article_text': clean_desc,
                    'source_domain': 'factly.in',
                    'publish_date': date_str,
                    'claim_verdict': 'False',
                    'label': 1
                })
            print(f"  ✓ Factly Page {p}: {len(items)} items processed ({len(records)} English accepted)")
            time.sleep(0.3)
        except Exception as e:
            print(f"  ✗ Factly Page {p} error: {e}")
    return records

def build_fake_news_corpus(pages_per_source=5):
    os.makedirs(DATA_DIR, exist_ok=True)
    
    altnews_records = fetch_altnews_rss(pages=pages_per_source)
    factly_records = fetch_factly_rss(pages=pages_per_source)
    
    all_records = altnews_records + factly_records
    if not all_records:
        print("No records fetched.")
        return
        
    df = pd.DataFrame(all_records)
    
    if os.path.exists(OUTPUT_CSV):
        existing_df = pd.read_csv(OUTPUT_CSV)
        print(f"Existing corpus has {len(existing_df)} rows. Merging...")
        df = pd.concat([existing_df, df], ignore_index=True)
        df.drop_duplicates(subset=['headline'], keep='first', inplace=True)
    
    df.reset_index(drop=True, inplace=True)
    if 'id' in df.columns:
        df['id'] = range(1, len(df) + 1)
    else:
        df.insert(0, 'id', range(1, len(df) + 1))
        
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    print(f"\n Successfully saved {len(df)} total records to:")
    print(f"  --> {OUTPUT_CSV}")

if __name__ == '__main__':
    build_fake_news_corpus(pages_per_source=5)
