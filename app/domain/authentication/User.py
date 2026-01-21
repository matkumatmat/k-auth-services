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

    def has_primary_contact(self) -> bool:
        return self.has_email() or self.has_phone()

    def can_add_auth_provider(self) -> bool:
        return self.is_verified and self.is_active and not self.is_deleted()

    def get_primary_contact(self) -> str | None:
        return self.email if self.has_email() else self.phone

    def supports_password_auth(self) -> bool:
        return (self.has_email() or self.has_phone()) and self.has_password()

    def mark_verified(self) -> None:
        self.is_verified = True

    def mark_unverified(self) -> None:
        self.is_verified = False
