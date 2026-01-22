from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.adapter.input.http.AuthController import router as auth_router
from app.infrastructure.adapter.input.http.OtpController import router as otp_router
from app.infrastructure.adapter.input.http.UserController import router as user_router
from app.infrastructure.adapter.input.http.ValidationController import router as validation_router
from app.infrastructure.adapter.input.middleware.ExceptionHandler import (
    database_exception_handler,
    domain_exception_handler,
    generic_exception_handler
)
from app.infrastructure.adapter.input.middleware.LoggingMiddleware import LoggingMiddleware
from app.infrastructure.config.EnvConfig import EnvConfig
from app.infrastructure.dependencies import db_factory, redis_client
from app.domain.exceptions import DomainException
from app.domain.ServerConfig import ServerConfig
from app.shared.Exceptions import DatabaseException

config = EnvConfig.load()
env = ServerConfig(environtment=config.environment).is_production()

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
    docs_url="/docs" if env is False else None,
    redoc_url="/redoc" if env is False else None,
    openapi_url="/openapi.json" if env is False else None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if config.debug else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(DatabaseException, database_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(validation_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(otp_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    if env:
        return {"status": "healthy"}

    return {
        "status": "healthy",
        "environment": env,
        "debug": config.debug
    }


if env is False:
    @app.get("/")
    async def root():
        return {
            "message": "Auth Service API",
            "version": "1.0.0",
            "docs": "/docs"
        }


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.debug
    )
