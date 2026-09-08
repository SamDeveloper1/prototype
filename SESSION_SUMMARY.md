# Session Summary & Resumption Guide

**Last Updated**: September 4, 2026  
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

## 🎯 Immediate Next Steps When You Resume

1. **Run 10k Dataset Pipeline (`scale_fake_news_10k.py`)**:
   - Collect and merge the confirmed sources into the 10,000-row `indian_fake_news_corpus.csv` file.
   - Generate stratified splits (Train: 8k, Val: 1k, Test: 1k).
2. **Model Training (Notebook / Colab)**:
   - Train 3–4 classical ML baselines (TF-IDF + Logistic Regression, SVM, Naive Bayes, Random Forest).
   - Fine-tune 2 Deep Learning Transformer models (DeBERTa-v3 for Fake News, IndicBERT / RoBERTa for Hate Speech).

