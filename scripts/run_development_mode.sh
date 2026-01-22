#!/bin/bash
export ENVIRONMENT=development
echo "Starting server in DEVELOPMENT mode..."
echo "Expected: Colorized logs, human-readable, request body shown"
echo "=============================================="
poetry run python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
