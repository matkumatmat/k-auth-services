from dataclasses import dataclass
from uuid import UUID


@dataclass
class AuthenticationRequest:
    email: str | None = None
    phone: str | None = None
    password: str | None = None
    otp_code: str | None = None
    provider_code: str | None = None
    device_info: str | None = None
    ip_address: str | None = None


@dataclass
class AuthenticationResult:
    user_id: UUID
    session_id : UUID
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"

@dataclass
class AuthenticatedUser:
    user_id : UUID
    session_id : UUID
