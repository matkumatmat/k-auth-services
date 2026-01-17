from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class ApiKey:
    id: UUID
    user_id: UUID
    key_hash: str
    name: str
    scopes: list[str]
    expires_at: datetime | None
    last_used_at: datetime | None
    is_active: bool
    created_at: datetime

    def is_expired(self, current_time: datetime) -> bool:
        if self.expires_at is None:
            return False
        return current_time > self.expires_at

    def is_valid(self, current_time: datetime) -> bool:
        return self.is_active and not self.is_expired(current_time)

    def has_scope(self, scope: str) -> bool:
        return scope in self.scopes

    def has_any_scope(self, scopes: list[str]) -> bool:
        return any(scope in self.scopes for scope in scopes)
