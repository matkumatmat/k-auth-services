import os
import pytest

from app.infrastructure.config.EnvConfig import EnvConfig


class TestEnvConfigLoading:
    def test_development_env_loads_successfully(self):
        config = EnvConfig.load(env_file="env/.env.development")

        assert config.environment == "development"
        assert config.debug is True
        assert config.debug_otp is True

        assert config.auth.jwt_secret is not None
        assert config.auth.password_salt is not None
        assert len(config.auth.jwt_secret) > 10
        assert len(config.auth.password_salt) > 10

        assert "postgresql+asyncpg://" in config.database.url
        assert "k_service_auth" in config.database.url
        assert "auth_service_db" in config.database.url
        assert config.database.pool_size == 20
        assert config.database.max_overflow == 10
        assert config.database.pool_recycle == 3600
        assert config.database.echo is False

        assert "redis://" in config.redis.url
        assert config.redis.pool_size == 10
        assert config.redis.max_connections == 50
        assert config.redis.decode_responses is True

    def test_production_env_has_required_secrets(self):
        config = EnvConfig.load(env_file="env/.env.production")

        assert config.environment == "production"
        assert config.debug is False
        assert config.debug_otp is False

        assert config.auth.jwt_secret is not None
        assert config.auth.password_salt is not None

        assert "postgresql+asyncpg://" in config.database.url
        assert "redis://" in config.redis.url

    def test_database_url_format(self):
        config = EnvConfig.load(env_file="env/.env.development")

        db_url = config.database.url
        assert db_url.startswith("postgresql+asyncpg://")
        assert "@" in db_url
        assert ":" in db_url
        assert "/" in db_url

    def test_redis_url_format(self):
        config = EnvConfig.load(env_file="env/.env.development")

        redis_url = config.redis.url
        assert redis_url.startswith("redis://")
        assert "@localhost" in redis_url or "localhost" in redis_url

    def test_auth_config_values(self):
        config = EnvConfig.load(env_file="env/.env.development")

        assert config.auth.jwt_algorithm == "HS256"
        assert config.auth.access_token_expiry_hours == 1
        assert config.auth.refresh_token_expiry_days == 7
        assert config.auth.otp_expiry_seconds == 300
        assert config.auth.otp_code_length == 6

    def test_pool_configuration(self):
        config = EnvConfig.load(env_file="env/.env.development")

        assert config.database.pool_size >= 1
        assert config.database.max_overflow >= 0
        assert config.database.pool_recycle > 0

        assert config.redis.pool_size >= 1
        assert config.redis.max_connections >= config.redis.pool_size

    def test_environment_variable_override(self, monkeypatch):
        monkeypatch.setenv("JWT_SECRET", "override-secret-12345678")
        monkeypatch.setenv("PASSWORD_SALT", "override-salt-12345678")
        monkeypatch.setenv("DB_POOL_SIZE", "50")

        config = EnvConfig.load(env_file="env/.env.development")

        assert config.auth.jwt_secret == "override-secret-12345678"
        assert config.auth.password_salt == "override-salt-12345678"
        assert config.database.pool_size == 50

    def test_computed_fields_are_dataclasses(self):
        config = EnvConfig.load(env_file="env/.env.development")

        assert hasattr(config.database, "url")
        assert hasattr(config.database, "pool_size")
        assert hasattr(config.redis, "url")
        assert hasattr(config.redis, "pool_size")
        assert hasattr(config.auth, "jwt_secret")
        assert hasattr(config.auth, "password_salt")
