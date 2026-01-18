#!/bin/bash

echo "🚀 Auth Service - Quick Start"
echo "=============================="
echo ""

# Check if docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start infrastructure
echo "📦 Starting PostgreSQL and Redis..."
docker-compose up -d

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until docker exec auth_postgres pg_isready -U k_service_auth -d auth_service_db > /dev/null 2>&1; do
    sleep 1
done
echo "✅ PostgreSQL is ready"

# Wait for Redis to be ready
echo "⏳ Waiting for Redis to be ready..."
until docker exec auth_redis redis-cli -a ksauth ping > /dev/null 2>&1; do
    sleep 1
done
echo "✅ Redis is ready"

echo ""
echo "📊 Creating database tables..."
poetry run python -m scripts.init_db

echo ""
echo "🌱 Seeding initial data..."
poetry run python -m scripts.seed_database

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎉 You can now start the application:"
echo "   poetry run uvicorn app.main:app --reload"
echo ""
echo "📚 API Docs: http://localhost:8000/docs"
echo "🏥 Health: http://localhost:8000/health"
