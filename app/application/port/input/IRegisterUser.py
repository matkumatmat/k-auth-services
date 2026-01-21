from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.authentication.User import User


class IRegisterUser(ABC):
    @abstractmethod
    async def execute(self, contact: str, password: str | None = None) -> User:
        pass

    @abstractmethod
    async def verify(self, user_id: UUID, otp_code: str) -> bool:
        pass
