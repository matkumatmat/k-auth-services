from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class ServiceAccess:
    id: UUID
    user_id: UUID
    service_name: str
    is_allowed: bool
    allowed_features: list[str] | None
    granted_at: datetime
    revoked_at: datetime | None
    created_at: datetime
    updated_at: datetime

    def is_active(self) -> bool:
        return self.is_allowed and self.revoked_at is None

    def is_revoked(self) -> bool:
        return self.revoked_at is not None

    def has_feature(self, feature: str) -> bool:
        if not self.is_active():
            return False
        if self.allowed_features is None:
            return True
        return feature in self.allowed_features
