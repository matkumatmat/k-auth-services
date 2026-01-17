from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.Plan import Plan


class IPlanRepository(ABC):
    @abstractmethod
    async def find_by_id(self, plan_id: UUID) -> Plan | None:
        pass

    @abstractmethod
    async def find_by_name(self, name: str) -> Plan | None:
        pass

    @abstractmethod
    async def find_all_active(self) -> list[Plan]:
        pass
