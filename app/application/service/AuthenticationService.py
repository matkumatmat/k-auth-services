from datetime import timedelta
from uuid import UUID

from app.application.dto.AuthenticationDTO import AuthenticationResult
from app.application.port.input.IAuthenticateUser import IAuthenticateUser
from app.application.port.output.IAuthProviderRepository import IAuthProviderRepository
from app.application.port.output.IOtpCodeRepository import IOtpCodeRepository
from app.application.port.output.ISessionRepository import ISessionRepository
from app.application.port.output.ITransactionLogger import ITransactionLogger
from app.application.port.output.IUserRepository import IUserRepository
from app.domain.authorization.Session import Session
from app.domain.log.UserBehaviorLog import UserBehaviorLog
from app.domain.ValueObjects import OtpPurpose, UserBehaviorAction
from app.shared.Cryptography import Salter
from app.shared.DateTime import DateTimeProtocol
from app.shared.TokenGenerator import ITokenGenerator
from app.shared.UuidGenerator import UuidGeneratorProtocol
from app.domain.exceptions import (
    AuthenticationException,
    InvalidCredentialsException,
    UserNotFoundException,
)
from app.shared.Logger import ILogger


class AuthenticationService(IAuthenticateUser):
    def __init__(
        self,
        user_repository: IUserRepository,
        auth_provider_repository: IAuthProviderRepository,
        session_repository: ISessionRepository,
        otp_repository: IOtpCodeRepository,
        transaction_logger: ITransactionLogger,
        salter: Salter,
        token_generator: ITokenGenerator,
        uuid_generator: UuidGeneratorProtocol,
        datetime_converter: DateTimeProtocol,
        logger: ILogger,
    ):
        self.user_repository = user_repository
        self.auth_provider_repository = auth_provider_repository
        self.session_repository = session_repository
        self.otp_repository = otp_repository
        self.transaction_logger = transaction_logger
        self.salter = salter
        self.token_generator = token_generator
        self.uuid_generator = uuid_generator
        self.datetime_converter = datetime_converter
        self.logger = logger


    async def execute_with_email(self, email: str, password: str, device_info: str, ip_address: str) -> AuthenticationResult:
        current_time = self.datetime_converter.now_utc()
        user = await self.user_repository.find_by_email(email)

        if not user:
            await self.transaction_logger.log_user_behavior(
                UserBehaviorLog(
                    id=self.uuid_generator.generate(),
                    user_id=None,
                    action=UserBehaviorAction.LOGIN_FAILED,
                    ip_address=ip_address,
                    user_agent=device_info,
                    additional_metadata={"email": email, "reason": "user_not_found"},
                    created_at=current_time
                )
            )
            raise UserNotFoundException(details={"email": email})

        if not user.can_authenticate():
            await self.transaction_logger.log_user_behavior(
                UserBehaviorLog(
                    id=self.uuid_generator.generate(),
                    user_id=user.id,
                    action=UserBehaviorAction.LOGIN_FAILED,
                    ip_address=ip_address,
                    user_agent=device_info,
                    additional_metadata={"email": email, "reason": "account_not_active_or_verified"},
                    # service_name=service_name,
                    created_at=current_time
                )
            )
            raise AuthenticationException("User account is not active or verified")

        if not user.has_password():
            await self.transaction_logger.log_user_behavior(
                UserBehaviorLog(
                    id=self.uuid_generator.generate(),
                    user_id=user.id,
                    action=UserBehaviorAction.LOGIN_FAILED,
                    ip_address=ip_address,
                    user_agent=device_info,
                    additional_metadata={"email": email, "reason": "password_not_configured"},
                    created_at=current_time
                )
            )
            raise InvalidCredentialsException()

        is_valid = self.salter.verify_password(password, user.password_hash)
        if not is_valid:
            await self.transaction_logger.log_user_behavior(
                UserBehaviorLog(
                    id=self.uuid_generator.generate(),
                    user_id=user.id,
                    action=UserBehaviorAction.LOGIN_FAILED,
                    ip_address=ip_address,
                    user_agent=device_info,
                    additional_metadata={"email": email, "reason": "invalid_password"},
                    created_at=current_time
                )
            )
            raise InvalidCredentialsException()

        result = await self._create_session(user.id, device_info, ip_address)

        await self.transaction_logger.log_user_behavior(
            UserBehaviorLog(
                id=self.uuid_generator.generate(),
                user_id=user.id,
                action=UserBehaviorAction.LOGIN_SUCCESS,
                ip_address=ip_address,
                user_agent=device_info,
                additional_metadata={"email": email, "method": "email_password"},
                created_at=current_time
            )
        )

        return result

    async def execute_with_phone(self, phone: str, otp_code: str, device_info: str, ip_address: str) -> AuthenticationResult:
        current_time = self.datetime_converter.now_utc()
        user = await self.user_repository.find_by_phone(phone)

        if not user:
            await self.transaction_logger.log_user_behavior(
                UserBehaviorLog(
                    id=self.uuid_generator.generate(),
                    user_id=None,
                    action=UserBehaviorAction.LOGIN_FAILED,
                    ip_address=ip_address,
                    user_agent=device_info,
                    additional_metadata={"phone": phone, "reason": "user_not_found"},
                    created_at=current_time
                )
            )
            raise UserNotFoundException(details={"phone": phone})

        if not user.can_authenticate():
            await self.transaction_logger.log_user_behavior(
                UserBehaviorLog(
                    id=self.uuid_generator.generate(),
                    user_id=user.id,
                    action=UserBehaviorAction.LOGIN_FAILED,
                    ip_address=ip_address,
                    user_agent=device_info,
                    additional_metadata={"phone": phone, "reason": "account_not_active_or_verified"},
                    created_at=current_time
                )
            )
            raise AuthenticationException("User account is not active or verified")

        otp = await self.otp_repository.find_valid_by_target(phone, OtpPurpose.LOGIN)

        if not otp or not otp.is_valid(current_time):
            await self.transaction_logger.log_user_behavior(
                UserBehaviorLog(
                    id=self.uuid_generator.generate(),
                    user_id=user.id,
                    action=UserBehaviorAction.LOGIN_FAILED,
                    ip_address=ip_address,
                    user_agent=device_info,
                    additional_metadata={"phone": phone, "reason": "invalid_or_expired_otp"},
                    created_at=current_time
                )
            )
            raise InvalidCredentialsException()

        is_valid = self.salter.verify_password(otp_code, otp.code_hash)
        if not is_valid:
            await self.transaction_logger.log_user_behavior(
                UserBehaviorLog(
                    id=self.uuid_generator.generate(),
                    user_id=user.id,
                    action=UserBehaviorAction.LOGIN_FAILED,
                    ip_address=ip_address,
                    user_agent=device_info,
                    additional_metadata={"phone": phone, "reason": "invalid_otp_code"},
                    created_at=current_time
                )
            )
            raise InvalidCredentialsException()

        await self.otp_repository.mark_used(otp.id)

        result = await self._create_session(user.id, device_info, ip_address)

        await self.transaction_logger.log_user_behavior(
            UserBehaviorLog(
                id=self.uuid_generator.generate(),
                user_id=user.id,
                action=UserBehaviorAction.LOGIN_SUCCESS,
                ip_address=ip_address,
                user_agent=device_info,
                additional_metadata={"phone": phone, "method": "phone_otp"},
                created_at=current_time
            )
        )

        return result

    async def execute_with_oauth2(self, provider: str, code: str, device_info: str, ip_address: str) -> AuthenticationResult:
        raise NotImplementedError("OAuth2 authentication not yet implemented")

    async def _create_session(self, user_id: UUID, device_info: str, ip_address: str) -> AuthenticationResult:
        current_time = self.datetime_converter.now_utc()

        session_id = self.uuid_generator.generate()

        access_token_payload = {
            "user_id": str(user_id),
            "session_id": str(session_id),
            "type": "access"
        }
        access_token = self.token_generator.generate(
            access_token_payload,
            expires_delta=timedelta(hours=1)
        )

        refresh_token_payload = {
            "user_id": str(user_id),
            "session_id": str(session_id),
            "type": "refresh"
        }
        refresh_token = self.token_generator.generate(
            refresh_token_payload,
            expires_delta=timedelta(days=7)
        )
        refresh_token_hash = self.salter.hash_password(refresh_token)

        session = Session(
            id=session_id,
            user_id=user_id,
            refresh_token_hash=refresh_token_hash,
            device_info=device_info,
            ip_address=ip_address,
            expires_at=self.datetime_converter.add_timedelta(
                current_time,
                timedelta(days=7)
            ),
            revoked_at=None,
            created_at=current_time,
        )

        await self.session_repository.save(session)

        return AuthenticationResult(
            user_id=user_id,
            session_id=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=3600,
            token_type="Bearer",
        )
