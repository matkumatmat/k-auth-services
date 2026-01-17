from uuid import UUID

from app.application.dto.TokenValidationDTO import TokenValidationResult
from app.application.port.input.IValidateToken import IValidateToken
from app.application.port.output.ISessionRepository import ISessionRepository
from app.shared.DateTime import DateTimeProtocol
from app.shared.Exceptions import TokenExpiredException, TokenInvalidException
from app.shared.TokenGenerator import ITokenGenerator


class TokenValidationService(IValidateToken):
    def __init__(
        self,
        session_repository: ISessionRepository,
        token_generator: ITokenGenerator,
        datetime_converter: DateTimeProtocol,
    ):
        self.session_repository = session_repository
        self.token_generator = token_generator
        self.datetime_converter = datetime_converter

    async def execute(self, token: str) -> TokenValidationResult:
        try:
            payload = self.token_generator.decode(token)
        except TokenExpiredException:
            return TokenValidationResult(
                is_valid=False,
                error_message="Token has expired"
            )
        except TokenInvalidException:
            return TokenValidationResult(
                is_valid=False,
                error_message="Token is invalid"
            )

        user_id_str = payload.get("user_id")
        if not user_id_str:
            return TokenValidationResult(
                is_valid=False,
                error_message="Token payload missing user_id"
            )

        try:
            user_id = UUID(user_id_str)
        except (ValueError, TypeError):
            return TokenValidationResult(
                is_valid=False,
                error_message="Invalid user_id format in token"
            )

        sessions = await self.session_repository.find_active_by_user(user_id)

        if not sessions:
            return TokenValidationResult(
                is_valid=False,
                error_message="No active session found for user"
            )

        current_time = self.datetime_converter.now_utc()
        active_session = None

        for session in sessions:
            if session.is_active(current_time):
                active_session = session
                break

        if not active_session:
            return TokenValidationResult(
                is_valid=False,
                error_message="Session expired or revoked"
            )

        return TokenValidationResult(
            is_valid=True,
            user_id=user_id,
            session_id=active_session.id
        )
