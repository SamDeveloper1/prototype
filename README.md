# 📰 The Veritas Chronicle: Indian Fake News & Hate Speech Detection System

An academic, production-grade AI system engineered for real-time verification of contextual misinformation, disinformation, and multimodal hate speech across the Indian socio-political landscape.

---

## 🏛️ System Architecture

* **Backend**: FastAPI (`http://localhost:8000`)
* **Frontend**: Next.js 14 App Router, TypeScript, Tailwind CSS, Framer Motion (`http://localhost:3000`)
* **Natural Language Processing**:
  * **Classical ML Baselines**: Linear Support Vector Machines (SVM), Logistic Regression, Naive Bayes, Random Forest (Trained on 20,000 Indian news & toxicity samples).
  * **Deep Learning Transformers**: Fine-tuned BERT (`bert-base-uncased` — **97.02% F1** on Fake News, **78.08% F1** on Hate Speech).
* **Multimodal Speech-to-Text**: OpenAI Whisper (`base` model, ~74M parameters) + `ffmpeg` for extracting and transcribing audio tracks from uploaded `.mp4` and `.mov` videos.

---

## 📋 Prerequisites & Installation

To run this project on any machine (**Windows**, **macOS**, or **Linux**), ensure you have:
1. **Python 3.10+**
2. **Node.js 18+ or 20+** and `npm`
3. **ffmpeg** (required for extracting audio from video files)

### Step 1: Install `ffmpeg` on Your System

* **macOS** (via Homebrew):
  ```bash
  brew install ffmpeg
  ```
* **Windows** (via PowerShell or Command Prompt):
  ```powershell
  winget install Gyan.FFmpeg
  # Or via Chocolatey: choco install ffmpeg
  ```
* **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update && sudo apt install -y ffmpeg
  ```

---

## 🚀 Step-by-Step Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/SamDeveloper1/prototype.git
cd prototype
```

---

### 2. Backend Setup (FastAPI + AI Models)

Open a terminal in the project root folder:

#### On macOS / Linux:
```bash
# 1. Create a virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt
```

#### On Windows (PowerShell):
```powershell
# 1. Create a virtual environment
python -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Install Python dependencies
pip install -r requirements.txt
```

---

### 3. Frontend Setup (Next.js Broadsheet UI)

Open a second terminal (or navigate into the `web/` folder):

```bash
cd web

# Install Node.js dependencies
npm install
```

---

## 🏃‍♂️ How to Run the Application

### Option A: One-Command Launcher (macOS / Linux)
In the project root folder, simply run:
```bash
./run_app.sh
```
*(This automatically launches FastAPI on `:8000` and Next.js on `:3000` concurrently).*

---

### Option B: Manual Two-Terminal Run (Windows & All Platforms)

#### Terminal 1 — Backend (FastAPI):
```bash
# Ensure virtual environment is activated
python main.py
```
* Backend starts at: **`http://localhost:8000`**
* Interactive Swagger API Docs: **`http://localhost:8000/docs`**

#### Terminal 2 — Frontend (Next.js):
```bash
cd web
npm run dev
```
* Frontend starts at: **`http://localhost:3000`**

Open **`http://localhost:3000`** in your web browser to use the application!

---

## 📦 What is Pushed to GitHub vs. What Must Be Sent Separately?

### What is ALREADY in GitHub (Pushed automatically):
1. **Full Next.js 14 Frontend**: All broadsheet components, navigation, rubber stamp animations, and styles.
2. **FastAPI Backend & Controllers**: Input scrapers, Whisper media processor, and endpoints.
3. **All Clean Datasets**: 10,000 Fake News samples and 10,000 Hate Speech samples with 80/10/10 train/val/test splits in `data/splits/`.
4. **All Classical ML Models**: `fake_news_best_model.joblib` (Linear SVM, 93.0% F1) and `hate_speech_best_model.joblib` in `models/`.
5. **BiLSTM Weights**: Saved under `models/deep_learning/**/bilstm/`.

---

### ⚠️ What MUST be sent separately (Cannot be pushed to GitHub):

GitHub has a **strict 100 MB per-file limit** and automatically rejects any push containing files larger than 100 MB. 

Because fine-tuned BERT models are **~438 MB each**, they are ignored by `.gitignore` and **must be shared via Google Drive or Hugging Face**:

| Missing File | Size | Exact Folder Location to Paste Into |
| :--- | :---: | :--- |
| **`model.safetensors`** *(Fake News BERT)* | **438 MB** | `models/deep_learning/fakenews/bert-base-uncased/best_model/model.safetensors` |
| **`model.safetensors`** *(Hate Speech BERT)* | **438 MB** | `models/deep_learning/hatespeech/bert-base-uncased/best_model/model.safetensors` |

> [!NOTE]
> **Graceful Fallback Built-In**:  
> If someone clones the repository **without** downloading these two 438 MB BERT files, the backend **does not crash**. It automatically falls back to the high-accuracy Linear SVM baseline models (93.00% F1 on Fake News and 72.39% F1 on Hate Speech), meaning the system works out-of-the-box even without the large weights!

---

## 🧪 API Endpoints Reference

| Method | Route | Description |
| :--- | :--- | :--- |
| `POST` | `/predict_fakenews` | Accepts `{ "text": "..." }` or `{ "url": "https://..." }`. Scrapes web link and returns Real/Fake verdict + confidence. |
| `POST` | `/predict_hatespeech` | Accepts `{ "text": "..." }`. Returns Safe/Hostile verdict + confidence. |
| `POST` | `/predict_hatespeech_media` | Accepts `multipart/form-data` audio (`.mp3`, `.wav`) or video (`.mp4`, `.mov`). Transcribes speech via Whisper and predicts toxicity. |
| `GET` | `/health` | Healthcheck and active model status. |
| `GET` | `/docs` | Interactive Swagger documentation. |
