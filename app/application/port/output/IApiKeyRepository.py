from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.ApiKey import ApiKey


class IApiKeyRepository(ABC):
    @abstractmethod
    async def find_by_id(self, api_key_id: UUID) -> ApiKey | None:
        pass

    @abstractmethod
    async def find_by_key_hash(self, key_hash: str) -> ApiKey | None:
        pass

    @abstractmethod
    async def find_active_by_user(self, user_id: UUID) -> list[ApiKey]:
        pass

    @abstractmethod
    async def save(self, api_key: ApiKey) -> ApiKey:
        pass

    @abstractmethod
    async def update(self, api_key: ApiKey) -> ApiKey:
        pass

    @abstractmethod
    async def delete(self, api_key_id: UUID) -> None:
        pass
