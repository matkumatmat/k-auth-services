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

    def can_be_used(self, current_time: datetime) -> bool:
        return self.is_valid(current_time)

    def matches_target(self, target: str) -> bool:
        return self.delivery_target == target

    def is_for_registration(self) -> bool:
        return self.purpose == OtpPurpose.REGISTRATION

    def is_for_login(self) -> bool:
        return self.purpose == OtpPurpose.LOGIN

    def is_for_password_reset(self) -> bool:
        return self.purpose == OtpPurpose.PASSWORD_RESET

    def mark_used(self, current_time: datetime) -> None:
        self.used_at = current_time
