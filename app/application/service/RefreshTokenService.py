from datetime import timedelta
from uuid import UUID

from app.application.dto.AuthenticationDTO import AuthenticationResult
from app.application.port.input.IRefreshToken import IRefreshToken
from app.application.port.output.ISessionRepository import ISessionRepository
from app.application.port.output.ITransactionLogger import ITransactionLogger
from app.domain.authorization.Session import Session
from app.domain.log.UserBehaviorLog import UserBehaviorLog
from app.domain.ValueObjects import UserBehaviorAction
from app.shared.Cryptography import Salter
from app.shared.DateTime import DateTimeProtocol
from app.shared.TokenGenerator import ITokenGenerator
from app.shared.UuidGenerator import UuidGeneratorProtocol
from app.domain.exceptions import (
    # SessionExpiredException,
    SessionInactiveException,
    SessionNotFoundException,
    TokenExpiredException,
    TokenInvalidException,
)


class RefreshTokenService(IRefreshToken):
    def __init__(
        self,
        session_repository: ISessionRepository,
        transaction_logger: ITransactionLogger,
        salter: Salter,
        token_generator: ITokenGenerator,
        uuid_generator: UuidGeneratorProtocol,
        datetime_converter: DateTimeProtocol,
    ):
        self.session_repository = session_repository
        self.transaction_logger = transaction_logger
        self.salter = salter
        self.token_generator = token_generator
        self.uuid_generator = uuid_generator
        self.datetime_converter = datetime_converter

    async def execute(self, refresh_token: str) -> AuthenticationResult:
        try:
            payload = self.token_generator.decode(refresh_token)
        except TokenExpiredException:
            raise TokenExpiredException()
        except TokenInvalidException:
            raise TokenInvalidException()

        token_type = payload.get("type")
        if token_type != "refresh":
            raise TokenInvalidException("Token is not a refresh token")

        user_id_str = payload.get("user_id")
        if not user_id_str:
            raise TokenInvalidException("Token payload missing user_id")

        session_id_str = payload.get("session_id")
        if not session_id_str:
            raise TokenInvalidException("Token payload missing session_id")

        try:
            user_id = UUID(user_id_str)
            session_id = UUID(session_id_str)
        except (ValueError, TypeError):
            raise TokenInvalidException("Invalid user_id or session_id format in token")

        matching_session = await self.session_repository.find_by_id(session_id)

        if not matching_session:
            raise SessionNotFoundException(session_id=str(session_id))

        if matching_session.user_id != user_id:
            raise TokenInvalidException("Session does not belong to user")

        current_time = self.datetime_converter.now_utc()

        if not matching_session.is_active(current_time):
            raise SessionInactiveException(session_id=str(session_id))

        is_valid = self.salter.verify_password(refresh_token, matching_session.refresh_token_hash)
        if not is_valid:
            raise TokenInvalidException("Invalid refresh token")

        await self.session_repository.revoke(matching_session.id)

        new_session_id = self.uuid_generator.generate()

        access_token_payload = {
            "user_id": str(user_id),
            "session_id": str(new_session_id),
            "type": "access"
        }
        access_token = self.token_generator.generate(
            access_token_payload,
            expires_delta=timedelta(hours=1)
        )

        new_refresh_token_payload = {
            "user_id": str(user_id),
            "session_id": str(new_session_id),
            "type": "refresh"
        }
        new_refresh_token = self.token_generator.generate(
            new_refresh_token_payload,
            expires_delta=timedelta(days=7)
        )
        new_refresh_token_hash = self.salter.hash_password(new_refresh_token)

        new_session = Session(
            id=new_session_id,
            user_id=user_id,
            refresh_token_hash=new_refresh_token_hash,
            device_info=matching_session.device_info,
            ip_address=matching_session.ip_address,
            expires_at=self.datetime_converter.add_timedelta(
                current_time,
                timedelta(days=7)
            ),
            revoked_at=None,
            created_at=current_time,
        )

        await self.session_repository.save(new_session)

        await self.transaction_logger.log_user_behavior(
            UserBehaviorLog(
                id=self.uuid_generator.generate(),
                user_id=user_id,
                action=UserBehaviorAction.TOKEN_REFRESH,
                ip_address=matching_session.ip_address,
                user_agent=matching_session.device_info,
                additional_metadata={"old_session_id": str(matching_session.id), "new_session_id": str(new_session.id)},
                created_at=current_time
            )
        )

        return AuthenticationResult(
            user_id=user_id,
            session_id=new_session_id,
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=3600,
            token_type="Bearer",
        )
