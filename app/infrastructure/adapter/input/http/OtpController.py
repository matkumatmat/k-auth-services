from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.application.service.LinkAuthProviderService import LinkAuthProviderService
from app.application.service.ResendOtpService import ResendOtpService
from app.infrastructure.dependencies import (
    get_current_user,
    get_link_auth_provider_service,
    get_resend_otp_service
)
from app.domain.exceptions import (
    TooManyRequestsException,
    UserAlreadyExistsException,
    UserEmailRequiredException,
    UserNotFoundException,
    UserPhoneRequiredException,
)

router = APIRouter(prefix="/otp", tags=["OTP"])


class LinkEmailRequest(BaseModel):
    email: EmailStr
    password: str


class LinkPhoneRequest(BaseModel):
    phone: str


@router.post("/resend/email", status_code=status.HTTP_200_OK)
async def resend_email_otp(
    service: ResendOtpService = Depends(get_resend_otp_service),
    current_user = Depends(get_current_user)
):
    try:
        await service.resend_email_otp(current_user.user_id)
        return {"message": "OTP resent successfully to email"}
    except TooManyRequestsException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
            headers={"Retry-After": str(e.details.get("retry_after_seconds", 900))}
        )
    except (UserNotFoundException, UserEmailRequiredException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/resend/phone", status_code=status.HTTP_200_OK)
async def resend_phone_otp(
    service: ResendOtpService = Depends(get_resend_otp_service),
    current_user = Depends(get_current_user)
):
    try:
        await service.resend_phone_otp(current_user.user_id)
        return {"message": "OTP resent successfully to phone"}
    except TooManyRequestsException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
            headers={"Retry-After": str(e.details.get("retry_after_seconds", 900))}
        )
    except (UserNotFoundException, UserPhoneRequiredException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/link/email", status_code=status.HTTP_201_CREATED)
async def link_email(
    request: LinkEmailRequest,
    service: LinkAuthProviderService = Depends(get_link_auth_provider_service),
    current_user = Depends(get_current_user)
):
    try:
        await service.link_email(current_user.user_id, request.email, request.password)
        return {
            "message": "Email linked successfully. Please verify with OTP sent to your email.",
            "email": request.email
        }
    except (UserNotFoundException, UserAlreadyExistsException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/link/phone", status_code=status.HTTP_201_CREATED)
async def link_phone(
    request: LinkPhoneRequest,
    service: LinkAuthProviderService = Depends(get_link_auth_provider_service),
    current_user = Depends(get_current_user)
):
    try:
        await service.link_phone(current_user.user_id, request.phone)
        return {
            "message": "Phone linked successfully. Please verify with OTP sent to your phone.",
            "phone": request.phone
        }
    except (UserNotFoundException, UserAlreadyExistsException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
