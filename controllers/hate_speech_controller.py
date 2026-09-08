"""
Hate Speech Controller
======================
Handles:
  1. Input validation (raw text or link/URL)
  2. URL scraping if web link received
  3. Preprocessing and TF-IDF transformation
  4. Model inference
  5. Returning verdict + confidence score
"""

import os
import time
import joblib
from typing import Optional, Dict, Any
from fastapi import HTTPException
from pydantic import BaseModel, Field
from controllers.scraper_utils import is_valid_url, scrape_url_content

# Model Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'hate_speech_tfidf_vectorizer.joblib')
MODEL_PATH = os.path.join(MODELS_DIR, 'hate_speech_best_model.joblib')

# In-memory cached model and vectorizer
_vectorizer = None
_model = None

def get_hate_speech_model():
    """Loads and caches model and vectorizer in memory."""
    global _vectorizer, _model
    if _vectorizer is None:
        if not os.path.exists(VECTORIZER_PATH):
            raise RuntimeError(f"Vectorizer file not found at: {VECTORIZER_PATH}")
        _vectorizer = joblib.load(VECTORIZER_PATH)
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(f"Model file not found at: {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
    return _vectorizer, _model

class HateSpeechInput(BaseModel):
    text: Optional[str] = Field(None, description="Raw social media comment, post, or tweet text")
    url: Optional[str] = Field(None, description="Web link/URL of post or comment thread to scrape")

def handle_hate_speech_prediction(payload: HateSpeechInput) -> Dict[str, Any]:
    """
    Validates input, processes text/link, executes inference,
    and returns verdict + confidence score.
    """
    t_start = time.time()
    raw_text = (payload.text or "").strip()
    raw_url = (payload.url or "").strip()

    # Step 1: Input Validation
    if not raw_text and not raw_url:
        raise HTTPException(
            status_code=422,
            detail="Validation Error: Please provide either 'text' or 'url' to analyze."
        )

    # Check if text is actually a URL
    if raw_text and is_valid_url(raw_text) and not raw_url:
        raw_url = raw_text
        raw_text = ""

    input_type = "url" if raw_url else "text"
    text_to_analyze = ""

    # Step 2: Handle Link vs. Raw Text
    if raw_url:
        headline, body = scrape_url_content(raw_url)
        text_to_analyze = f"{headline} {body}".strip()
    else:
        # Validate minimum length
        if len(raw_text) < 5:
            raise HTTPException(
                status_code=422,
                detail="Validation Error: Input text is too short. Please provide at least 5 characters."
            )
        text_to_analyze = raw_text

    # Step 3: Run Model Inference
    vectorizer, model = get_hate_speech_model()
    vec = vectorizer.transform([text_to_analyze])

    # Predict probabilities: [prob_safe (class 0), prob_hostile (class 1)]
    probabilities = model.predict_proba(vec)[0]
    prob_safe = float(probabilities[0])
    prob_hostile = float(probabilities[1])

    # Determine Verdict and Confidence Score
    if prob_hostile >= 0.5:
        verdict = "Hate Speech / Hostile"
        confidence_score = round(prob_hostile * 100, 2)
    else:
        verdict = "Safe / Non-Hate"
        confidence_score = round(prob_safe * 100, 2)

    inference_time = round((time.time() - t_start) * 1000, 2)

    # Step 4: Return Formatted Result
    return {
        "status": "success",
        "verdict": verdict,
        "confidence_score": confidence_score,
        "input_type": input_type,
        "preview_text": text_to_analyze[:300] + ("..." if len(text_to_analyze) > 300 else ""),
        "inference_time_ms": inference_time
    }
