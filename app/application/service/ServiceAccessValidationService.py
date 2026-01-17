from uuid import UUID

from app.application.dto.ServiceAccessDTO import ServiceAccessResult
from app.application.port.input.IValidateServiceAccess import IValidateServiceAccess
from app.application.port.output.IServiceAccessRepository import IServiceAccessRepository
from app.application.port.output.IUserPlanRepository import IUserPlanRepository
from app.shared.DateTime import DateTimeProtocol


class ServiceAccessValidationService(IValidateServiceAccess):
    def __init__(
        self,
        service_access_repository: IServiceAccessRepository,
        user_plan_repository: IUserPlanRepository,
        datetime_converter: DateTimeProtocol,
    ):
        self.service_access_repository = service_access_repository
        self.user_plan_repository = user_plan_repository
        self.datetime_converter = datetime_converter

    async def execute(self, user_id: UUID, service_name: str) -> ServiceAccessResult:
        service_access = await self.service_access_repository.find_by_user_and_service(
            user_id, service_name
        )

        if not service_access:
            return ServiceAccessResult(
                is_allowed=False,
                error_message=f"No access configured for service: {service_name}"
            )

        if not service_access.is_active():
            return ServiceAccessResult(
                is_allowed=False,
                error_message="Service access has been revoked or disabled"
            )

        user_plan = await self.user_plan_repository.find_active_by_user(user_id)

        if not user_plan:
            return ServiceAccessResult(
                is_allowed=False,
                error_message="User has no active plan"
            )

        current_time = self.datetime_converter.now_utc()
        if not user_plan.is_active(current_time):
            return ServiceAccessResult(
                is_allowed=False,
                error_message="User plan has expired or is inactive"
            )

        return ServiceAccessResult(
            is_allowed=True,
            allowed_features=service_access.allowed_features
        )

    async def check_feature_access(self, user_id: UUID, service_name: str, feature: str) -> bool:
        service_access = await self.service_access_repository.find_by_user_and_service(
            user_id, service_name
        )

        if not service_access or not service_access.is_active():
            return False

        return service_access.has_feature(feature)
