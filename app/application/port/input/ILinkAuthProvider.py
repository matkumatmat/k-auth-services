from abc import ABC, abstractmethod
from uuid import UUID


class ILinkAuthProvider(ABC):
    @abstractmethod
    async def link_email(self, user_id: UUID, email: str, password: str) -> None:
        pass

    @abstractmethod
    async def link_phone(self, user_id: UUID, phone: str) -> None:
        pass
