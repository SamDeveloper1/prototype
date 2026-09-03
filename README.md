# Indian Fake News & Hate Speech Detection System (Phase 2 Prototype)

A production-ready NLP system engineered for detecting contextual misinformation, disinformation, and hate speech across the Indian media and social landscape.

---

## 🏗️ System Architecture

```
sec_prototype/
├── data/                       # Curated datasets and train/val/test splits
│   ├── indian_fake_news_corpus.csv
│   └── splits/
├── models/                     # Trained model weights (.pt, .pkl)
├── notebooks/                  # Jupyter & Google Colab training workflows
├── src/                        # Production Python modules & ETL pipelines
│   ├── fetch_fake_news.py      # Automated scraper for AltNews & Factly
│   ├── fetch_real_news.py      # Automated scraper for The Hindu & Indian Express
│   ├── scale_dataset.py        # Balanced multi-source data builder with deduplication
│   └── add_manual_sample.py    # CLI wizard for manual data entry
├── .env.example                # Environment variables template
├── .gitignore                  # Production Git ignore rules
└── requirements.txt            # Pinned dependencies
```

---

## 🚀 Team Quickstart Guide

### 1. Clone & Setup Virtual Environment

```bash
# Clone the repository
git clone <repo-url>
cd sec_prototype

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install all required dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Copy the template to `.env`:
```bash
cp .env.example .env
```

---

## 📊 Data Pipelines (ETL)

All data collection is automated, strictly English-validated, and deduplicated:

* **Re-build & Scale Dataset**:
  ```bash
  python src/scale_dataset.py
  ```
* **Add a Manual Entry via CLI Wizard**:
  ```bash
  python src/add_manual_sample.py
  ```

---

## 👥 Team Collaboration Guidelines

1. **Branching**: Always branch off `main` for new features (`git checkout -b feature/<feature-name>`).
2. **Commit Messages**: Use clean, descriptive commit messages (e.g. `feat: add RoBERTa fine-tuning script`, `fix: remove non-Latin characters from tokenizer`).
3. **No Hardcoded Absolute Paths**: Always use `os.path` relative to `__file__` or the repository root.
4. **Weights**: Large model checkpoints (`*.pt`, `*.bin`, `*.safetensors`) are ignored by `.gitignore` to prevent exceeding GitHub limits. Store download links in `models/README.md` or use Git LFS / Hugging Face Hub.
