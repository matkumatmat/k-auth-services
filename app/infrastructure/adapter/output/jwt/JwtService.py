
import jwt
from datetime import datetime, timedelta, timezone
from uuid import UUID
from app.application.service.IJwtService import IJwtService


class JwtService(IJwtService):

    def __init__(self, secret_key: str, access_token_expire_minutes: int, refresh_token_expire_days: int):
        self._secret_key = secret_key
        self._access_token_expire_minutes = access_token_expire_minutes
        self._refresh_token_expire_days = refresh_token_expire_days

    def create_access_token(
        self, user_id: UUID, session_id: UUID, scopes: list[str]
    ) -> str:
        to_encode = {
            "sub": str(user_id),
            "session_id": str(session_id),
            "scopes": scopes,
            "exp": datetime.now(timezone.UTC) + timedelta(minutes=self._access_token_expire_minutes),
            "iat": datetime.now(timezone.UTC),
            "type": "access"
        }
        return jwt.encode(to_encode, self._secret_key, algorithm="HS256")

    def create_refresh_token(self, session_id: UUID) -> str:
        to_encode = {
            "sub": str(session_id),
            "exp": datetime.now(timezone.UTC) + timedelta(days=self._refresh_token_expire_days),
            "iat": datetime.now(timezone.UTC),
            "type": "refresh"
        }
        return jwt.encode(to_encode, self._secret_key, algorithm="HS256")

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, self._secret_key, algorithms=["HS256"])
