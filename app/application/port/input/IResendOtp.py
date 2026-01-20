from abc import ABC, abstractmethod
from uuid import UUID


class IResendOtp(ABC):
    @abstractmethod
    async def resend_email_otp(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def resend_phone_otp(self, user_id: UUID) -> None:
        pass
