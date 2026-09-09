#!/usr/bin/env bash
# =====================================================================
# THE VERITAS CHRONICLE: UNIFIED FULL STACK LAUNCHER
# =====================================================================
# Runs FastAPI Backend (Port 8000) and Next.js Frontend (Port 3000)
# Press CTRL+C to cleanly terminate both servers.
# =====================================================================

set -e

# Change to script directory
cd "$(dirname "$0")"

echo ""
echo "================================================================="
echo "  THE VERITAS CHRONICLE: LAUNCHING PROTOTYPE"
echo "  Backend:  http://localhost:8000 (FastAPI + BERT + Whisper)"
echo "  Frontend: http://localhost:3000 (Next.js 14 Broadsheet)"
echo "================================================================="
echo ""

# Handle clean exit
trap 'kill $(jobs -p) 2>/dev/null || true' EXIT SIGINT SIGTERM

# Start FastAPI Backend
echo "[1/2] Starting FastAPI Backend on :8000..."
/opt/anaconda3/bin/python main.py &

# Wait for backend to initialize
sleep 4

# Start Next.js Frontend
echo "[2/2] Starting Next.js Broadsheet Frontend on :3000..."
cd web
npm run dev
