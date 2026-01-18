# AUTH SERVICE - DEPLOYMENT GUIDE
**Complete guide to deploy and run the authentication service**

---

## QUICK START (Development)

### 1. Prerequisites

```bash
# System requirements
- Python 3.13+
- Docker & Docker Compose
- Poetry (Python dependency manager)
```

### 2. Install Dependencies

```bash
# Navigate to project root
cd /home/k/pythonic/py3_13/auth-app

# Install dependencies with Poetry
poetry install

# Activate virtual environment
poetry shell
```

### 3. Start Infrastructure (PostgreSQL + Redis)

```bash
# Start Docker containers
docker-compose up -d

# Verify containers are running
docker ps
```

Expected output:
- `auth_postgres` on port 5432
- `auth_redis` on port 6379

### 4. Initialize Database

```bash
# Run Alembic migrations (creates all tables)
poetry run alembic upgrade head

# Seed initial data (plans + services)
poetry run python -m scripts.seed_database
```

### 5. Run Application

```bash
# Development mode (with auto-reload)
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using python directly
poetry run python -m app.main
```

Application will be available at:
- **API:** http://localhost:8000
- **Docs:** http://localhost:8000/docs
- **Health:** http://localhost:8000/health

---

## DATABASE SETUP

### Alembic Migration Commands

```bash
# Create new migration
poetry run alembic revision --autogenerate -m "description"

# Apply migrations
poetry run alembic upgrade head

# Rollback one migration
poetry run alembic downgrade -1

# Show current migration
poetry run alembic current

# Show migration history
poetry run alembic history
```

### Database Seeding

The seed script creates:
- **4 Plans:** Anonym, Free, Pro, Enterprise
- **4 Services:** cvmaker, jobportal, 3dbinpacking, media_information

```bash
# Run seed script
poetry run python -m scripts.seed_database

# Verify seeding
poetry run python -m scripts.verify_seeds
```

---

## CONFIGURATION

### Environment Variables

Configuration loaded from `env/.env.development` or `env/.env.production`

**Critical Variables (MUST CHANGE in Production):**
```bash
# Security
JWT_SECRET=CHANGE_ME_IN_PRODUCTION_USE_STRONG_SECRET
PASSWORD_SALT=CHANGE_ME_IN_PRODUCTION_USE_STRONG_SALT

# Database
DB_PASSWORD=CHANGE_ME_IN_PRODUCTION

# Redis
REDIS_PASSWORD=CHANGE_ME_IN_PRODUCTION
```

### Switching Environments

```bash
# Development (default)
export ENVIRONMENT=development

# Production
export ENVIRONMENT=production
```

---

## API ENDPOINTS

### Authentication Endpoints

```bash
POST /api/v1/auth/register/email
POST /api/v1/auth/register/phone
POST /api/v1/auth/login/email
POST /api/v1/auth/login/phone
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
```

### Validation Endpoints (for Microservices)

```bash
POST /api/v1/validate/token
POST /api/v1/validate/service-access
POST /api/v1/validate/quota/check
POST /api/v1/validate/quota/consume
```

### User Endpoints

```bash
POST /api/v1/user/verify/email
POST /api/v1/user/verify/phone
GET  /api/v1/user/services/{user_id}
```

---

## TESTING

### Quick API Test

```bash
# Register new user
curl -X POST http://localhost:8000/api/v1/auth/register/email \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'

# Health check
curl http://localhost:8000/health
```

### Run Tests (when implemented)

```bash
# Unit tests
poetry run pytest tests/unit

# Integration tests
poetry run pytest tests/integration

# All tests
poetry run pytest
```

---

## PRODUCTION DEPLOYMENT

### 1. Prepare Environment

```bash
# Update env/.env.production with production values
# CRITICAL: Change all secrets!

# Set environment
export ENVIRONMENT=production
```

### 2. Database Setup

```bash
# Run migrations on production database
poetry run alembic upgrade head

# Seed initial data
poetry run python -m scripts.seed_database
```

### 3. Run with Gunicorn (Production Server)

```bash
# Install gunicorn
poetry add gunicorn

# Run with Gunicorn + Uvicorn workers
poetry run gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### 4. Docker Deployment (Recommended)

```bash
# Build Docker image
docker build -t auth-service:1.0.0 .

# Run container
docker run -d \
  --name auth-service \
  -p 8000:8000 \
  --env-file env/.env.production \
  auth-service:1.0.0
```

---

## TROUBLESHOOTING

### Database Connection Error

```bash
# Check PostgreSQL is running
docker logs auth_postgres

# Test connection
docker exec -it auth_postgres psql -U postgres -d auth_db -c "SELECT 1"
```

### Redis Connection Error

```bash
# Check Redis is running
docker logs auth_redis

# Test connection
docker exec -it auth_redis redis-cli ping
```

### Import Errors

```bash
# Ensure virtual environment is activated
poetry shell

# Reinstall dependencies
poetry install --no-cache
```

### Migration Errors

```bash
# Reset database (CAUTION: Deletes all data)
docker-compose down -v
docker-compose up -d
poetry run alembic upgrade head
```

---

## MONITORING & LOGS

### Application Logs

```bash
# View logs in real-time
tail -f logs/app.log

# Search for errors
grep ERROR logs/app.log
```

### Database Logs

```bash
# PostgreSQL logs
docker logs auth_postgres --tail 100 -f

# Redis logs
docker logs auth_redis --tail 100 -f
```

---

## SECURITY CHECKLIST

- [ ] Changed JWT_SECRET in production
- [ ] Changed PASSWORD_SALT in production
- [ ] Changed database passwords
- [ ] Disabled debug mode in production
- [ ] Configured CORS origins (not allow_origins=["*"])
- [ ] Enabled HTTPS/TLS
- [ ] Setup rate limiting
- [ ] Regular security updates
- [ ] Monitor transaction logs

---

## ARCHITECTURE SUMMARY

**Layer Structure:**
```
app/
├── domain/              # Business entities (User, Session, etc.)
├── application/
│   ├── port/           # Interfaces (contracts)
│   └── service/        # Business logic
├── infrastructure/
│   ├── adapter/
│   │   ├── input/      # Controllers, middleware
│   │   └── output/     # Repositories, mappers
│   └── config/         # Database, Redis, DI
├── shared/             # Custom modules (UUID, DateTime, Crypto)
└── main.py             # FastAPI application

