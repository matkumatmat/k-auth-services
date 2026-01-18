from fastapi import APIRouter, Depends, HTTPException

from app.application.dto.AuthenticationDTO import AuthenticationRequest
from app.application.usecase.AuthenticateUserUseCase import AuthenticateUserUseCase
from app.application.usecase.RegisterUserUseCase import RegisterUserUseCase
from app.infrastructure.dependencies import get_authenticate_user_use_case, get_register_user_use_case


router = APIRouter()

@router.post("/register")
async def register_user(
    request: AuthenticationRequest,
    register_user_use_case: RegisterUserUseCase = Depends(get_register_user_use_case),
):
    try:
        user = await register_user_use_case.execute_with_email(request.email, request.password)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(
    request: AuthenticationRequest,
    authenticate_user_use_case: AuthenticateUserUseCase = Depends(get_authenticate_user_use_case),
):
    try:
        result = await authenticate_user_use_case.execute_with_email(
            request.email, request.password, request.device_info, request.ip_address
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
