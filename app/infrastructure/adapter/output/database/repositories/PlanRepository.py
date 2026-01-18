
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.port.output.IPlanRepository import IPlanRepository
from app.domain.Plan import Plan
from app.infrastructure.adapter.output.database.mappers.PlanMapper import PlanMapper
from app.infrastructure.config.database.persistence.PlanModel import PlanModel


class PlanRepository(IPlanRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self._mapper = PlanMapper()

    async def find_by_id(self, plan_id: UUID) -> Plan | None:
        stmt = select(PlanModel).where(PlanModel.id == plan_id)
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return self._mapper.to_domain(model) if model else None

    async def find_by_name(self, name: str) -> Plan | None:
        stmt = select(PlanModel).where(PlanModel.name == name)
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return self._mapper.to_domain(model) if model else None

    async def find_all_active(self) -> list[Plan]:
        stmt = select(PlanModel).where(PlanModel.is_active.is_(True))
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._mapper.to_domain(model) for model in models]
