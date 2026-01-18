from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.application.service.AuthenticationService import AuthenticationService
from app.application.service.RefreshTokenService import RefreshTokenService
from app.application.service.RevokeSessionService import RevokeSessionService
from app.application.service.UserRegistrationService import UserRegistrationService
from app.infrastructure.dependencies import (
    get_authentication_service,
    get_refresh_token_service,
    get_revoke_session_service,
    get_user_registration_service
)
from app.shared.Exceptions import (
    AuthenticationException,
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterEmailRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterPhoneRequest(BaseModel):
    phone: str


class LoginEmailRequest(BaseModel):
    email: EmailStr
    password: str
    device_info: str | None = None
    ip_address: str | None = None


class LoginPhoneRequest(BaseModel):
    phone: str
    otp_code: str
    device_info: str | None = None
    ip_address: str | None = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    session_id: str | None = None


class AuthResponse(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"


@router.post("/register/email", status_code=status.HTTP_201_CREATED)
async def register_with_email(
    request: RegisterEmailRequest,
    service: UserRegistrationService = Depends(get_user_registration_service)
):
    try:
        user = await service.execute_with_email(request.email, request.password)
        return {
            "user_id": str(user.id),
            "email": user.email,
            "is_verified": user.is_verified,
            "message": "User registered successfully. Please verify your email."
        }
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/register/phone", status_code=status.HTTP_201_CREATED)
async def register_with_phone(
    request: RegisterPhoneRequest,
    service: UserRegistrationService = Depends(get_user_registration_service)
):
    try:
        user = await service.execute_with_phone(request.phone)
        return {
            "user_id": str(user.id),
            "phone": user.phone,
            "is_verified": user.is_verified,
            "message": "User registered successfully. Please verify your phone."
        }
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login/email", response_model=AuthResponse)
async def login_with_email(
    request: LoginEmailRequest,
    service: AuthenticationService = Depends(get_authentication_service)
):
    try:
        result = await service.execute_with_email(
            request.email,
            request.password,
            request.device_info or "unknown",
            request.ip_address or "0.0.0.0"
        )
        return AuthResponse(
            user_id=str(result.user_id),
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            expires_in=result.expires_in,
            token_type=result.token_type
        )
    except (UserNotFoundException, InvalidCredentialsException) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.post("/login/phone", response_model=AuthResponse)
async def login_with_phone(
    request: LoginPhoneRequest,
    service: AuthenticationService = Depends(get_authentication_service)
):
    try:
        result = await service.execute_with_phone(
            request.phone,
            request.otp_code,
            request.device_info or "unknown",
            request.ip_address or "0.0.0.0"
        )
        return AuthResponse(
            user_id=str(result.user_id),
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            expires_in=result.expires_in,
            token_type=result.token_type
        )
    except (UserNotFoundException, InvalidCredentialsException) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.post("/refresh", response_model=AuthResponse)
async def refresh_access_token(
    request: RefreshTokenRequest,
    service: RefreshTokenService = Depends(get_refresh_token_service)
):
    try:
        result = await service.execute(request.refresh_token)
        return AuthResponse(
            user_id=str(result.user_id),
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            expires_in=result.expires_in,
            token_type=result.token_type
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: LogoutRequest,
    service: RevokeSessionService = Depends(get_revoke_session_service)
):
    try:
        if request.session_id:
            from uuid import UUID
            await service.execute(UUID(request.session_id))
        return None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
