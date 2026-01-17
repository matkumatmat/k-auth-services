from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.User import User


class IUserRepository(ABC):
    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def find_by_phone(self, phone: str) -> User | None:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        pass
