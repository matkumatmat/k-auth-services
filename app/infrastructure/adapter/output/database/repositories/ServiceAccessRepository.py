from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.port.output.IServiceAccessRepository import IServiceAccessRepository
from app.domain.authorization.ServiceAccess import ServiceAccess
from app.infrastructure.adapter.output.database.mappers.ServiceAccessMapper import ServiceAccessMapper
from app.infrastructure.config.database.persistence.ServiceAccessModel import ServiceAccessModel
from app.shared.DateTime import DateTimeProtocol


class ServiceAccessRepository(IServiceAccessRepository):
    def __init__(self, session: AsyncSession, datetime_converter: DateTimeProtocol):
        self._session = session
        self._datetime_converter = datetime_converter

    async def find_by_user_and_service(
        self, user_id: UUID, service_name: str
    ) -> ServiceAccess | None:
        stmt = select(ServiceAccessModel).where(
            ServiceAccessModel.user_id == user_id,
            ServiceAccessModel.service_name == service_name
        )
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return ServiceAccessMapper.to_domain(model) if model else None

    async def find_all_by_user(self, user_id: UUID) -> list[ServiceAccess]:
        stmt = select(ServiceAccessModel).where(
            ServiceAccessModel.user_id == user_id,
            ServiceAccessModel.revoked_at.is_(None)
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [ServiceAccessMapper.to_domain(model) for model in models]

    async def save(self, service_access: ServiceAccess) -> ServiceAccess:
        access_model = ServiceAccessMapper.to_persistence(service_access)
        self._session.add(access_model)
        await self._session.flush()
        await self._session.refresh(access_model)
        return ServiceAccessMapper.to_domain(access_model)

    async def revoke(self, access_id: UUID) -> None:
        current_time = self._datetime_converter.now_utc()
        stmt = (
            update(ServiceAccessModel)
            .where(ServiceAccessModel.id == access_id)
            .values(
                revoked_at=current_time,
                is_allowed=False,
                updated_at=current_time
            )
        )
        await self._session.execute(stmt)
        await self._session.flush()
