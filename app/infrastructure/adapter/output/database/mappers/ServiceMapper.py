from app.domain.Service import Service
from app.infrastructure.config.database.persistence.ServiceModel import ServiceModel


class ServiceMapper:
    @staticmethod
    def to_domain(model: ServiceModel) -> Service:
        return Service(
            id=model.id,
            name=model.name,
            display_name=model.display_name,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_persistence(domain: Service) -> ServiceModel:
        return ServiceModel(
            id=domain.id,
            name=domain.name,
            display_name=domain.display_name,
            description=domain.description,
            is_active=domain.is_active,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
