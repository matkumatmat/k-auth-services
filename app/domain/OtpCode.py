from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.ValueObjects import OtpDeliveryMethod, OtpPurpose


@dataclass
class OtpCode:
    id: UUID
    user_id: UUID | None
    code_hash: str
    delivery_method: OtpDeliveryMethod
    delivery_target: str
    purpose: OtpPurpose
    expires_at: datetime
    used_at: datetime | None
    created_at: datetime

    def is_expired(self, current_time: datetime) -> bool:
        return current_time > self.expires_at

    def is_used(self) -> bool:
        return self.used_at is not None

    def is_valid(self, current_time: datetime) -> bool:
        return not self.is_expired(current_time) and not self.is_used()
