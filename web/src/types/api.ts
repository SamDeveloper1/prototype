/**
 * API Response and Request Types
 * ==============================
 * Maps directly to FastAPI backend schemas in sec_prototype/main.py
 */

export interface FakeNewsResponse {
  status: "success" | "error";
  verdict: "Real News" | "Fake News";
  confidence_score: number;
  model_used?: string;
  input_type: "text" | "url";
  headline_analyzed: string;
  preview_text: string;
  inference_time_ms: number;
}

export interface HateSpeechResponse {
  status: "success" | "error";
  verdict: "Safe / Non-Hate" | "Hate Speech / Hostile";
  confidence_score: number;
  model_used?: string;
  input_type: "text" | "url" | "audio" | "video";
  preview_text: string;
  transcribed_text?: string;
  inference_time_ms: number;
}

export interface HealthResponse {
  status: string;
  models: {
    fake_news: string;
    hate_speech: string;
    audio_transcription: string;
  };
}
