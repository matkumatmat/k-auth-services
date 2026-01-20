import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DatabaseConfig:
    host: str
    port: int
    user: str
    password: str
    database: str
    pool_size: int
    max_overflow: int
    pool_recycle: int
    echo: bool

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class RedisConfig:
    host: str
    port: int
    db: int
    password: str | None
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


@dataclass
class EnvConfig:
    environment: str
    debug: bool
    debug_otp: bool
    database: DatabaseConfig
    redis: RedisConfig
    auth: AuthConfig

    @classmethod
    def load(cls, env_file: str | None = None) -> "EnvConfig":
        if env_file is None:
            environment = os.getenv("ENVIRONMENT", "development")
            env_file = f"env/.env.{environment}"

        if Path(env_file).exists():
            from dotenv import load_dotenv
            load_dotenv(env_file)

        return cls(
            environment=os.getenv("ENVIRONMENT", "development"),
            debug=os.getenv("DEBUG", "False").lower() == "true",
            debug_otp=os.getenv("DEBUG_OTP", "False").lower() == "true",
            database=DatabaseConfig(
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", "5432")),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "postgres"),
                database=os.getenv("DB_NAME", "auth_db"),
                pool_size=int(os.getenv("DB_POOL_SIZE", "20")),
                max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
                pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "3600")),
                echo=os.getenv("DB_ECHO", "False").lower() == "true"
            ),
            redis=RedisConfig(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", "6379")),
                db=int(os.getenv("REDIS_DB", "0")),
                password=os.getenv("REDIS_PASSWORD"),
                pool_size=int(os.getenv("REDIS_POOL_SIZE", "10")),
                max_connections=int(os.getenv("REDIS_MAX_CONNECTIONS", "50")),
                decode_responses=os.getenv("REDIS_DECODE_RESPONSES", "True").lower() == "true"
            ),
            auth=AuthConfig(
                jwt_secret=os.getenv("JWT_SECRET", "change-me-in-production"),
                jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
                access_token_expiry_hours=int(os.getenv("ACCESS_TOKEN_EXPIRY_HOURS", "1")),
                refresh_token_expiry_days=int(os.getenv("REFRESH_TOKEN_EXPIRY_DAYS", "7")),
                password_salt=os.getenv("PASSWORD_SALT", "change-me-in-production"),
                otp_expiry_seconds=int(os.getenv("OTP_EXPIRY_SECONDS", "300")),
                otp_code_length=int(os.getenv("OTP_CODE_LENGTH", "6"))
            )
        )
