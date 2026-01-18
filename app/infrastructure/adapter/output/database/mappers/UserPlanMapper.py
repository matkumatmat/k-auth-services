from app.domain.UserPlan import UserPlan
from app.infrastructure.config.database.persistence.UserPlanModel import UserPlanModel


class UserPlanMapper:
    @staticmethod
    def to_domain(model: UserPlanModel) -> UserPlan:
        return UserPlan(
            id=model.id,
            user_id=model.user_id,
            plan_id=model.plan_id,
            started_at=model.started_at,
            expires_at=model.expires_at,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_persistence(domain: UserPlan) -> UserPlanModel:
        return UserPlanModel(
            id=domain.id,
            user_id=domain.user_id,
            plan_id=domain.plan_id,
            started_at=domain.started_at,
            expires_at=domain.expires_at,
            is_active=domain.is_active,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
