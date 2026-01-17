from abc import ABC, abstractmethod
from uuid import UUID

from app.application.dto.ServiceAccessDTO import ServiceAccessResult


class IValidateServiceAccess(ABC):
    @abstractmethod
    async def execute(self, user_id: UUID, service_name: str) -> ServiceAccessResult:
        pass

    @abstractmethod
    async def check_feature_access(self, user_id: UUID, service_name: str, feature: str) -> bool:
        pass
