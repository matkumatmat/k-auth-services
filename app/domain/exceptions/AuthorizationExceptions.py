from http import HTTPStatus
from typing import Any

from app.domain.exceptions.BaseException import DomainException


class AuthorizationException(DomainException):
    def __init__(self, message: str = "Authorization failed", details: dict[str, Any] | None = None):
        super().__init__(
            message=message,
            status_code=HTTPStatus.FORBIDDEN,
            details=details,
        )


class InsufficientQuotaException(DomainException):
    def __init__(self, quota_type: str, current: int, required: int):
        super().__init__(
            message=f"Insufficient {quota_type} quota",
            status_code=HTTPStatus.FORBIDDEN,
            details={
                "quota_type": quota_type,
                "current": current,
                "required": required,
            },
        )


class PlanLimitExceededException(DomainException):
    def __init__(self, plan_name: str, limit_type: str):
        super().__init__(
            message=f"Plan limit exceeded for {limit_type}",
            status_code=HTTPStatus.FORBIDDEN,
            details={
                "plan_name": plan_name,
                "limit_type": limit_type,
            },
        )


class AccessDeniedException(DomainException):
    def __init__(self, resource: str):
        super().__init__(
            message=f"Access denied to {resource}",
            status_code=HTTPStatus.FORBIDDEN,
            details={"resource": resource},
        )
