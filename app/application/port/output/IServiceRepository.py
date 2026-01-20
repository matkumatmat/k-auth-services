from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.Service import Service


class IServiceRepository(ABC):
    @abstractmethod
    async def find_by_id(self, service_id: UUID) -> Service | None:
        pass

    @abstractmethod
    async def find_by_name(self, name: str) -> Service | None:
        pass

    @abstractmethod
    async def find_all_active(self) -> list[Service]:
        pass

    @abstractmethod
    async def find_by_ids(self, service_ids: list[UUID]) -> list[Service]:
        pass

    @abstractmethod
    async def save(self, service: Service) -> Service:
        pass
