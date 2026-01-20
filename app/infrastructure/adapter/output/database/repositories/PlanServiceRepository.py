from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.port.output.IPlanServiceRepository import IPlanServiceRepository
from app.domain.PlanService import PlanService
from app.infrastructure.adapter.output.database.mappers.PlanServiceMapper import PlanServiceMapper
from app.infrastructure.config.database.persistence.PlanServiceModel import PlanServiceModel


class PlanServiceRepository(IPlanServiceRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_plan_id(self, plan_id: UUID) -> list[PlanService]:
        stmt = select(PlanServiceModel).where(PlanServiceModel.plan_id == plan_id)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [PlanServiceMapper.to_domain(model) for model in models]

    async def find_by_plan_and_service(self, plan_id: UUID, service_id: UUID) -> PlanService | None:
        stmt = select(PlanServiceModel).where(
            PlanServiceModel.plan_id == plan_id,
            PlanServiceModel.service_id == service_id
        )
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return PlanServiceMapper.to_domain(model) if model else None

    async def save(self, plan_service: PlanService) -> PlanService:
        plan_service_model = PlanServiceMapper.to_persistence(plan_service)
        self._session.add(plan_service_model)
        await self._session.flush()
        await self._session.refresh(plan_service_model)
        return PlanServiceMapper.to_domain(plan_service_model)

    async def save_many(self, plan_services: list[PlanService]) -> list[PlanService]:
        plan_service_models = [PlanServiceMapper.to_persistence(ps) for ps in plan_services]
        self._session.add_all(plan_service_models)
        await self._session.flush()
        for model in plan_service_models:
            await self._session.refresh(model)
        return [PlanServiceMapper.to_domain(model) for model in plan_service_models]

    async def delete(self, plan_service_id: UUID) -> None:
        stmt = delete(PlanServiceModel).where(PlanServiceModel.id == plan_service_id)
        await self._session.execute(stmt)
        await self._session.flush()

    async def delete_by_plan_id(self, plan_id: UUID) -> None:
        stmt = delete(PlanServiceModel).where(PlanServiceModel.plan_id == plan_id)
        await self._session.execute(stmt)
        await self._session.flush()
