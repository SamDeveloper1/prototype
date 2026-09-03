import os
import argparse
import pandas as pd
from datetime import datetime

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
OUTPUT_CSV = os.path.join(DATA_DIR, 'indian_fake_news_corpus.csv')

def add_sample(headline, article_text, source_domain, publish_date, claim_verdict, label):
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Check if CSV exists
    if os.path.exists(OUTPUT_CSV):
        df = pd.read_csv(OUTPUT_CSV)
        next_id = len(df) + 1
    else:
        df = pd.DataFrame(columns=['id', 'headline', 'article_text', 'source_domain', 'publish_date', 'claim_verdict', 'label'])
        next_id = 1
        
    new_row = {
        'id': next_id,
        'headline': headline.strip(),
        'article_text': article_text.strip(),
        'source_domain': source_domain.strip(),
        'publish_date': publish_date.strip(),
        'claim_verdict': claim_verdict.strip(),
        'label': int(label)
    }
    
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    
    print("\n✅ New sample successfully added to dataset!")
    print(f"  • ID: {next_id}")
    print(f"  • Headline: {headline}")
    print(f"  • Source: {source_domain}")
    print(f"  • Date: {publish_date}")
    print(f"  • Label: {label} ({'Fake' if int(label) == 1 else 'Real'})")
    print(f"  • Total corpus size: {len(df)} rows")

def interactive_mode():
    print("=" * 60)
    print("📝 Manual News Sample Entry Wizard")
    print("=" * 60)
    
    today_str = datetime.today().strftime('%Y-%m-%d')
    
    headline = input("1. Enter Headline / Viral Claim: ").strip()
    while not headline:
        print("   Headline cannot be empty!")
        headline = input("   Enter Headline / Viral Claim: ").strip()
        
    article_text = input("2. Enter Body Context / Detailed Claim (press Enter to skip): ").strip()
    if not article_text:
        article_text = headline
        
    source = input("3. Enter Source / Domain [Default: PIB Fact Check]: ").strip()
    if not source:
        source = "pib.gov.in"
        
    date = input(f"4. Enter Date (YYYY-MM-DD) [Default: {today_str}]: ").strip()
    if not date:
        date = today_str
        
    verdict = input("5. Enter Verdict (e.g. False, Misleading, Real) [Default: False]: ").strip()
    if not verdict:
        verdict = "False"
        
    label_input = input("6. Enter Label (1 = Fake/Debunked, 0 = Real) [Default: 1]: ").strip()
    label = 1 if label_input != "0" else 0
    
    add_sample(headline, article_text, source, date, verdict, label)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Add a manual news sample to indian_fake_news_corpus.csv")
    parser.add_argument('--headline', type=str, help="Headline or viral claim")
    parser.add_argument('--text', type=str, default="", help="Article body text or description")
    parser.add_argument('--source', type=str, default="PIB Fact Check", help="Source or domain name")
    parser.add_argument('--date', type=str, default=datetime.today().strftime('%Y-%m-%d'), help="Publication date (YYYY-MM-DD)")
    parser.add_argument('--verdict', type=str, default="False", help="Verdict label (e.g., False, Misleading, Real)")
    parser.add_argument('--label', type=int, default=1, help="Numerical label: 1 for Fake, 0 for Real")
    
    args = parser.parse_args()
    
    if args.headline:
        text = args.text if args.text else args.headline
        add_sample(args.headline, text, args.source, args.date, args.verdict, args.label)
    else:
        interactive_mode()
