# Deep Learning Collaboration Guide (NVIDIA RTX 3050 4GB)
**Project**: Final Year B.Tech — Indian Context Fake News & Hate Speech Detection System  
**Hardware Profile**: NVIDIA GeForce RTX 3050 (4GB VRAM) on Windows / Linux  
**Repository**: `https://github.com/SamDeveloper1/prototype.git`

---

## 📌 Executive Summary for the DL Teammate

* All **data engineering, scraping, cleaning, zero-curse filtering, and 80/10/10 stratified train/val/test splits** are already completed and present in `data/splits/`.
* Classical ML baselines are already benchmarked (Linear SVM scores **93.0% F1** on Fake News, and **72.4% F1** on Hate Speech).
* **Your Objective**: Train Deep Learning Transformer models (`microsoft/deberta-v3-small`, `roberta-base`, or `ai4bharat/indic-bert`) to see if contextual embeddings beat classical ML (especially on Hate Speech nuance) and record the test metrics for our final project report.

---

## ⚡ Hardware Constraints & Safe Config (4GB VRAM)

| Parameter | Recommended Value | Why? |
| :--- | :---: | :--- |
| **Precision** | `fp16=True` | Halves VRAM consumption on RTX 3050 Tensor Cores. |
| **Per-Device Batch Size** | `8` | Fits safely inside 4GB without `CUDA OutOfMemoryError`. |
| **Gradient Accumulation** | `2` | Simulates an effective batch size of **16** (`8 x 2`). |
| **Max Sequence Length** | `256` tokens | 512 tokens causes quadratic attention OOM on 4GB. |
| **Recommended Models** | `microsoft/deberta-v3-small`<br>`roberta-base`<br>`ai4bharat/indic-bert` | Fast, fits within 4GB, excellent accuracy. |

---

## 🛠️ Step 1: Environment Setup on RTX 3050 Machine

### 1. Clone the repository and switch to a new branch:
```bash
git clone https://github.com/SamDeveloper1/prototype.git
cd prototype
git checkout -b feat/dl-transformers
```

### 2. Create and activate a Python virtual environment:
**Windows (PowerShell):**
```powershell
python -m venv venv_gpu
.\venv_gpu\Scripts\Activate.ps1
```

**Linux / WSL:**
```bash
python3 -m venv venv_gpu
source venv_gpu/bin/activate
```

### 3. Install PyTorch with CUDA 12.1 support:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 4. Install project dependencies:
```bash
pip install -r requirements-gpu.txt
```

### 5. Verify CUDA is active on your RTX 3050:
```bash
python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
```
*(Should output: `CUDA Available: True`, `Device: NVIDIA GeForce RTX 3050`)*

---

## 🚀 Step 2: Training the Models

You have two easy ways to train:

### Option A: Command Line (Fastest & Headless)

#### Train Fake News Transformer:
```bash
python src/train_dl_models.py --task fakenews --model_name microsoft/deberta-v3-small --epochs 3 --batch_size 8 --grad_accum 2 --max_length 256
```

#### Train Hate Speech Transformer:
```bash
python src/train_dl_models.py --task hatespeech --model_name microsoft/deberta-v3-small --epochs 3 --batch_size 8 --grad_accum 2 --max_length 256
```

*To try RoBERTa, simply replace `--model_name microsoft/deberta-v3-small` with `--model_name roberta-base`.*

---

### Option B: Interactive Jupyter Notebook
Open Jupyter Notebook / VS Code:
```bash
jupyter notebook notebooks/train_deep_learning_gpu.ipynb
```
Run the cells sequentially. The notebook handles data loading, tokenization, training, confusion matrix plotting, and model saving automatically.

---

## 📦 Step 3: Model Outputs & Deliverables

After training finishes, the script/notebook outputs everything cleanly into:
`models/deep_learning/{task}/{model_name}/`
- `best_model/`: Checkpoint files (`model.safetensors`, `config.json`, `tokenizer.json`).
- `dl_benchmark_results.json`: Accuracy, Precision, Recall, F1, and Confusion Matrix.
- `test_confusion_matrix.png`: High-resolution visual plot for our report slides.

### ⚠️ IMPORTANT: Large Model Weights Git Rule
Hugging Face model checkpoints (`model.safetensors` is ~400MB) are **ignored by `.gitignore`** so GitHub doesn't reject your push (>100MB limit).

**How to share the trained models:**
1. **Push your code, notebooks, and metric results to GitHub:**
   ```bash
   git add notebooks/ src/ models/deep_learning/
   git commit -m "feat(dl): train deberta-v3-small on RTX 3050 with benchmark results"
   git push origin feat/dl-transformers
   ```
2. **For the heavy `best_model/` weights folder (~400MB):**
   - Upload the folder to Google Drive / OneDrive and share the link, OR
   - (Optional) Push directly to Hugging Face Hub (`model.push_to_hub("SamDeveloper1/fake-news-deberta")`).

---

## 🤖 Prompt for the Teammate's AI Coding Assistant

If you are using ChatGPT, Claude, or Antigravity CLI on your machine, paste this exact prompt into your chat:

```text
I am working on my B.Tech final year project (Indian Context Fake News and Hate Speech Detection).
I have cloned the repository 'prototype' and have an NVIDIA GeForce RTX 3050 with 4GB VRAM.
The repository already contains:
1. 10,000-row stratified datasets in `data/splits/` (train.csv, val.csv, test.csv for Fake News; hate_train.csv, hate_val.csv, hate_test.csv for Hate Speech).
2. GPU requirements in `requirements-gpu.txt`.
3. Training script in `src/train_dl_models.py` and notebook in `notebooks/train_deep_learning_gpu.ipynb`.

My task is to fine-tune transformer models (e.g. microsoft/deberta-v3-small or roberta-base) on both tasks using PyTorch and Hugging Face Transformers.
Because I have 4GB VRAM, please ensure all training uses:
- Mixed precision FP16 (fp16=True)
- Batch size = 8 with Gradient Accumulation = 2 (effective batch size 16)
- Max sequence length = 256
- Best model saved at the end based on F1-score.

Please guide me through running the training script, tracking VRAM, evaluating on the unseen test set, and exporting the benchmark metrics to `models/deep_learning/`.
```
