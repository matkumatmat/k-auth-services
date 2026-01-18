from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.adapter.input.http.AuthController import router as auth_router
from app.infrastructure.adapter.input.http.UserController import router as user_router
from app.infrastructure.adapter.input.http.ValidationController import router as validation_router
from app.infrastructure.adapter.input.middleware.ExceptionHandler import (
    domain_exception_handler,
    generic_exception_handler
)
from app.infrastructure.config.EnvConfig import EnvConfig
from app.infrastructure.dependencies import db_factory, redis_client
from app.shared.Exceptions import DomainException

config = EnvConfig.load()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_factory.close()
    await redis_client.close()


app = FastAPI(
    title="Auth Service API",
    version="1.0.0",
    description="Scalable authentication service for multi-microservices architecture",
    debug=config.debug,
    docs_url="/docs" if config.debug else None,
    redoc_url="/redoc" if config.debug else None,
    openapi_url="/openapi.json" if config.debug else None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if config.debug else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(validation_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": config.environment,
        "debug": config.debug
    }


@app.get("/")
async def root():
    return {
        "message": "Auth Service API",
        "version": "1.0.0",
        "docs": "/docs" if config.debug else "disabled in production"
    }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.debug
    )
