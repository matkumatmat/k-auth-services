from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, RedisDsn, Field, computed_field

CURRENT_FILE = Path(__file__).resolve()
APP_ROOT = CURRENT_FILE.parent.parent.parent.parent
ENV_DEV_FILE_PATH = APP_ROOT / "env" / ".env.development"
ENV_PROD_FILE_PATH = APP_ROOT / "env" / ".env.production"

class Settings(BaseSettings):
    app_name : str = "k-auth-service"
    environtment : str = Field(default="development")
    debug : bool = Field(default=True)

    database_url : PostgresDsn
    database_pool_size : int = 10
    database_max_overflow : int = 20

    redis_url : RedisDsn
    redis_session_db : int = 0
    redis_cache_db : int = 1

    jwt_secret_key : str
    jwt_algorithm : str = "HS256"
    jwt_access_token_expire_minutes : int = 15
    jwt_refresh_token_expire_days: int = 7

    encryption_key : str
    salt_secret : str

    oauth2_google_client_id : str | None = None
    oauth2_google_client_secret : str | None = None
    oauth2_google_client_redirect_url : str | None = None

    twilio_account_sid : str | None = None
    twilio_auth_token : str | None = None
    twilio_whatsapp_from : str | None = None

    server_host : str = "0.0.0.0"
    server_port : int = 8000
    server_workers : int = 2
    server_log_level : str = "debug"

    cors_allowed_origins : str = "*"
    cors_allow_credentials : bool = True

    @computed_field
    @property
    def cors_origins_list(self) -> list[str]:
        if not self.cors_allowed_origins:
            return []
        return [origin.strip() for origin in self.cors_allowed_origins.split(",")]
    model_config = SettingsConfigDict(
        env_file = ENV_DEV_FILE_PATH,
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

settings = Settings()


