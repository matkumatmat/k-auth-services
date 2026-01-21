from app.domain.authentication.UserPlan import UserPlan
from app.domain.ValueObjects import UserPlanStatus
from app.infrastructure.config.database.persistence.UserPlanModel import UserPlanModel


class UserPlanMapper:
    @staticmethod
    def to_domain(model: UserPlanModel) -> UserPlan:
        return UserPlan(
            id=model.id,
            user_id=model.user_id,
            plan_id=model.plan_id,
            # Convert string dari DB balik ke Enum
            status=UserPlanStatus(model.status),
            started_at=model.started_at,
            expires_at=model.expires_at,
            # Mapping field baru
            auto_renew=model.auto_renew,
            payment_gateway=model.payment_gateway,
            payment_gateway_subscription_id=model.payment_gateway_subscription_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_persistence(domain: UserPlan) -> UserPlanModel:
        return UserPlanModel(
            id=domain.id,
            user_id=domain.user_id,
            plan_id=domain.plan_id,
            # Pass Enum langsung (SQLAlchemy bakal handle)
            status=domain.status,
            started_at=domain.started_at,
            expires_at=domain.expires_at,
            # HAPUS 'is_active', GANTI DENGAN field baru:
            auto_renew=domain.auto_renew,
            payment_gateway=domain.payment_gateway,
            payment_gateway_subscription_id=domain.payment_gateway_subscription_id,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )