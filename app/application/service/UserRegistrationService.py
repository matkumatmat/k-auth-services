from uuid import UUID

from app.application.port.input.IRegisterUser import IRegisterUser
from app.application.port.output.IAuthProviderRepository import IAuthProviderRepository
from app.application.port.output.IOtpCodeRepository import IOtpCodeRepository
from app.application.port.output.IPlanRepository import IPlanRepository
from app.application.port.output.IServiceAccessRepository import IServiceAccessRepository
from app.application.port.output.IServiceRepository import IServiceRepository
from app.application.port.output.ITransactionLogger import ITransactionLogger
from app.application.port.output.IUserPlanRepository import IUserPlanRepository
from app.application.port.output.IUserRepository import IUserRepository
from app.domain.AuthProvider import AuthProvider
from app.domain.DatabaseTransactionLog import DatabaseTransactionLog
from app.domain.ServiceAccess import ServiceAccess
from app.domain.User import User
from app.domain.UserPlan import UserPlan
from app.domain.ValueObjects import AuthProviderType, BillingCycle, DatabaseOperation, OtpPurpose
from app.shared.Cryptography import Salter
from app.shared.DateTime import DateTimeProtocol
from app.shared.Exceptions import InvalidCredentialsException, UserAlreadyExistsException, UserNotFoundException
from app.shared.UuidGenerator import UuidGeneratorProtocol


