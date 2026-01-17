from datetime import timedelta
from uuid import UUID

from app.application.dto.AuthenticationDTO import AuthenticationResult
from app.application.port.input.IRefreshToken import IRefreshToken
from app.application.port.output.ISessionRepository import ISessionRepository
from app.application.port.output.ITransactionLogger import ITransactionLogger
from app.domain.Session import Session
from app.domain.UserBehaviorLog import UserBehaviorLog
from app.domain.ValueObjects import UserBehaviorAction
from app.shared.Cryptography import Salter
from app.shared.DateTime import DateTimeProtocol
from app.shared.Exceptions import AuthenticationException, TokenExpiredException, TokenInvalidException
from app.shared.TokenGenerator import ITokenGenerator
from app.shared.UuidGenerator import UuidGeneratorProtocol


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
            raise TokenExpiredException(message="Refresh token has expired")
        except TokenInvalidException:
            raise TokenInvalidException(message="Refresh token is invalid")

        token_type = payload.get("type")
        if token_type != "refresh":
            raise TokenInvalidException(message="Token is not a refresh token")

        user_id_str = payload.get("user_id")
        if not user_id_str:
            raise TokenInvalidException(message="Token payload missing user_id")

        try:
            user_id = UUID(user_id_str)
        except (ValueError, TypeError):
            raise TokenInvalidException(message="Invalid user_id format in token")

        sessions = await self.session_repository.find_active_by_user(user_id)

        if not sessions:
            raise AuthenticationException(message="No active session found for user")

        current_time = self.datetime_converter.now_utc()
        matching_session = None

        for session in sessions:
            if session.is_active(current_time):
                is_valid = self.salter.verify_password(refresh_token, session.refresh_token_hash)
                if is_valid:
                    matching_session = session
                    break

        if not matching_session:
            raise AuthenticationException(message="Invalid or expired refresh token")

        await self.session_repository.revoke(matching_session.id)

        access_token_payload = {"user_id": str(user_id), "type": "access"}
        access_token = self.token_generator.generate(
            access_token_payload,
            expires_delta=timedelta(hours=1)
        )

        new_refresh_token_payload = {"user_id": str(user_id), "type": "refresh"}
        new_refresh_token = self.token_generator.generate(
            new_refresh_token_payload,
            expires_delta=timedelta(days=7)
        )
        new_refresh_token_hash = self.salter.hash_password(new_refresh_token)

        new_session = Session(
            id=self.uuid_generator.generate(),
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
                metadata={"old_session_id": str(matching_session.id), "new_session_id": str(new_session.id)},
                timestamp=current_time
            )
        )

        return AuthenticationResult(
            user_id=user_id,
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=3600,
            token_type="Bearer",
        )
