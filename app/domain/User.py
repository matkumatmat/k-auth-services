from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    email: str | None
    phone: str | None
    password_hash: str | None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None

    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def has_password(self) -> bool:
        return self.password_hash is not None

    def has_email(self) -> bool:
        return self.email is not None

    def has_phone(self) -> bool:
        return self.phone is not None

    def can_authenticate(self) -> bool:
        return self.is_active and self.is_verified and not self.is_deleted()
