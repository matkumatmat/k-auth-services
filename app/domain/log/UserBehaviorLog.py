from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserBehaviorLog:
    id: UUID
    user_id: UUID | None
    action: str
    service_name: str | None =  None
    ip_address: str | None = None
    user_agent: str | None = None
    device_fingerprint: str | None = None #hardcode
    geolocation: dict[str, str] | None = None #hardcode
    additional_metadata: dict[str, str | int | bool] | None = None
    created_at: datetime = datetime.now()

    def is_login_action(self) -> bool:
        return "login" in self.action.lower()

    def is_authenticated_action(self) -> bool:
        return self.user_id is not None

    def has_geolocation(self) -> bool:
        return self.geolocation is not None
