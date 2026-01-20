from collections.abc import AsyncGenerator

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.AuthenticationDTO import AuthenticatedUser
from app.application.service.AuthenticationService import AuthenticationService
from app.application.service.LinkAuthProviderService import LinkAuthProviderService
from app.application.service.QuotaManagementService import QuotaManagementService
from app.application.service.RefreshTokenService import RefreshTokenService
from app.application.service.ResendOtpService import ResendOtpService
from app.application.service.RevokeSessionService import RevokeSessionService
from app.application.service.ServiceAccessValidationService import ServiceAccessValidationService
from app.application.service.TokenValidationService import TokenValidationService
from app.application.service.UserRegistrationService import UserRegistrationService
# from app.infrastructure.adapter.output.database.repositories.ApiKeyRepository import ApiKeyRepository
from app.infrastructure.adapter.output.database.repositories.AuthProviderRepository import AuthProviderRepository
from app.infrastructure.adapter.output.database.repositories.OtpCodeRepository import OtpCodeRepository
from app.infrastructure.adapter.output.database.repositories.PlanRepository import PlanRepository
from app.infrastructure.adapter.output.database.repositories.PlanServiceRepository import PlanServiceRepository
from app.infrastructure.adapter.output.database.repositories.QuotaRepository import QuotaRepository
from app.infrastructure.adapter.output.database.repositories.ServiceAccessRepository import ServiceAccessRepository
from app.infrastructure.adapter.output.database.repositories.ServiceRepository import ServiceRepository
from app.infrastructure.adapter.output.database.repositories.SessionRepository import SessionRepository
from app.infrastructure.adapter.output.database.repositories.TransactionLoggerRepository import TransactionLoggerRepository
from app.infrastructure.adapter.output.database.repositories.UserPlanRepository import UserPlanRepository
from app.infrastructure.adapter.output.database.repositories.UserRepository import UserRepository
from app.infrastructure.config.database.DatabaseSession import DatabaseSessionFactory
from app.infrastructure.config.database.redis.RedisClient import RedisClient
from app.infrastructure.config.EnvConfig import EnvConfig
from app.shared.Cryptography import Salter
from app.shared.DateTime import DateTimeConverter
from app.shared.OtpRateLimiter import OtpRateLimiter
from app.shared.TokenGenerator import JwtTokenGenerator
from app.shared.UuidGenerator import UuidGenerator

config = EnvConfig.load()

db_factory = DatabaseSessionFactory(config.database)
redis_client = RedisClient(config.redis)

datetime_converter = DateTimeConverter()
uuid_generator = UuidGenerator()
salter = Salter(config.auth.password_salt)
token_generator = JwtTokenGenerator(
    secret_key=config.auth.jwt_secret,
    datetime_converter=datetime_converter,
    algorithm=config.auth.jwt_algorithm
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_factory.get_session() as session:
        yield session


async def get_redis() -> RedisClient:
    return redis_client


async def get_token_validation_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> TokenValidationService:
    return TokenValidationService(
        session_repository=SessionRepository(db_session),
        token_generator=token_generator,
        datetime_converter=datetime_converter
    )


async def get_service_access_validation_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> ServiceAccessValidationService:
    return ServiceAccessValidationService(
        service_access_repository=ServiceAccessRepository(db_session),
        user_plan_repository=UserPlanRepository(db_session),
        datetime_converter=datetime_converter
    )


async def get_quota_management_service(
    db_session: AsyncSession = Depends(get_db_session),
    service_access_validator: ServiceAccessValidationService = Depends(get_service_access_validation_service),
) -> QuotaManagementService:
    return QuotaManagementService(
        quota_repository=QuotaRepository(db_session),
        user_plan_repository=UserPlanRepository(db_session),
        plan_repository=PlanRepository(db_session),
        transaction_logger=TransactionLoggerRepository(db_session),
        datetime_converter=datetime_converter,
        uuid_generator=uuid_generator,
        service_access_validator=service_access_validator
    )


async def get_authentication_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> AuthenticationService:
    return AuthenticationService(
        user_repository=UserRepository(db_session),
        auth_provider_repository=AuthProviderRepository(db_session),
        session_repository=SessionRepository(db_session),
        otp_repository=OtpCodeRepository(db_session),
        transaction_logger=TransactionLoggerRepository(db_session),
        salter=salter,
        token_generator=token_generator,
        uuid_generator=uuid_generator,
        datetime_converter=datetime_converter
    )


async def get_user_registration_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> UserRegistrationService:
    return UserRegistrationService(
        user_repository=UserRepository(db_session),
        auth_provider_repository=AuthProviderRepository(db_session),
        otp_repository=OtpCodeRepository(db_session),
        plan_repository=PlanRepository(db_session),
        user_plan_repository=UserPlanRepository(db_session),
        service_repository=ServiceRepository(db_session),
        service_access_repository=ServiceAccessRepository(db_session),
        plan_service_repository=PlanServiceRepository(db_session),
        transaction_logger=TransactionLoggerRepository(db_session),
        salter=salter,
        uuid_generator=uuid_generator,
        datetime_converter=datetime_converter,
        config=config
    )


async def get_refresh_token_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> RefreshTokenService:
    return RefreshTokenService(
        session_repository=SessionRepository(db_session),
        transaction_logger=TransactionLoggerRepository(db_session),
        salter=salter,
        token_generator=token_generator,
        uuid_generator=uuid_generator,
        datetime_converter=datetime_converter
    )


async def get_revoke_session_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> RevokeSessionService:
    return RevokeSessionService(
        session_repository=SessionRepository(db_session),
        transaction_logger=TransactionLoggerRepository(db_session),
        datetime_converter=datetime_converter,
        uuid_generator=uuid_generator
    )


async def get_resend_otp_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> ResendOtpService:
    rate_limiter = OtpRateLimiter(
        redis_client=redis_client,
        max_requests=3,
        window_seconds=900
    )
    return ResendOtpService(
        user_repository=UserRepository(db_session),
        auth_provider_repository=AuthProviderRepository(db_session),
        otp_repository=OtpCodeRepository(db_session),
        salter=salter,
        uuid_generator=uuid_generator,
        datetime_converter=datetime_converter,
        config=config,
        rate_limiter=rate_limiter
    )


async def get_link_auth_provider_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> LinkAuthProviderService:
    return LinkAuthProviderService(
        user_repository=UserRepository(db_session),
        auth_provider_repository=AuthProviderRepository(db_session),
        otp_repository=OtpCodeRepository(db_session),
        salter=salter,
        uuid_generator=uuid_generator,
        datetime_converter=datetime_converter,
        config=config,
        rate_limiter=OtpRateLimiter(
            redis_client=redis_client,
            max_requests=5,
            window_seconds=600
    ))


async def get_current_user(
    authorization: str = Header(..., alias="Authorization"),
    token_validation_service: TokenValidationService = Depends(get_token_validation_service)
) -> AuthenticatedUser:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected 'Bearer <token>'"
        )

    token = authorization.replace("Bearer ", "")

    result = await token_validation_service.execute(token)

    if not result.is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result.error_message or "Invalid or expired token"
        )

    return AuthenticatedUser(
        user_id=result.user_id,
        session_id=result.session_id
    )

