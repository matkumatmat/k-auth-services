from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Session:
    id: UUID
    user_id: UUID
    refresh_token_hash: str
    device_info: str
    ip_address: str
    expires_at: datetime
    revoked_at: datetime | None
    created_at: datetime

    def is_active(self, current_time: datetime) -> bool:
        return self.revoked_at is None and self.expires_at > current_time

    def is_expired(self, current_time: datetime) -> bool:
        return current_time > self.expires_at

    def is_revoked(self) -> bool:
        return self.revoked_at is not None