class UserRegistrationService(IRegisterUser):
    def __init__(
        self,
        user_repository: IUserRepository,
        auth_provider_repository: IAuthProviderRepository,
        otp_repository: IOtpCodeRepository,
        plan_repository: IPlanRepository,
        user_plan_repository: IUserPlanRepository,
        service_repository: IServiceRepository,
        service_access_repository: IServiceAccessRepository,
        transaction_logger: ITransactionLogger,
        salter: Salter,
        uuid_generator: UuidGeneratorProtocol,
        datetime_converter: DateTimeProtocol,
    ):
        self.user_repository = user_repository
        self.auth_provider_repository = auth_provider_repository
        self.otp_repository = otp_repository
        self.plan_repository = plan_repository
        self.user_plan_repository = user_plan_repository
        self.service_repository = service_repository
        self.service_access_repository = service_access_repository
        self.transaction_logger = transaction_logger
        self.salter = salter
        self.uuid_generator = uuid_generator
        self.datetime_converter = datetime_converter

    async def execute_with_email(self, email: str, password: str) -> User:
        existing_user = await self.user_repository.find_by_email(email)
        if existing_user:
            raise UserAlreadyExistsException(details={"email": email})

        current_time = self.datetime_converter.now_utc()
        password_hash = self.salter.hash_password(password)

        user = User(
            id=self.uuid_generator.generate(),
            email=email,
            phone=None,
            password_hash=password_hash,
            is_active=True,
            is_verified=False,
            created_at=current_time,
            updated_at=current_time,
            deleted_at=None
        )

        saved_user = await self.user_repository.save(user)

        await self.transaction_logger.log_database_transaction(
            DatabaseTransactionLog(
                id=self.uuid_generator.generate(),
                table_name="users",
                operation=DatabaseOperation.INSERT,
                record_id=saved_user.id,
                user_id=saved_user.id,
                old_values={},
                new_values={"email": email, "is_verified": False},
                timestamp=current_time
            )
        )

        auth_provider = AuthProvider(
            id=self.uuid_generator.generate(),
            user_id=saved_user.id,
            provider_type=AuthProviderType.EMAIL,
            provider_user_id=email,
            is_primary=True,
            provider_metadata={},
            created_at=current_time
        )

        await self.auth_provider_repository.save(auth_provider)

        await self._auto_assign_plan_and_services(saved_user.id, current_time)

        return saved_user

    async def execute_with_phone(self, phone: str) -> User:
        existing_user = await self.user_repository.find_by_phone(phone)
        if existing_user:
            raise UserAlreadyExistsException(details={"phone": phone})

        current_time = self.datetime_converter.now_utc()

        user = User(
            id=self.uuid_generator.generate(),
            email=None,
            phone=phone,
            password_hash=None,
            is_active=True,
            is_verified=False,
            created_at=current_time,
            updated_at=current_time,
            deleted_at=None
        )

        saved_user = await self.user_repository.save(user)

        await self.transaction_logger.log_database_transaction(
            DatabaseTransactionLog(
                id=self.uuid_generator.generate(),
                table_name="users",
                operation=DatabaseOperation.INSERT,
                record_id=saved_user.id,
                user_id=saved_user.id,
                old_values={},
                new_values={"phone": phone, "is_verified": False},
                timestamp=current_time
            )
        )

        auth_provider = AuthProvider(
            id=self.uuid_generator.generate(),
            user_id=saved_user.id,
            provider_type=AuthProviderType.WHATSAPP,
            provider_user_id=phone,
            is_primary=True,
            provider_metadata={},
            created_at=current_time
        )

        await self.auth_provider_repository.save(auth_provider)

        await self._auto_assign_plan_and_services(saved_user.id, current_time)

        return saved_user

    async def _auto_assign_plan_and_services(self, user_id: UUID, current_time) -> None:
        free_plan = await self.plan_repository.find_by_name("Free")

        if not free_plan:
            return

        user_plan = UserPlan(
            id=self.uuid_generator.generate(),
            user_id=user_id,
            plan_id=free_plan.id,
            started_at=current_time,
            expires_at=None,
            is_active=True,
            created_at=current_time,
            updated_at=current_time
        )

        await self.user_plan_repository.save(user_plan)

        await self.transaction_logger.log_database_transaction(
            DatabaseTransactionLog(
                id=self.uuid_generator.generate(),
                table_name="user_plans",
                operation=DatabaseOperation.INSERT,
                record_id=user_plan.id,
                user_id=user_id,
                old_values={},
                new_values={"plan_id": str(free_plan.id), "plan_name": free_plan.name},
                timestamp=current_time
            )
        )

        default_services = await self._get_default_services_for_plan(free_plan.name)

        for service in default_services:
            service_access = ServiceAccess(
                id=self.uuid_generator.generate(),
                user_id=user_id,
                service_name=service.name,
                is_allowed=True,
                allowed_features=None,
                granted_at=current_time,
                revoked_at=None,
                created_at=current_time,
                updated_at=current_time
            )

            await self.service_access_repository.save(service_access)

            await self.transaction_logger.log_database_transaction(
                DatabaseTransactionLog(
                    id=self.uuid_generator.generate(),
                    table_name="service_access",
                    operation=DatabaseOperation.INSERT,
                    record_id=service_access.id,
                    user_id=user_id,
                    old_values={},
                    new_values={"service_name": service.name},
                    timestamp=current_time
                )
            )

    async def _get_default_services_for_plan(self, plan_name: str) -> list:
        all_services = await self.service_repository.find_all_active()

        if plan_name == "Anonym":
            return []
        elif plan_name == "Free":
            default_service_names = ["cvmaker", "jobportal"]
            return [s for s in all_services if s.name in default_service_names]
        elif plan_name == "Pro":
            default_service_names = ["cvmaker", "jobportal", "3dbinpacking", "media_information"]
            return [s for s in all_services if s.name in default_service_names]
        elif plan_name == "Enterprise":
            return all_services
        else:
            return []

    async def verify_email(self, user_id: UUID, otp_code: str) -> bool:
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(details={"user_id": str(user_id)})

        if not user.has_email():
            raise InvalidCredentialsException(message="User does not have an email address")

        current_time = self.datetime_converter.now_utc()
        otp = await self.otp_repository.find_valid_by_target(user.email, OtpPurpose.REGISTRATION)

        if not otp or not otp.is_valid(current_time):
            raise InvalidCredentialsException(message="Invalid or expired OTP code")

        is_valid = self.salter.verify_password(otp_code, otp.code_hash)
        if not is_valid:
            raise InvalidCredentialsException(message="Invalid OTP code")

        await self.otp_repository.mark_used(otp.id)

        user.is_verified = True
        user.updated_at = current_time
        await self.user_repository.update(user)

        await self.transaction_logger.log_database_transaction(
            DatabaseTransactionLog(
                id=self.uuid_generator.generate(),
                table_name="users",
                operation=DatabaseOperation.UPDATE,
                record_id=user.id,
                user_id=user.id,
                old_values={"is_verified": False},
                new_values={"is_verified": True},
                timestamp=current_time
            )
        )

        return True

    async def verify_phone(self, user_id: UUID, otp_code: str) -> bool:
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(details={"user_id": str(user_id)})

        if not user.has_phone():
            raise InvalidCredentialsException(message="User does not have a phone number")

        current_time = self.datetime_converter.now_utc()
        otp = await self.otp_repository.find_valid_by_target(user.phone, OtpPurpose.REGISTRATION)

        if not otp or not otp.is_valid(current_time):
            raise InvalidCredentialsException(message="Invalid or expired OTP code")

        is_valid = self.salter.verify_password(otp_code, otp.code_hash)
        if not is_valid:
            raise InvalidCredentialsException(message="Invalid OTP code")

        await self.otp_repository.mark_used(otp.id)

        user.is_verified = True
        user.updated_at = current_time
        await self.user_repository.update(user)

        await self.transaction_logger.log_database_transaction(
            DatabaseTransactionLog(
                id=self.uuid_generator.generate(),
                table_name="users",
                operation=DatabaseOperation.UPDATE,
                record_id=user.id,
                user_id=user.id,
                old_values={"is_verified": False},
                new_values={"is_verified": True},
                timestamp=current_time
            )
        )

        return True
