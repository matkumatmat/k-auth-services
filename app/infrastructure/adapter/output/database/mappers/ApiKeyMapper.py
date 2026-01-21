from app.domain.authorization.ApiKey import ApiKey
from app.infrastructure.config.database.persistence.ApiKeyModel import ApiKeyModel


class ApiKeyMapper:
    @staticmethod
    def to_domain(model: ApiKeyModel) -> ApiKey:
        return ApiKey(
            id=model.id,
            user_id=model.user_id,
            key_hash=model.key_hash,
            name=model.name,
            scopes=model.scopes,
            expires_at=model.expires_at,
            last_used_at=model.last_used_at,
            is_active=model.is_active,
            created_at=model.created_at,
        )

    @staticmethod
    def to_persistence(domain: ApiKey) -> ApiKeyModel:
        return ApiKeyModel(
            id=domain.id,
            user_id=domain.user_id,
            key_hash=domain.key_hash,
            name=domain.name,
            scopes=domain.scopes,
            expires_at=domain.expires_at,
            last_used_at=domain.last_used_at,
            is_active=domain.is_active,
            created_at=domain.created_at,
        )
