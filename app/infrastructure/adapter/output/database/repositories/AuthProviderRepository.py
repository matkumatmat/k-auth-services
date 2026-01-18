from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.port.output.IAuthProviderRepository import IAuthProviderRepository
from app.domain.AuthProvider import AuthProvider
from app.domain.ValueObjects import AuthProviderType
from app.infrastructure.adapter.output.database.mappers.AuthProviderMapper import AuthProviderMapper
from app.infrastructure.config.database.persistence.AuthProviderModel import AuthProviderModel


class AuthProviderRepository(IAuthProviderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, provider_id: UUID) -> AuthProvider | None:
        stmt = select(AuthProviderModel).where(AuthProviderModel.id == provider_id)
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return AuthProviderMapper.to_domain(model) if model else None

    async def find_by_user_and_type(
        self, user_id: UUID, provider_type: AuthProviderType
    ) -> AuthProvider | None:
        stmt = select(AuthProviderModel).where(
            AuthProviderModel.user_id == user_id,
            AuthProviderModel.provider_type == provider_type.value
        )
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return AuthProviderMapper.to_domain(model) if model else None

    async def find_by_external_id(
        self, provider_type: AuthProviderType, external_id: str
    ) -> AuthProvider | None:
        stmt = select(AuthProviderModel).where(
            AuthProviderModel.provider_type == provider_type.value,
            AuthProviderModel.provider_user_id == external_id
        )
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return AuthProviderMapper.to_domain(model) if model else None

    async def save(self, provider: AuthProvider) -> AuthProvider:
        provider_model = AuthProviderMapper.to_persistence(provider)
        self._session.add(provider_model)
        await self._session.flush()
        await self._session.refresh(provider_model)
        return AuthProviderMapper.to_domain(provider_model)
