import secrets
import string
from datetime import timedelta
from uuid import UUID

from app.application.port.input.ILinkAuthProvider import ILinkAuthProvider
from app.application.port.output.IAuthProviderRepository import IAuthProviderRepository
from app.application.port.output.IOtpCodeRepository import IOtpCodeRepository
from app.application.port.output.IUserRepository import IUserRepository
from app.domain.AuthProvider import AuthProvider
from app.domain.OtpCode import OtpCode
from app.domain.ValueObjects import AuthProviderType, OtpDeliveryMethod, OtpPurpose
from app.infrastructure.config.EnvConfig import EnvConfig
from app.shared.Cryptography import Salter
from app.shared.DateTime import DateTimeProtocol
from app.shared.Exceptions import UserAlreadyExistsException, UserNotFoundException
from app.shared.OtpRateLimiter import OtpRateLimiter
from app.shared.UuidGenerator import UuidGeneratorProtocol


class LinkAuthProviderService(ILinkAuthProvider):
    def __init__(
        self,
        user_repository: IUserRepository,
        auth_provider_repository: IAuthProviderRepository,
        otp_repository: IOtpCodeRepository,
        salter: Salter,
        uuid_generator: UuidGeneratorProtocol,
        datetime_converter: DateTimeProtocol,
        config: EnvConfig,
        rate_limiter: OtpRateLimiter,
    ):
        self.user_repository = user_repository
        self.auth_provider_repository = auth_provider_repository
        self.otp_repository = otp_repository
        self.salter = salter
        self.uuid_generator = uuid_generator
        self.datetime_converter = datetime_converter
        self.config = config
        self.rate_limiter = rate_limiter

    async def link_email(self, user_id: UUID, email: str, password: str) -> None:
        await self.rate_limiter.check_rate_limit(user_id, operation="link_email")

        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(details={"user_id": str(user_id)})

        existing_user_with_email = await self.user_repository.find_by_email(email)
        if existing_user_with_email and existing_user_with_email.id != user_id:
            raise UserAlreadyExistsException(
                message="Email is already linked to another user",
                details={"email": email}
            )

        existing_provider = await self.auth_provider_repository.find_by_user_and_type(
            user_id, AuthProviderType.EMAIL
        )
        if existing_provider:
            raise UserAlreadyExistsException(
                message="User already has email provider linked",
                details={"user_id": str(user_id)}
            )

        current_time = self.datetime_converter.now_utc()
        password_hash = self.salter.hash_password(password)

        user.email = email
        user.password_hash = password_hash
        user.updated_at = current_time

        await self.user_repository.update(user)

        auth_provider = AuthProvider(
            id=self.uuid_generator.generate(),
            user_id=user_id,
            provider_type=AuthProviderType.EMAIL,
            provider_user_id=email,
            is_primary=False,
            provider_metadata={},
            created_at=current_time
        )

        await self.auth_provider_repository.save(auth_provider)

        otp_expiry_seconds = self.config.auth.otp_expiry_seconds
        otp_expires_at = self.datetime_converter.add_timedelta(
            current_time,
            timedelta(seconds=otp_expiry_seconds)
        )

        raw_otp_code = ''.join(
            secrets.choice(string.digits) for _ in range(self.config.auth.otp_code_length)
        )

        if self.config.debug_otp:
            print(f"\n[DEBUG] Link Email OTP for {email}: {raw_otp_code}\n")

        otp_hash = self.salter.hash_password(raw_otp_code)
        otp_code = OtpCode(
            id=self.uuid_generator.generate(),
            user_id=user_id,
            code_hash=otp_hash,
            delivery_method=OtpDeliveryMethod.EMAIL,
            delivery_target=email,
            purpose=OtpPurpose.REGISTRATION,
            expires_at=otp_expires_at,
            used_at=None,
            created_at=current_time
        )

        await self.otp_repository.save(otp_code)

    async def link_phone(self, user_id: UUID, phone: str) -> None:
        await self.rate_limiter.check_rate_limit(user_id, operation="link_phone")

        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(details={"user_id": str(user_id)})

        existing_user_with_phone = await self.user_repository.find_by_phone(phone)
        if existing_user_with_phone and existing_user_with_phone.id != user_id:
            raise UserAlreadyExistsException(
                message="Phone is already linked to another user",
                details={"phone": phone}
            )

        existing_provider = await self.auth_provider_repository.find_by_user_and_type(
            user_id, AuthProviderType.WHATSAPP
        )
        if existing_provider:
            raise UserAlreadyExistsException(
                message="User already has phone provider linked",
                details={"user_id": str(user_id)}
            )

        current_time = self.datetime_converter.now_utc()

        user.phone = phone
        user.updated_at = current_time

        await self.user_repository.update(user)

        auth_provider = AuthProvider(
            id=self.uuid_generator.generate(),
            user_id=user_id,
            provider_type=AuthProviderType.WHATSAPP,
            provider_user_id=phone,
            is_primary=False,
            provider_metadata={},
            created_at=current_time
        )

        await self.auth_provider_repository.save(auth_provider)

        otp_expiry_seconds = self.config.auth.otp_expiry_seconds
        otp_expires_at = self.datetime_converter.add_timedelta(
            current_time,
            timedelta(seconds=otp_expiry_seconds)
        )

        raw_otp_code = ''.join(
            secrets.choice(string.digits) for _ in range(self.config.auth.otp_code_length)
        )

        if self.config.debug_otp:
            print(f"\n[DEBUG] Link Phone OTP for {phone}: {raw_otp_code}\n")

        otp_hash = self.salter.hash_password(raw_otp_code)
        otp_code = OtpCode(
            id=self.uuid_generator.generate(),
            user_id=user_id,
            code_hash=otp_hash,
            delivery_method=OtpDeliveryMethod.WHATSAPP,
            delivery_target=phone,
            purpose=OtpPurpose.REGISTRATION,
            expires_at=otp_expires_at,
            used_at=None,
            created_at=current_time
        )

        await self.otp_repository.save(otp_code)
