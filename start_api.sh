#!/bin/bash
# Start the FastAPI server for the phishing detector extension

echo "Starting Phishing Detector API..."
echo "API will be available at: http://localhost:8001"
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
source venv/bin/activate
uvicorn src.api_fastapi:app --reload --port 8001
