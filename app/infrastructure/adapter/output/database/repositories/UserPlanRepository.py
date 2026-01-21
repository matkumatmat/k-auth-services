from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.port.output.IUserPlanRepository import IUserPlanRepository
from app.domain.authentication.UserPlan import UserPlan
from app.infrastructure.adapter.output.database.mappers.UserPlanMapper import UserPlanMapper
from app.infrastructure.config.database.persistence.UserPlanModel import UserPlanModel
from app.domain.ValueObjects import UserPlanStatus


class UserPlanRepository(IUserPlanRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, user_plan_id: UUID) -> UserPlan | None:
        stmt = select(UserPlanModel).where(UserPlanModel.id == user_plan_id)
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return UserPlanMapper.to_domain(model) if model else None

    async def find_active_by_user(self, user_id: UUID) -> UserPlan | None:
        current_time = datetime.utcnow()
        stmt = select(UserPlanModel).where(
            UserPlanModel.user_id == user_id,
            UserPlanModel.status == UserPlanStatus.ACTIVE,
            (UserPlanModel.expires_at.is_(None) | (UserPlanModel.expires_at > current_time))
        ).order_by(UserPlanModel.started_at.desc())

        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return UserPlanMapper.to_domain(model) if model else None

    async def save(self, user_plan: UserPlan) -> UserPlan:
        user_plan_model = UserPlanMapper.to_persistence(user_plan)
        self._session.add(user_plan_model)
        await self._session.flush()
        await self._session.refresh(user_plan_model)
        return UserPlanMapper.to_domain(user_plan_model)

    async def update(self, user_plan: UserPlan) -> UserPlan:
        user_plan_model = UserPlanMapper.to_persistence(user_plan)
        merged_model = await self._session.merge(user_plan_model)
        await self._session.flush()
        await self._session.refresh(merged_model)
        return UserPlanMapper.to_domain(merged_model)
