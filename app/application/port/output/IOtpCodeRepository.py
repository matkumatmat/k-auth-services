from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.OtpCode import OtpCode
from app.domain.ValueObjects import OtpPurpose


class IOtpCodeRepository(ABC):
    @abstractmethod
    async def find_by_id(self, otp_id: UUID) -> OtpCode | None:
        pass

    @abstractmethod
    async def find_valid_by_target(self, delivery_target: str, purpose: OtpPurpose) -> OtpCode | None:
        pass

    @abstractmethod
    async def save(self, otp: OtpCode) -> OtpCode:
        pass

    @abstractmethod
    async def mark_used(self, otp_id: UUID) -> None:
        pass
