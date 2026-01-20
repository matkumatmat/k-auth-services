from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.domain.Quota import Quota


class IQuotaRepository(ABC):
    @abstractmethod
    async def find_by_user_and_service(self, user_id: UUID, service_name: str, quota_type: str) -> Quota | None:
        pass

    @abstractmethod
    async def update_usage(self, quota_id: UUID, amount: int) -> bool:
        pass

    @abstractmethod
    async def reset_if_needed(self, quota_id: UUID, current_time: datetime) -> Quota:
        pass

    @abstractmethod
    async def save(self, quota: Quota) -> Quota:
        pass
