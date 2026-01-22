from datetime import timedelta
from uuid import UUID

from app.application.dto.QuotaCheckDTO import QuotaCheckResult
from app.application.port.input.ICheckQuota import ICheckQuota
from app.application.port.input.IValidateServiceAccess import IValidateServiceAccess
from app.application.port.output.IPlanRepository import IPlanRepository
from app.application.port.output.IQuotaRepository import IQuotaRepository
from app.application.port.output.ITransactionLogger import ITransactionLogger
from app.application.port.output.IUserPlanRepository import IUserPlanRepository
from app.domain.log.DatabaseTransactionLog import DatabaseTransactionLog
from app.domain.service.Quota import Quota
from app.domain.service.QuotaDefaults import QuotaDefaults
from app.domain.ValueObjects import DatabaseOperation
from app.shared.DateTime import DateTimeProtocol
from app.shared.UuidGenerator import UuidGeneratorProtocol
from app.domain.exceptions import (
    AccessDeniedException,
    InsufficientQuotaException,
)


class QuotaManagementService(ICheckQuota):
    def __init__(
        self,
        quota_repository: IQuotaRepository,
        user_plan_repository: IUserPlanRepository,
        plan_repository: IPlanRepository,
        transaction_logger: ITransactionLogger,
        datetime_converter: DateTimeProtocol,
        uuid_generator: UuidGeneratorProtocol,
        service_access_validator: IValidateServiceAccess,
        quota_defaults: QuotaDefaults,
    ):
        self.quota_repository = quota_repository
        self.user_plan_repository = user_plan_repository
        self.plan_repository = plan_repository
        self.transaction_logger = transaction_logger
        self.datetime_converter = datetime_converter
        self.uuid_generator = uuid_generator
        self.service_access_validator = service_access_validator
        self.quota_defaults = quota_defaults

    async def execute(self, user_id: UUID, service_name: str, quota_type: str, amount: int) -> QuotaCheckResult:
        current_time = self.datetime_converter.now_utc()

        quota = await self.quota_repository.find_by_user_and_service(
            user_id, service_name, quota_type
        )

        if not quota:
            quota = await self._create_default_quota(user_id, service_name, quota_type, current_time)

        if quota.needs_reset(current_time):
            quota = await self.quota_repository.reset_if_needed(quota.id, current_time)

        can_proceed = quota.can_consume(amount)

        return QuotaCheckResult(
            can_proceed=can_proceed,
            current_usage=quota.current_usage,
            limit=quota.limit,
            remaining=quota.remaining(),
            reset_at=self.datetime_converter.to_iso_string(quota.reset_at),
            error_message=None if can_proceed else "Quota limit exceeded"
        )

    async def consume(self, user_id: UUID, service_name: str, quota_type: str, amount: int) -> bool:
        current_time = self.datetime_converter.now_utc()

        service_access_result = await self.service_access_validator.execute(user_id, service_name)
        if not service_access_result.is_allowed:
            raise AccessDeniedException(resource=service_name)

        quota = await self.quota_repository.find_by_user_and_service(
            user_id, service_name, quota_type
        )

        if not quota:
            quota = await self._create_default_quota(user_id, service_name, quota_type, current_time)

        if quota.needs_reset(current_time):
            quota = await self.quota_repository.reset_if_needed(quota.id, current_time)

        if not quota.can_consume(amount):
            raise InsufficientQuotaException(
                quota_type=quota_type,
                current=quota.current_usage,
                required=amount
            )

        update_success = await self.quota_repository.update_usage(quota.id, amount)

        if not update_success:
            raise InsufficientQuotaException(
                quota_type=quota_type,
                current=quota.current_usage,
                required=amount
            )

        await self.transaction_logger.log_database_transaction(
            DatabaseTransactionLog(
                id=self.uuid_generator.generate(),
                table_name="quotas",
                operation=DatabaseOperation.UPDATE,
                record_id=quota.id,
                user_id=user_id,
                old_value={"current_usage": quota.current_usage},
                new_value={"current_usage": quota.current_usage + amount},
                created_at=self.datetime_converter.now_utc(),
                transaction_id=self.uuid_generator.generate()
            )
        )

        return True

    async def _create_default_quota(
        self,
        user_id: UUID,
        service_name: str,
        quota_type: str,
        current_time
    ) -> Quota:
        user_plan = await self.user_plan_repository.find_active_by_user(user_id)

        if user_plan:
            plan = await self.plan_repository.find_by_id(user_plan.plan_id)
            if plan:
                quota_limit = plan.get_quota_limit(quota_type)
                default_limit = self.quota_defaults.get_limit_for_plan(quota_limit)
            else:
                default_limit = self.quota_defaults.fallback_limit
        else:
            default_limit = self.quota_defaults.get_anonymous_limit()

        reset_at = self.datetime_converter.add_timedelta(
            current_time,
            self.quota_defaults.get_reset_period()
        )

        quota = Quota(
            id=self.uuid_generator.generate(),
            user_id=user_id,
            service_name=service_name,
            quota_type=quota_type,
            current_usage=0,
            limit=default_limit,
            reset_at=reset_at,
            created_at=current_time,
            updated_at=current_time
        )

        saved_quota = await self.quota_repository.save(quota)

        await self.transaction_logger.log_database_transaction(
            DatabaseTransactionLog(
                id=self.uuid_generator.generate(),
                table_name="quotas",
                operation=DatabaseOperation.INSERT,
                record_id=saved_quota.id,
                user_id=user_id,
                old_value={},
                new_value={
                    "service_name": service_name,
                    "quota_type": quota_type,
                    "limit": default_limit
                },
                created_at=current_time,
                transaction_id=self.uuid_generator.generate()
            )
        )

        return saved_quota
