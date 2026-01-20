from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.application.service.LinkAuthProviderService import LinkAuthProviderService
from app.application.service.ResendOtpService import ResendOtpService
from app.infrastructure.dependencies import (
    get_link_auth_provider_service,
    get_resend_otp_service
)
from app.shared.Exceptions import TooManyRequestsException, UserAlreadyExistsException, UserNotFoundException

router = APIRouter(prefix="/otp", tags=["OTP"])


class ResendEmailOtpRequest(BaseModel):
    user_id: str


class ResendPhoneOtpRequest(BaseModel):
    user_id: str


class LinkEmailRequest(BaseModel):
    user_id: str
    email: EmailStr
    password: str


class LinkPhoneRequest(BaseModel):
    user_id: str
    phone: str


@router.post("/resend/email", status_code=status.HTTP_200_OK)
async def resend_email_otp(
    request: ResendEmailOtpRequest,
    service: ResendOtpService = Depends(get_resend_otp_service)
):
    try:
        user_id = UUID(request.user_id)
        await service.resend_email_otp(user_id)
        return {"message": "OTP resent successfully to email"}
    except TooManyRequestsException as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=e.message,
            headers={"Retry-After": str(e.details.get("retry_after", 900))}
        )
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id format")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/resend/phone", status_code=status.HTTP_200_OK)
async def resend_phone_otp(
    request: ResendPhoneOtpRequest,
    service: ResendOtpService = Depends(get_resend_otp_service)
):
    try:
        user_id = UUID(request.user_id)
        await service.resend_phone_otp(user_id)
        return {"message": "OTP resent successfully to phone"}
    except TooManyRequestsException as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=e.message,
            headers={"Retry-After": str(e.details.get("retry_after", 900))}
        )
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id format")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/link/email", status_code=status.HTTP_201_CREATED)
async def link_email(
    request: LinkEmailRequest,
    service: LinkAuthProviderService = Depends(get_link_auth_provider_service)
):
    try:
        user_id = UUID(request.user_id)
        await service.link_email(user_id, request.email, request.password)
        return {
            "message": "Email linked successfully. Please verify with OTP sent to your email.",
            "email": request.email
        }
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id format")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/link/phone", status_code=status.HTTP_201_CREATED)
async def link_phone(
    request: LinkPhoneRequest,
    service: LinkAuthProviderService = Depends(get_link_auth_provider_service)
):
    try:
        user_id = UUID(request.user_id)
        await service.link_phone(user_id, request.phone)
        return {
            "message": "Phone linked successfully. Please verify with OTP sent to your phone.",
            "phone": request.phone
        }
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user_id format")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
