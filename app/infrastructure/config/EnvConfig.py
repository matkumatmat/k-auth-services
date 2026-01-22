from dataclasses import dataclass

from pydantic import Field, PostgresDsn, RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


@dataclass
class DatabaseConfig:
    url: str
    pool_size: int
    max_overflow: int
    pool_recycle: int
    echo: bool


@dataclass
class RedisConfig:
    url: str
    pool_size: int
    max_connections: int
    decode_responses: bool


@dataclass
class AuthConfig:
    jwt_secret: str
    jwt_algorithm: str
    access_token_expiry_hours: int
    refresh_token_expiry_days: int
    password_salt: str
    otp_expiry_seconds: int
    otp_code_length: int


class EnvConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    environment: str = "production"
    debug: bool = False
    debug_otp: bool = True

    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/auth_db",
        description="PostgreSQL connection URL"
    )
    db_pool_size: int = Field(default=20, ge=1)
    db_max_overflow: int = 10
    db_pool_recycle: int = 3600
    db_echo: bool = False

    redis_url: RedisDsn = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    redis_pool_size: int = 10
    redis_max_connections: int = 50
    redis_decode_responses: bool = True

    jwt_secret: str = Field(..., description="JWT secret key - REQUIRED")
    jwt_algorithm: str = "HS256"
    access_token_expiry_hours: int = 1
    refresh_token_expiry_days: int = 7
    password_salt: str = Field(..., description="Password hashing salt - REQUIRED")
    otp_expiry_seconds: int = 300
    otp_code_length: int = 6

    @computed_field
    @property
    def database(self) -> DatabaseConfig:
        return DatabaseConfig(
            url=str(self.database_url),
            pool_size=self.db_pool_size,
            max_overflow=self.db_max_overflow,
            pool_recycle=self.db_pool_recycle,
            echo=self.db_echo
        )

    @computed_field
    @property
    def redis(self) -> RedisConfig:
        return RedisConfig(
            url=str(self.redis_url),
            pool_size=self.redis_pool_size,
            max_connections=self.redis_max_connections,
            decode_responses=self.redis_decode_responses
        )

    @computed_field
    @property
    def auth(self) -> AuthConfig:
        return AuthConfig(
            jwt_secret=self.jwt_secret,
            jwt_algorithm=self.jwt_algorithm,
            access_token_expiry_hours=self.access_token_expiry_hours,
            refresh_token_expiry_days=self.refresh_token_expiry_days,
            password_salt=self.password_salt,
            otp_expiry_seconds=self.otp_expiry_seconds,
            otp_code_length=self.otp_code_length
        )

    @classmethod
    def load(cls, env_file: str | None = None) -> "EnvConfig":
        import os
        if env_file is None:
            environment = os.getenv("ENVIRONMENT", "production")
            env_file = f"env/.env.{environment}"

        return cls(_env_file=env_file)
