from abc import ABC, abstractmethod
from uuid import UUID


class IRevokeSession(ABC):
    @abstractmethod
    async def execute(self, session_id: UUID, authenticated_user_id: UUID | None = None) -> None:
        pass

    @abstractmethod
    async def execute_all_by_user(self, user_id: UUID) -> None:
        pass
