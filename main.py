"""
FastAPI Main Application
========================
Routes:
  - POST /predict_fakenews   -> Handled by controllers/fake_news_controller.py
  - POST /predict_hatespeech -> Handled by controllers/hate_speech_controller.py
  - GET  /health             -> Healthcheck
  - GET  /                   -> Welcome & API Documentation link
"""

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.fake_news_controller import (
    FakeNewsInput,
    handle_fake_news_prediction,
    get_fake_news_model
)
from controllers.hate_speech_controller import (
    HateSpeechInput,
    handle_hate_speech_prediction,
    get_hate_speech_model
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Preloads ML models and vectorizers into memory at startup."""
    print("\n[Startup] Pre-loading ML models into memory...")
    try:
        get_fake_news_model()
        print("  ✓ Fake News Model & Vectorizer cached.")
        get_hate_speech_model()
        print("  ✓ Hate Speech Model & Vectorizer cached.")
        print("[Startup] All models ready for sub-millisecond inference!\n")
    except Exception as e:
        print(f"  ✗ Warning during model pre-loading: {e}")
    yield
    print("[Shutdown] Cleaning up API resources.")

app = FastAPI(
    title="AI Fake News & Hate Speech Detection System",
    description="Production-grade AI backend trained on 10,000 Indian News samples and 10,000 Hate Speech samples.",
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS for Next.js frontend (localhost:3000) and external clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "project": "Fake News & Hate Speech Detection System",
        "version": "2.0.0",
        "docs_url": "/docs",
        "endpoints": {
            "fake_news": "/predict_fakenews (POST)",
            "hate_speech": "/predict_hatespeech (POST)",
            "health": "/health (GET)"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "models": {
            "fake_news": "Linear SVM (93.00% F1)",
            "hate_speech": "Multinomial Naive Bayes (72.59% F1)"
        }
    }

@app.post("/predict_fakenews", summary="Detect Fake News from Raw Text or Web Link")
def predict_fakenews(payload: FakeNewsInput):
    """
    Analyzes input text or web link to classify whether it is Real News or Fake News.
    - If a URL/link is provided, the article headline and body are scraped automatically.
    - Returns verdict ('Real News' or 'Fake News') along with the confidence score.
    """
    return handle_fake_news_prediction(payload)

@app.post("/predict_hatespeech", summary="Detect Hate Speech from Raw Text or Web Link")
def predict_hatespeech(payload: HateSpeechInput):
    """
    Analyzes input comment, post, or web link to classify whether it contains Hate Speech / Hostility.
    - Returns verdict ('Safe / Non-Hate' or 'Hate Speech / Hostile') along with the confidence score.
    """
    return handle_hate_speech_prediction(payload)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
