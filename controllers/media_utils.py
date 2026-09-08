"""
Media Processing & Speech-to-Text Utilities
===========================================
Handles:
  1. Audio and Video file format validation
  2. Audio track extraction from video using ffmpeg
  3. Speech-to-text transcription using OpenAI Whisper (base model)
"""

import os
import shutil
import subprocess
import tempfile
import whisper
from fastapi import HTTPException

# File Extension sets
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac', '.wma'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.mkv', '.avi', '.webm', '.flv', '.wmv'}

# Global cached Whisper model instance
_whisper_model = None

def get_whisper_model():
    """Loads and caches the Whisper base model in memory."""
    global _whisper_model
    if _whisper_model is None:
        print("[Whisper] Loading Whisper base model into memory...")
        _whisper_model = whisper.load_model("base")
        print("[Whisper] Whisper base model ready.")
    return _whisper_model

def get_media_type(filename: str) -> str:
    """
    Determines whether a file is 'audio', 'video', or unsupported.
    Returns: 'audio' | 'video' | None
    """
    ext = os.path.splitext(filename.lower())[1]
    if ext in AUDIO_EXTENSIONS:
        return 'audio'
    if ext in VIDEO_EXTENSIONS:
        return 'video'
    return None

def extract_audio_from_video(video_path: str, output_audio_path: str):
    """
    Extracts audio track from video file using ffmpeg.
    Converts to 16kHz mono MP3 optimized for Whisper speech recognition.
    """
    # Find ffmpeg binary
    ffmpeg_bin = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
    if not os.path.exists(ffmpeg_bin):
        raise HTTPException(
            status_code=500,
            detail="ffmpeg is required for video processing but was not found on the server."
        )

    cmd = [
        ffmpeg_bin,
        "-y",               # Overwrite output
        "-i", video_path,   # Input video
        "-vn",              # Disable video recording
        "-acodec", "libmp3lame",
        "-ar", "16000",     # 16kHz audio sample rate
        "-ac", "1",         # Mono audio
        output_audio_path
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        err_msg = result.stderr.decode('utf-8', errors='ignore')
        raise HTTPException(
            status_code=400,
            detail=f"Failed to extract audio track from video. ffmpeg error: {err_msg[:200]}"
        )

def transcribe_media_file(file_path: str, is_video: bool = False) -> str:
    """
    Transcribes spoken speech from an audio or video file into English text.
    Returns: Clean transcribed string.
    """
    audio_target_path = file_path
    temp_audio_file = None

    try:
        # Step 1: If video, extract audio track first
        if is_video:
            temp_fd, temp_audio_file = tempfile.mkstemp(suffix=".mp3")
            os.close(temp_fd)
            extract_audio_from_video(file_path, temp_audio_file)
            audio_target_path = temp_audio_file

        # Step 2: Transcribe with Whisper
        model = get_whisper_model()
        # fp16=False ensures stability on CPU/Apple Silicon
        result = model.transcribe(audio_target_path, fp16=False, language="en")
        transcribed_text = (result.get("text") or "").strip()
        return transcribed_text

    finally:
        # Clean up temporary extracted audio file
        if temp_audio_file and os.path.exists(temp_audio_file):
            try:
                os.remove(temp_audio_file)
            except Exception:
                pass
