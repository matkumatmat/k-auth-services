export ENVIRONMENT=production
poetry run python -m uvicorn app.main:app --reload
