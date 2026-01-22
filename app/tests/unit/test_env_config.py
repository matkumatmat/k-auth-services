import os
import pytest
from pydantic import ValidationError

from app.infrastructure.config.EnvConfig import EnvConfig


class TestEnvConfigValidation:
    def test_missing_jwt_secret_raises_validation_error(self, monkeypatch):
        monkeypatch.delenv("JWT_SECRET", raising=False)
        monkeypatch.delenv("PASSWORD_SALT", raising=False)
        monkeypatch.setenv("PASSWORD_SALT", "some-salt")

        with pytest.raises(ValidationError) as exc_info:
            EnvConfig.load(env_file="/dev/null")

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("jwt_secret",) for error in errors)

    def test_missing_password_salt_raises_validation_error(self, monkeypatch):
        monkeypatch.delenv("JWT_SECRET", raising=False)
        monkeypatch.delenv("PASSWORD_SALT", raising=False)
        monkeypatch.setenv("JWT_SECRET", "some-secret")

        with pytest.raises(ValidationError) as exc_info:
            EnvConfig.load(env_file="/dev/null")

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("password_salt",) for error in errors)

    def test_missing_both_required_fields_raises_validation_error(self, monkeypatch):
        monkeypatch.delenv("JWT_SECRET", raising=False)
        monkeypatch.delenv("PASSWORD_SALT", raising=False)

        with pytest.raises(ValidationError) as exc_info:
            EnvConfig.load(env_file="/dev/null")

        errors = exc_info.value.errors()
        error_fields = {error["loc"][0] for error in errors}
        assert "jwt_secret" in error_fields
        assert "password_salt" in error_fields

    def test_invalid_pool_size_raises_validation_error(self, monkeypatch):
        monkeypatch.setenv("JWT_SECRET", "test-secret")
        monkeypatch.setenv("PASSWORD_SALT", "test-salt")
        monkeypatch.setenv("DB_POOL_SIZE", "0")

        with pytest.raises(ValidationError) as exc_info:
            EnvConfig.load(env_file="/dev/null")

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("db_pool_size",) for error in errors)

    def test_valid_config_loads_successfully(self, monkeypatch):
        monkeypatch.setenv("JWT_SECRET", "test-secret-key-12345678")
        monkeypatch.setenv("PASSWORD_SALT", "test-salt-12345678")
        monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost:5432/testdb")
        monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")

        config = EnvConfig.load(env_file="/dev/null")

        assert config.auth.jwt_secret == "test-secret-key-12345678"
        assert config.auth.password_salt == "test-salt-12345678"
        assert "postgresql+asyncpg://" in config.database.url
        assert "redis://" in config.redis.url

    def test_database_url_validation(self, monkeypatch):
        monkeypatch.setenv("JWT_SECRET", "test-secret")
        monkeypatch.setenv("PASSWORD_SALT", "test-salt")
        monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://testuser:testpass@testhost:5432/testdb")

        config = EnvConfig.load(env_file="/dev/null")

        assert config.database.url == "postgresql+asyncpg://testuser:testpass@testhost:5432/testdb"
        assert config.database.pool_size == 20
        assert config.database.max_overflow == 10

    def test_redis_url_validation(self, monkeypatch):
        monkeypatch.setenv("JWT_SECRET", "test-secret")
        monkeypatch.setenv("PASSWORD_SALT", "test-salt")
        monkeypatch.setenv("REDIS_URL", "redis://:password@redishost:6379/1")

        config = EnvConfig.load(env_file="/dev/null")

        assert "redis://" in config.redis.url
        assert config.redis.pool_size == 10
        assert config.redis.max_connections == 50

    def test_auth_config_defaults(self, monkeypatch):
        monkeypatch.setenv("JWT_SECRET", "test-secret")
        monkeypatch.setenv("PASSWORD_SALT", "test-salt")

        config = EnvConfig.load(env_file="/dev/null")

        assert config.auth.jwt_algorithm == "HS256"
        assert config.auth.access_token_expiry_hours == 1
        assert config.auth.refresh_token_expiry_days == 7
        assert config.auth.otp_expiry_seconds == 300
        assert config.auth.otp_code_length == 6

    def test_custom_auth_config(self, monkeypatch):
        monkeypatch.setenv("JWT_SECRET", "custom-secret")
        monkeypatch.setenv("PASSWORD_SALT", "custom-salt")
        monkeypatch.setenv("JWT_ALGORITHM", "HS512")
        monkeypatch.setenv("ACCESS_TOKEN_EXPIRY_HOURS", "24")
        monkeypatch.setenv("OTP_CODE_LENGTH", "8")

        config = EnvConfig.load(env_file="/dev/null")

        assert config.auth.jwt_algorithm == "HS512"
        assert config.auth.access_token_expiry_hours == 24
        assert config.auth.otp_code_length == 8

    def test_environment_specific_loading(self, monkeypatch):
        monkeypatch.setenv("ENVIRONMENT", "development")

        config = EnvConfig.load()

        assert config.environment == "development"
        assert config.auth.jwt_secret is not None
        assert config.auth.password_salt is not None

    def test_debug_flags(self, monkeypatch):
        monkeypatch.setenv("JWT_SECRET", "test-secret")
        monkeypatch.setenv("PASSWORD_SALT", "test-salt")
        monkeypatch.setenv("DEBUG", "true")
        monkeypatch.setenv("DEBUG_OTP", "true")

        config = EnvConfig.load(env_file="/dev/null")

        assert config.debug is True
        assert config.debug_otp is True
