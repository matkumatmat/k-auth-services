
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.port.output.IApiKeyRepository import IApiKeyRepository
from app.domain.ApiKey import ApiKey
from app.infrastructure.adapter.output.database.mappers.ApiKeyMapper import ApiKeyMapper
from app.infrastructure.config.database.persistence.ApiKeyModel import ApiKeyModel


class ApiKeyRepository(IApiKeyRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self._mapper = ApiKeyMapper()

    async def find_by_id(self, api_key_id: UUID) -> ApiKey | None:
        stmt = select(ApiKeyModel).where(ApiKeyModel.id == api_key_id, ApiKeyModel.is_active.is_(True))
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return self._mapper.to_domain(model) if model else None

    async def find_by_key_hash(self, key_hash: str) -> ApiKey | None:
        stmt = select(ApiKeyModel).where(ApiKeyModel.key_hash == key_hash, ApiKeyModel.is_active.is_(True))
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return self._mapper.to_domain(model) if model else None

    async def find_active_by_user(self, user_id: UUID) -> list[ApiKey]:
        stmt = select(ApiKeyModel).where(ApiKeyModel.user_id == user_id, ApiKeyModel.is_active.is_(True))
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._mapper.to_domain(model) for model in models]

    async def save(self, api_key: ApiKey) -> ApiKey:
        api_key_model = self._mapper.to_persistence(api_key)
        self._session.add(api_key_model)
        await self._session.flush()
        await self._session.refresh(api_key_model)
        return self._mapper.to_domain(api_key_model)

    async def update(self, api_key: ApiKey) -> ApiKey:
        api_key_model = self._mapper.to_persistence(api_key)
        await self._session.merge(api_key_model)
        await self._session.flush()
        await self._session.refresh(api_key_model)
        return self._mapper.to_domain(api_key_model)

    async def delete(self, api_key_id: UUID) -> None:
        stmt = (
            update(ApiKeyModel)
            .where(ApiKeyModel.id == api_key_id)
            .values(is_active=False)
        )
        await self._session.execute(stmt)
        await self._session.flush()
