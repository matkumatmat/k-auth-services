import secrets
import string
from datetime import timedelta
from uuid import UUID

from app.application.port.input.IResendOtp import IResendOtp
from app.application.port.output.IAuthProviderRepository import IAuthProviderRepository
from app.application.port.output.IOtpCodeRepository import IOtpCodeRepository
from app.application.port.output.IUserRepository import IUserRepository
from app.domain.OtpCode import OtpCode
from app.domain.ValueObjects import AuthProviderType, OtpDeliveryMethod, OtpPurpose
from app.infrastructure.config.EnvConfig import EnvConfig
from app.shared.Cryptography import Salter
from app.shared.DateTime import DateTimeProtocol
from app.shared.OtpRateLimiter import OtpRateLimiter
from app.shared.UuidGenerator import UuidGeneratorProtocol
from app.domain.exceptions import (
    UserEmailRequiredException,
    UserNotFoundException,
    UserPhoneRequiredException,
)


class ResendOtpService(IResendOtp):
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

    async def resend_email_otp(self, user_id: UUID) -> None:
        await self.rate_limiter.check_rate_limit(user_id, operation="otp_resend_email")

        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(details={"user_id": str(user_id)})

        if not user.has_email():
            raise UserEmailRequiredException(user_id=str(user_id))

        email = user.email

        existing_otp = await self.otp_repository.find_valid_by_target(email, OtpPurpose.REGISTRATION)
        if existing_otp:
            await self.otp_repository.mark_used(existing_otp.id)

        current_time = self.datetime_converter.now_utc()
        otp_expiry_seconds = self.config.auth.otp_expiry_seconds
        otp_expires_at = self.datetime_converter.add_timedelta(
            current_time,
            timedelta(seconds=otp_expiry_seconds)
        )

        raw_otp_code = ''.join(
            secrets.choice(string.digits) for _ in range(self.config.auth.otp_code_length)
        )

        if self.config.debug_otp:
            print(f"\n[DEBUG] Resend OTP for {email}: {raw_otp_code}\n")

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

    async def resend_phone_otp(self, user_id: UUID) -> None:
        await self.rate_limiter.check_rate_limit(user_id, operation="otp_resend_phone")

        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(details={"user_id": str(user_id)})

        if not user.has_phone():
            raise UserPhoneRequiredException(user_id=str(user_id))

        phone = user.phone

        existing_otp = await self.otp_repository.find_valid_by_target(phone, OtpPurpose.REGISTRATION)
        if existing_otp:
            await self.otp_repository.mark_used(existing_otp.id)

        current_time = self.datetime_converter.now_utc()
        otp_expiry_seconds = self.config.auth.otp_expiry_seconds
        otp_expires_at = self.datetime_converter.add_timedelta(
            current_time,
            timedelta(seconds=otp_expiry_seconds)
        )

        raw_otp_code = ''.join(
            secrets.choice(string.digits) for _ in range(self.config.auth.otp_code_length)
        )

        if self.config.debug_otp:
            print(f"\n[DEBUG] Resend OTP for {phone}: {raw_otp_code}\n")

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
