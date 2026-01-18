from datetime import timedelta
from uuid import UUID

from app.application.dto.QuotaCheckDTO import QuotaCheckResult
from app.application.port.input.ICheckQuota import ICheckQuota
from app.application.port.output.IPlanRepository import IPlanRepository
from app.application.port.output.IQuotaRepository import IQuotaRepository
from app.application.port.output.ITransactionLogger import ITransactionLogger
from app.application.port.output.IUserPlanRepository import IUserPlanRepository
from app.domain.DatabaseTransactionLog import DatabaseTransactionLog
from app.domain.Quota import Quota
from app.domain.ValueObjects import DatabaseOperation
from app.shared.DateTime import DateTimeProtocol
from app.shared.Exceptions import InsufficientQuotaException
from app.shared.UuidGenerator import UuidGeneratorProtocol


class QuotaManagementService(ICheckQuota):
    def __init__(
        self,
        quota_repository: IQuotaRepository,
        user_plan_repository: IUserPlanRepository,
        plan_repository: IPlanRepository,
        transaction_logger: ITransactionLogger,
        datetime_converter: DateTimeProtocol,
        uuid_generator: UuidGeneratorProtocol,
    ):
        self.quota_repository = quota_repository
        self.user_plan_repository = user_plan_repository
        self.plan_repository = plan_repository
        self.transaction_logger = transaction_logger
        self.datetime_converter = datetime_converter
        self.uuid_generator = uuid_generator

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

        quota = await self.quota_repository.find_by_user_and_service(
            user_id, service_name, quota_type
        )

        if not quota:
            quota = await self._create_default_quota(user_id, service_name, quota_type, current_time)

        if quota.needs_reset(current_time):
            quota = await self.quota_repository.reset_if_needed(quota.id, current_time)

        if not quota.can_consume(amount):
            raise InsufficientQuotaException(
                details={
                    "service_name": service_name,
                    "quota_type": quota_type,
                    "current_usage": quota.current_usage,
                    "limit": quota.limit,
                    "requested": amount
                }
            )

        await self.quota_repository.update_usage(quota.id, amount)

        await self.transaction_logger.log_database_transaction(
            DatabaseTransactionLog(
                id=self.uuid_generator.generate(),
                table_name="quotas",
                operation=DatabaseOperation.UPDATE,
                record_id=quota.id,
                user_id=user_id,
                old_values={"current_usage": quota.current_usage},
                new_values={"current_usage": quota.current_usage + amount},
                timestamp=self.datetime_converter.now_utc()
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
                default_limit = quota_limit if quota_limit is not None else 50
            else:
                default_limit = 50
        else:
            default_limit = 1

        reset_at = self.datetime_converter.add_timedelta(
            current_time,
            timedelta(days=1)
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
                old_values={},
                new_values={
                    "service_name": service_name,
                    "quota_type": quota_type,
                    "limit": default_limit
                },
                timestamp=current_time
            )
        )

        return saved_quota
