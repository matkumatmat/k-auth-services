from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.application.service.ServiceAccessValidationService import ServiceAccessValidationService
from app.application.service.UserRegistrationService import UserRegistrationService
from app.infrastructure.dependencies import (
    get_service_access_validation_service,
    get_user_registration_service
)
from app.shared.Exceptions import InvalidCredentialsException, UserNotFoundException

router = APIRouter(prefix="/user", tags=["User"])


class VerifyEmailRequest(BaseModel):
    user_id: str
    otp_code: str


class VerifyPhoneRequest(BaseModel):
    user_id: str
    otp_code: str


class ServiceInfo(BaseModel):
    service_name: str
    allowed_features: list[str] | None


@router.post("/verify/email", status_code=status.HTTP_200_OK)
async def verify_email(
    request: VerifyEmailRequest,
    service: UserRegistrationService = Depends(get_user_registration_service)
):
    try:
        user_id = UUID(request.user_id)
        result = await service.verify_email(user_id, request.otp_code)
        return {"verified": result, "message": "Email verified successfully"}
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id format")


@router.post("/verify/phone", status_code=status.HTTP_200_OK)
async def verify_phone(
    request: VerifyPhoneRequest,
    service: UserRegistrationService = Depends(get_user_registration_service)
):
    try:
        user_id = UUID(request.user_id)
        result = await service.verify_phone(user_id, request.otp_code)
        return {"verified": result, "message": "Phone verified successfully"}
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id format")


@router.get("/services/{user_id}", response_model=list[ServiceInfo])
async def get_user_services(
    user_id: str,
    service: ServiceAccessValidationService = Depends(get_service_access_validation_service)
):
    try:
        uid = UUID(user_id)
        from app.infrastructure.dependencies import get_db_session
        from app.infrastructure.adapter.output.database.repositories.ServiceAccessRepository import ServiceAccessRepository

        async for session in get_db_session():
            repo = ServiceAccessRepository(session)
            service_accesses = await repo.find_all_by_user(uid)

            return [
                ServiceInfo(
                    service_name=sa.service_name,
                    allowed_features=sa.allowed_features
                )
                for sa in service_accesses
            ]
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id format")
