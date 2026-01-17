from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.ServiceAccess import ServiceAccess


class IServiceAccessRepository(ABC):
    @abstractmethod
    async def find_by_user_and_service(self, user_id: UUID, service_name: str) -> ServiceAccess | None:
        pass

    @abstractmethod
    async def find_all_by_user(self, user_id: UUID) -> list[ServiceAccess]:
        pass

    @abstractmethod
    async def save(self, access: ServiceAccess) -> ServiceAccess:
        pass

    @abstractmethod
    async def revoke(self, access_id: UUID) -> None:
        pass
