from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.User import User


class IRegisterUser(ABC):
    @abstractmethod
    async def execute_with_email(self, email: str, password: str) -> User:
        pass

    @abstractmethod
    async def execute_with_phone(self, phone: str) -> User:
        pass

    @abstractmethod
    async def verify_email(self, user_id: UUID, otp_code: str) -> bool:
        pass

    @abstractmethod
    async def verify_phone(self, user_id: UUID, otp_code: str) -> bool:
        pass
