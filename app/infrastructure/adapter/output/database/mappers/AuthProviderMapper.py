from app.domain.AuthProvider import AuthProvider
from app.domain.ValueObjects import AuthProviderType
from app.infrastructure.config.database.persistence.AuthProviderModel import AuthProviderModel


class AuthProviderMapper:
    @staticmethod
    def to_domain(model: AuthProviderModel) -> AuthProvider:
        return AuthProvider(
            id=model.id,
            user_id=model.user_id,
            provider_type=AuthProviderType(model.provider_type),
            provider_user_id=model.provider_user_id,
            is_primary=model.is_primary,
            provider_metadata=model.provider_metadata or {},
            created_at=model.created_at
        )

    @staticmethod
    def to_persistence(domain: AuthProvider) -> AuthProviderModel:
        return AuthProviderModel(
            id=domain.id,
            user_id=domain.user_id,
            provider_type=domain.provider_type.value,
            provider_user_id=domain.provider_user_id,
            is_primary=domain.is_primary,
            provider_metadata=domain.provider_metadata,
            created_at=domain.created_at
        )
