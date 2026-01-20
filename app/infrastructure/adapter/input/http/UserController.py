from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.application.service.ServiceAccessValidationService import ServiceAccessValidationService
from app.application.service.UserRegistrationService import UserRegistrationService
from app.infrastructure.dependencies import (
    get_current_user,
    get_service_access_validation_service,
    get_user_registration_service
)
from app.domain.exceptions import (
    InvalidOtpCodeException,
    UserNotFoundException,
)

router = APIRouter(prefix="/user", tags=["User"])


class VerifyOtpRequest(BaseModel):
    otp_code: str


class ServiceInfo(BaseModel):
    service_name: str
    allowed_features: list[str] | None


@router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_otp(
    request: VerifyOtpRequest,
    service: UserRegistrationService = Depends(get_user_registration_service),
    current_user = Depends(get_current_user)
):
    try:
        result = await service.verify(current_user.user_id, request.otp_code)
        return {"verified": result, "message": "Account verified successfully"}
    except (UserNotFoundException, InvalidOtpCodeException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/services", response_model=list[ServiceInfo])
async def get_user_services(
    service: ServiceAccessValidationService = Depends(get_service_access_validation_service),
    current_user = Depends(get_current_user)
):
    from app.infrastructure.dependencies import get_db_session
    from app.infrastructure.adapter.output.database.repositories.ServiceAccessRepository import ServiceAccessRepository

    async for session in get_db_session():
        repo = ServiceAccessRepository(session)
        service_accesses = await repo.find_all_by_user(current_user.user_id)

        return [
            ServiceInfo(
                service_name=sa.service_name,
                allowed_features=sa.allowed_features
            )
            for sa in service_accesses
        ]
