from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserBehaviorLog:
    id: UUID
    user_id: UUID | None
    action: str
    service_name: str | None
    ip_address: str
    user_agent: str
    device_fingerprint: str | None
    geolocation: dict[str, str] | None
    additional_metadata: dict[str, str | int | bool] | None
    created_at: datetime

    def is_login_action(self) -> bool:
        return "login" in self.action.lower()

    def is_authenticated_action(self) -> bool:
        return self.user_id is not None

    def has_geolocation(self) -> bool:
        return self.geolocation is not None
