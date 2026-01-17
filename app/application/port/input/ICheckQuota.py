from abc import ABC, abstractmethod
from uuid import UUID

from app.application.dto.QuotaCheckDTO import QuotaCheckResult


class ICheckQuota(ABC):
    @abstractmethod
    async def execute(self, user_id: UUID, service_name: str, quota_type: str, amount: int) -> QuotaCheckResult:
        pass

    @abstractmethod
    async def consume(self, user_id: UUID, service_name: str, quota_type: str, amount: int) -> bool:
        pass
