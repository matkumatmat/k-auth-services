from datetime import datetime
from uuid import UUID

from anyio import current_time
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.port.output.IOtpCodeRepository import IOtpCodeRepository
from app.domain.OtpCode import OtpCode
from app.domain.ValueObjects import OtpPurpose
from app.infrastructure.adapter.output.database.mappers.OtpCodeMapper import OtpCodeMapper
from app.infrastructure.config.database.persistence.OtpCodeModel import OtpCodeModel
from app.shared.DateTime import DateTimeConverter

class OtpCodeRepository(IOtpCodeRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, otp_id: UUID) -> OtpCode | None:
        stmt = select(OtpCodeModel).where(OtpCodeModel.id == otp_id)
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return OtpCodeMapper.to_domain(model) if model else None

    async def find_valid_by_target(
        self, target: str, purpose: OtpPurpose
    ) -> OtpCode | None:
        current_time = DateTimeConverter().now_utc()
        stmt = select(OtpCodeModel).where(
            OtpCodeModel.delivery_target == target,
            OtpCodeModel.purpose == purpose.value,
            OtpCodeModel.used_at.is_(None),
            OtpCodeModel.expires_at > current_time
        ).order_by(OtpCodeModel.created_at.desc())

        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return OtpCodeMapper.to_domain(model) if model else None

    async def save(self, otp: OtpCode) -> OtpCode:
        otp_model = OtpCodeMapper.to_persistence(otp)
        self._session.add(otp_model)
        await self._session.flush()
        await self._session.refresh(otp_model)
        return OtpCodeMapper.to_domain(otp_model)

    async def mark_used(self, otp_id: UUID) -> None:
        current_time = DateTimeConverter().now_utc()
        stmt = (
            update(OtpCodeModel)
            .where(OtpCodeModel.id == otp_id)
            .values(used_at=current_time)
        )
        await self._session.execute(stmt)
        await self._session.flush()
