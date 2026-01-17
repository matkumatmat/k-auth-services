from abc import ABC, abstractmethod
from uuid import UUID


class IRevokeSession(ABC):
    @abstractmethod
    async def execute(self, session_id: UUID) -> None:
        pass

    @abstractmethod
    async def execute_all_by_user(self, user_id: UUID) -> None:
        pass
