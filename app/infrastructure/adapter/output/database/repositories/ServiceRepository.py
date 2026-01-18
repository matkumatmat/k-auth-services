from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.port.output.IServiceRepository import IServiceRepository
from app.domain.Service import Service
from app.infrastructure.adapter.output.database.mappers.ServiceMapper import ServiceMapper
from app.infrastructure.config.database.persistence.ServiceModel import ServiceModel


class ServiceRepository(IServiceRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, service_id: UUID) -> Service | None:
        stmt = select(ServiceModel).where(ServiceModel.id == service_id)
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return ServiceMapper.to_domain(model) if model else None

    async def find_by_name(self, name: str) -> Service | None:
        stmt = select(ServiceModel).where(ServiceModel.name == name)
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return ServiceMapper.to_domain(model) if model else None

    async def find_all_active(self) -> list[Service]:
        stmt = select(ServiceModel).where(ServiceModel.is_active == True)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [ServiceMapper.to_domain(model) for model in models]

    async def save(self, service: Service) -> Service:
        service_model = ServiceMapper.to_persistence(service)
        self._session.add(service_model)
        await self._session.flush()
        await self._session.refresh(service_model)
        return ServiceMapper.to_domain(service_model)
