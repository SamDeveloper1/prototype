import os
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

def fetch_the_hindu_real_news(limit=50):
    """Fetches verified real national news from The Hindu RSS feed."""
    records = []
    print(f"Fetching verified news from The Hindu (up to {limit})...")
    url = "https://www.thehindu.com/news/national/feeder/default.rss"
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        soup = BeautifulSoup(r.text, 'xml')
        items = soup.find_all('item')[:limit]
        
        for item in items:
            title = item.title.text.strip() if item.title else ''
            desc = item.description.text.strip() if item.description else ''
            clean_desc = BeautifulSoup(desc, 'html.parser').get_text(separator=' ', strip=True) if desc else title
            pub_date = item.pubDate.text.strip() if item.pubDate else ''
            try:
                dt = datetime.strptime(pub_date[:16], '%a, %d %b %Y')
                date_str = dt.strftime('%Y-%m-%d')
            except Exception:
                date_str = pub_date[:10]

            records.append({
                'headline': title,
                'article_text': clean_desc,
                'source_domain': 'thehindu.com',
                'publish_date': date_str,
                'claim_verdict': 'Verified Real',
                'label': 0
            })
        print(f"  ✓ Fetched {len(records)} real news stories from The Hindu")
    except Exception as e:
        print(f"  ✗ Error fetching The Hindu: {e}")
    return records

def fetch_indian_express_real_news(limit=50):
    """Fetches verified real national news from The Indian Express."""
    records = []
    print(f"Fetching verified news from The Indian Express (up to {limit})...")
    url = "https://indianexpress.com/section/india/feed/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        soup = BeautifulSoup(r.text, 'xml')
        items = soup.find_all('item')[:limit]
        
        for idx, item in enumerate(items, 1):
            title = item.title.text.strip() if item.title else ''
            link = item.link.text.strip() if item.link else ''
            pub_date = item.pubDate.text.strip() if item.pubDate else ''
            try:
                dt = datetime.strptime(pub_date[:16], '%a, %d %b %Y')
                date_str = dt.strftime('%Y-%m-%d')
            except Exception:
                date_str = pub_date[:10]

            # Fetch lead paragraphs from article
            body_text = title
            if link:
                try:
                    art_r = requests.get(link, headers=HEADERS, timeout=5)
                    art_soup = BeautifulSoup(art_r.text, 'html.parser')
                    body_div = art_soup.find(id='pcl-full-content') or art_soup.find(class_='story_details') or art_soup.find('article')
                    if body_div:
                        paras = [p.text.strip() for p in body_div.find_all('p') if len(p.text.strip()) > 50]
                        if paras:
                            body_text = ' '.join(paras[:2])
                except Exception:
                    pass

            records.append({
                'headline': title,
                'article_text': body_text,
                'source_domain': 'indianexpress.com',
                'publish_date': date_str,
                'claim_verdict': 'Verified Real',
                'label': 0
            })
            if idx % 10 == 0:
                print(f"  ... fetched {idx}/{limit} articles")
                time.sleep(0.3)

        print(f"  ✓ Fetched {len(records)} real news stories from The Indian Express")
    except Exception as e:
        print(f"  ✗ Error fetching The Indian Express: {e}")
    return records

def append_real_news(hindu_count=50, express_count=50):
    os.makedirs(DATA_DIR, exist_ok=True)
    
    real_records = fetch_the_hindu_real_news(limit=hindu_count)
    real_records += fetch_indian_express_real_news(limit=express_count)
    
    if not real_records:
        print("No real records fetched.")
        return
        
    real_df = pd.DataFrame(real_records)
    
    if os.path.exists(OUTPUT_CSV):
        corpus_df = pd.read_csv(OUTPUT_CSV)
        print(f"\nExisting corpus has {len(corpus_df)} rows. Appending real news...")
        combined_df = pd.concat([corpus_df, real_df], ignore_index=True)
        # Drop duplicates by headline
        combined_df.drop_duplicates(subset=['headline'], keep='first', inplace=True)
    else:
        combined_df = real_df

    # Reset IDs sequentially
    combined_df.reset_index(drop=True, inplace=True)
    if 'id' in combined_df.columns:
        combined_df['id'] = range(1, len(combined_df) + 1)
    else:
        combined_df.insert(0, 'id', range(1, len(combined_df) + 1))
        
    combined_df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    
    print("\n" + "=" * 60)
    print(f"🎉 Corpus updated successfully! Total rows: {len(combined_df)}")
    print("Class Balance:")
    print(combined_df['label'].value_counts().rename(index={1: 'Fake (1)', 0: 'Real (0)'}))
    print("Sources Breakdown:")
    print(combined_df['source_domain'].value_counts())
    print("=" * 60)
    print(f"📁 Saved to: {OUTPUT_CSV}")

if __name__ == '__main__':
    append_real_news(hindu_count=50, express_count=50)
