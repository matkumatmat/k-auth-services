
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.port.output.IUserRepository import IUserRepository
from app.domain.User import User
from app.infrastructure.adapter.output.database.mappers.UserMapper import UserMapper
from app.infrastructure.config.database.persistence.UserModel import UserModel


class UserRepository(IUserRepository):

    def __init__(self, session: AsyncSession):
        self._session = session
        self._mapper = UserMapper()

    async def find_by_id(self, user_id: UUID) -> User | None:
        stmt = select(UserModel).where(UserModel.id == user_id, UserModel.deleted_at.is_(None))
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return self._mapper.to_domain(model) if model else None

    async def find_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email, UserModel.deleted_at.is_(None))
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return self._mapper.to_domain(model) if model else None

    async def find_by_phone(self, phone: str) -> User | None:
        stmt = select(UserModel).where(UserModel.phone == phone, UserModel.deleted_at.is_(None))
        result = await self._session.execute(stmt)
        model = result.scalars().first()
        return self._mapper.to_domain(model) if model else None

    async def save(self, user: User) -> User:
        user_model = self._mapper.to_persistence(user)
        self._session.add(user_model)
        await self._session.flush()
        await self._session.refresh(user_model)
        return self._mapper.to_domain(user_model)

    async def update(self, user: User) -> User:
        user_model = self._mapper.to_persistence(user)
        await self._session.merge(user_model)
        await self._session.flush()
        await self._session.refresh(user_model)
        return self._mapper.to_domain(user_model)

    async def delete(self, user_id: UUID) -> None:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(deleted_at=datetime.utcnow())
        )
        await self._session.execute(stmt)
        await self._session.flush()
