from dataclasses import dataclass
from uuid import UUID


@dataclass
class TokenValidationResult:
    is_valid: bool
    user_id: UUID | None = None
    session_id: UUID | None = None
    error_message: str | None = None
    refresh_token: str | None = None
