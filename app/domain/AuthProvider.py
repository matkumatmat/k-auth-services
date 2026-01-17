from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.ValueObjects import AuthProviderType


@dataclass
class AuthProvider:
    id: UUID
    user_id: UUID
    provider_type: AuthProviderType
    provider_user_id: str
    is_primary: bool
    provider_metadata: dict[str, str | int | bool]
    created_at: datetime

    def is_oauth_provider(self) -> bool:
        return self.provider_type == AuthProviderType.OAUTH2_GOOGLE

    def is_email_provider(self) -> bool:
        return self.provider_type == AuthProviderType.EMAIL

    def is_whatsapp_provider(self) -> bool:
        return self.provider_type == AuthProviderType.WHATSAPP
