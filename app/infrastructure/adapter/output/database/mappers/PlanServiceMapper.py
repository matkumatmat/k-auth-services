from app.domain.service.PlanService import PlanService
from app.infrastructure.config.database.persistence.PlanServiceModel import PlanServiceModel


class PlanServiceMapper:
    @staticmethod
    def to_domain(model: PlanServiceModel) -> PlanService:
        return PlanService(
            id=model.id,
            plan_id=model.plan_id,
            service_id=model.service_id,
            created_at=model.created_at
        )

    @staticmethod
    def to_persistence(domain: PlanService) -> PlanServiceModel:
        return PlanServiceModel(
            id=domain.id,
            plan_id=domain.plan_id,
            service_id=domain.service_id,
            created_at=domain.created_at
        )
