from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.PlanService import PlanService


class IPlanServiceRepository(ABC):
    @abstractmethod
    async def find_by_plan_id(self, plan_id: UUID) -> list[PlanService]:
        pass

    @abstractmethod
    async def find_by_plan_and_service(self, plan_id: UUID, service_id: UUID) -> PlanService | None:
        pass

    @abstractmethod
    async def save(self, plan_service: PlanService) -> PlanService:
        pass

    @abstractmethod
    async def save_many(self, plan_services: list[PlanService]) -> list[PlanService]:
        pass

    @abstractmethod
    async def delete(self, plan_service_id: UUID) -> None:
        pass

    @abstractmethod
    async def delete_by_plan_id(self, plan_id: UUID) -> None:
        pass
