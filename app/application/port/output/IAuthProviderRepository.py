from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.AuthProvider import AuthProvider
from app.domain.ValueObjects import AuthProviderType


class IAuthProviderRepository(ABC):
    @abstractmethod
    async def find_by_id(self, provider_id: UUID) -> AuthProvider | None:
        pass

    @abstractmethod
    async def find_by_user_and_type(self, user_id: UUID, provider_type: AuthProviderType) -> AuthProvider | None:
        pass

    @abstractmethod
    async def find_by_external_id(self, provider_type: AuthProviderType, external_id: str) -> AuthProvider | None:
        pass

    @abstractmethod
    async def save(self, provider: AuthProvider) -> AuthProvider:
        pass
