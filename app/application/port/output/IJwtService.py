from abc import ABC, abstractmethod
from uuid import UUID


class IJwtService(ABC):
    @abstractmethod
    def create_access_token(
        self, user_id: UUID, session_id: UUID, scopes: list[str]
    ) -> str:
        pass

    @abstractmethod
    def create_refresh_token(self, session_id: UUID) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        pass
