from app.domain.authorization.ServiceAccess import ServiceAccess
from app.infrastructure.config.database.persistence.ServiceAccessModel import ServiceAccessModel


class ServiceAccessMapper:
    @staticmethod
    def to_domain(model: ServiceAccessModel) -> ServiceAccess:
        return ServiceAccess(
            id=model.id,
            user_id=model.user_id,
            service_name=model.service_name,
            is_allowed=model.is_allowed,
            allowed_features=model.allowed_features,
            granted_at=model.granted_at,
            revoked_at=model.revoked_at,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_persistence(domain: ServiceAccess) -> ServiceAccessModel:
        return ServiceAccessModel(
            id=domain.id,
            user_id=domain.user_id,
            service_name=domain.service_name,
            is_allowed=domain.is_allowed,
            allowed_features=domain.allowed_features,
            granted_at=domain.granted_at,
            revoked_at=domain.revoked_at,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
