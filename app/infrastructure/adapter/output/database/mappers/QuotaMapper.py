from app.domain.Quota import Quota
from app.infrastructure.config.database.persistence.QuotaModel import QuotaModel


class QuotaMapper:
    @staticmethod
    def to_domain(model: QuotaModel) -> Quota:
        return Quota(
            id=model.id,
            user_id=model.user_id,
            service_name=model.service_name,
            quota_type=model.quota_type,
            current_usage=model.current_usage,
            limit=model.limit,
            reset_at=model.reset_at,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_persistence(domain: Quota) -> QuotaModel:
        return QuotaModel(
            id=domain.id,
            user_id=domain.user_id,
            service_name=domain.service_name,
            quota_type=domain.quota_type,
            current_usage=domain.current_usage,
            limit=domain.limit,
            reset_at=domain.reset_at,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
