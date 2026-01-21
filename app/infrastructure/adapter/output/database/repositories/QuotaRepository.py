from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.port.output.IQuotaRepository import IQuotaRepository
from app.domain.service.Quota import Quota
from app.infrastructure.adapter.output.database.mappers.QuotaMapper import QuotaMapper
from app.infrastructure.config.database.persistence.QuotaModel import QuotaModel


class QuotaRepository(IQuotaRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_user_and_service(
        self, user_id: UUID, service_name: str, quota_type: str
    ) -> Quota | None:
        stmt = select(QuotaModel).where(
            QuotaModel.user_id == user_id,
            QuotaModel.service_name == service_name,
            QuotaModel.quota_type == quota_type
        )
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return QuotaMapper.to_domain(model) if model else None

    async def update_usage(self, quota_id: UUID, amount: int) -> bool:
        current_time = datetime.utcnow()

        stmt = (
            update(QuotaModel)
            .where(QuotaModel.id == quota_id)
            .where(QuotaModel.current_usage + amount <= QuotaModel.limit)
            .values(
                current_usage=QuotaModel.current_usage + amount,
                updated_at=current_time
            )
            .returning(QuotaModel)
        )

        result = await self._session.execute(stmt)
        updated_model = result.scalars().first()
        await self._session.flush()

        return updated_model is not None

    async def reset_if_needed(self, quota_id: UUID, current_time: datetime) -> Quota:
        stmt = (
            update(QuotaModel)
            .where(QuotaModel.id == quota_id)
            .values(
                current_usage=0,
                reset_at=current_time,
                updated_at=current_time
            )
            .returning(QuotaModel)
        )

        result = await self._session.execute(stmt)
        updated_model = result.scalars().one()
        await self._session.flush()

        return QuotaMapper.to_domain(updated_model)

    async def save(self, quota: Quota) -> Quota:
        quota_model = QuotaMapper.to_persistence(quota)
        self._session.add(quota_model)
        await self._session.flush()
        await self._session.refresh(quota_model)
        return QuotaMapper.to_domain(quota_model)
