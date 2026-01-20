from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.application.service.QuotaManagementService import QuotaManagementService
from app.application.service.ServiceAccessValidationService import ServiceAccessValidationService
from app.application.service.TokenValidationService import TokenValidationService
from app.infrastructure.dependencies import (
    get_current_user,
    get_quota_management_service,
    get_service_access_validation_service,
    get_token_validation_service
)
from app.domain.exceptions import (
    AccessDeniedException,
    InsufficientQuotaException,
)

router = APIRouter(prefix="/validate", tags=["Validation"])


class ValidateTokenRequest(BaseModel):
    token: str


class ValidateTokenResponse(BaseModel):
    is_valid: bool
    user_id: str | None = None
    session_id: str | None = None
    error_message: str | None = None


class ValidateServiceAccessRequest(BaseModel):
    service_name: str


class ValidateServiceAccessResponse(BaseModel):
    is_allowed: bool
    allowed_features: list[str] | None = None
    error_message: str | None = None


class CheckQuotaRequest(BaseModel):
    service_name: str
    quota_type: str = "api_calls_per_day"
    amount: int = 1


class ConsumeQuotaRequest(BaseModel):
    service_name: str
    quota_type: str = "api_calls_per_day"
    amount: int = 1


class QuotaResponse(BaseModel):
    can_proceed: bool
    current_usage: int
    limit: int
    remaining: int
    reset_at: str
    error_message: str | None = None


@router.post("/token", response_model=ValidateTokenResponse)
async def validate_token(
    request: ValidateTokenRequest,
    service: TokenValidationService = Depends(get_token_validation_service)
):
    result = await service.execute(request.token)
    return ValidateTokenResponse(
        is_valid=result.is_valid,
        user_id=str(result.user_id) if result.user_id else None,
        session_id=str(result.session_id) if result.session_id else None,
        error_message=result.error_message
    )


@router.post("/service-access", response_model=ValidateServiceAccessResponse)
async def validate_service_access(
    request: ValidateServiceAccessRequest,
    service: ServiceAccessValidationService = Depends(get_service_access_validation_service),
    current_user = Depends(get_current_user)
):
    result = await service.execute(current_user.user_id, request.service_name)
    return ValidateServiceAccessResponse(
        is_allowed=result.is_allowed,
        allowed_features=result.allowed_features,
        error_message=result.error_message
    )


@router.post("/quota/check", response_model=QuotaResponse)
async def check_quota(
    request: CheckQuotaRequest,
    service: QuotaManagementService = Depends(get_quota_management_service),
    current_user = Depends(get_current_user)
):
    result = await service.execute(
        current_user.user_id,
        request.service_name,
        request.quota_type,
        request.amount
    )
    return QuotaResponse(
        can_proceed=result.can_proceed,
        current_usage=result.current_usage,
        limit=result.limit,
        remaining=result.remaining,
        reset_at=result.reset_at,
        error_message=result.error_message
    )


@router.post("/quota/consume", response_model=QuotaResponse)
async def consume_quota(
    request: ConsumeQuotaRequest,
    service: QuotaManagementService = Depends(get_quota_management_service),
    current_user = Depends(get_current_user)
):
    try:
        await service.consume(
            current_user.user_id,
            request.service_name,
            request.quota_type,
            request.amount
        )

        check_result = await service.execute(
            current_user.user_id,
            request.service_name,
            request.quota_type,
            0
        )

        return QuotaResponse(
            can_proceed=True,
            current_usage=check_result.current_usage,
            limit=check_result.limit,
            remaining=check_result.remaining,
            reset_at=check_result.reset_at,
            error_message=None
        )
    except (InsufficientQuotaException, AccessDeniedException) as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
