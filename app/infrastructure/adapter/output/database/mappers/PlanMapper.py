from app.domain.service.Plan import Plan
from app.domain.ValueObjects import BillingCycle
from app.infrastructure.config.database.persistence.PlanModel import PlanModel


class PlanMapper:
    @staticmethod
    def to_domain(model: PlanModel) -> Plan:
        return Plan(
            id=model.id,
            name=model.name,
            billing_cycle=BillingCycle(model.billing_cycle),
            features=model.features,
            rate_limits=model.rate_limits,
            quota_limits=model.quota_limits,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_persistence(domain: Plan) -> PlanModel:
        return PlanModel(
            id=domain.id,
            name=domain.name,
            billing_cycle=domain.billing_cycle.value,
            features=domain.features,
            rate_limits=domain.rate_limits,
            quota_limits=domain.quota_limits,
            is_active=domain.is_active,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )
