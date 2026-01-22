#!/bin/bash
export ENVIRONMENT=production
echo "Starting server in PRODUCTION mode..."
echo "Expected: JSON logs, no colors, no request body"
echo "=============================================="
poetry run python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
