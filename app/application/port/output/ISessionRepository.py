from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.authorization.Session import Session


class ISessionRepository(ABC):
    @abstractmethod
    async def find_by_id(self, session_id: UUID) -> Session | None:
        pass

    @abstractmethod
    async def find_active_by_user(self, user_id: UUID) -> list[Session]:
        pass

    @abstractmethod
    async def save(self, session: Session) -> Session:
        pass

    @abstractmethod
    async def revoke(self, session_id: UUID) -> None:
        pass

    @abstractmethod
    async def revoke_all_by_user(self, user_id: UUID) -> None:
        pass
