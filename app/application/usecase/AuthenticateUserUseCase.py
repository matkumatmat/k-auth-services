from datetime import datetime, timezone
from uuid import uuid4
import bcrypt

from app.application.dto.AuthenticationDTO import AuthenticationRequest, AuthenticationResult
from app.application.port.input.IAuthenticateUser import IAuthenticateUser
from app.application.port.output.ISessionRepository import ISessionRepository
from app.application.port.output.IUserRepository import IUserRepository
from app.application.service.IJwtService import IJwtService
from app.domain.Session import Session


class AuthenticateUserUseCase(IAuthenticateUser):

    def __init__(self, user_repository: IUserRepository, session_repository: ISessionRepository, jwt_service: IJwtService):
        self._user_repository = user_repository
        self._session_repository = session_repository
        self._jwt_service = jwt_service

    async def execute_with_email(self, email: str, password: str, device_info: str, ip_address: str) -> AuthenticationResult:
        user = await self._user_repository.find_by_email(email)
        if user is None or not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            raise Exception("Invalid credentials")

        session = Session(
            id=uuid4(),
            user_id=user.id,
            device_info=device_info,
            ip_address=ip_address,
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        await self._session_repository.save(session)

        access_token = self._jwt_service.create_access_token(user.id, session.id, [])
        refresh_token = self._jwt_service.create_refresh_token(session.id)

        return AuthenticationResult(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user
        )

    async def execute_with_phone(self, phone: str, otp_code: str, device_info: str, ip_address: str) -> AuthenticationResult:
        pass

    async def execute_with_oauth2(self, provider: str, code: str, device_info: str, ip_address: str) -> AuthenticationResult:
        pass
