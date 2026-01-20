from http import HTTPStatus
from typing import Any

from app.domain.exceptions.BaseException import DomainException


class UserNotFoundException(DomainException):
    def __init__(self, details: dict[str, Any] | None = None):
        super().__init__(
            message="User not found",
            status_code=HTTPStatus.NOT_FOUND,
            details=details,
        )


class UserAlreadyExistsException(DomainException):
    def __init__(self, details: dict[str, Any] | None = None):
        super().__init__(
            message="User already exists with this contact",
            status_code=HTTPStatus.CONFLICT,
            details=details,
        )


class InvalidContactFormatException(DomainException):
    def __init__(self, contact: str):
        super().__init__(
            message="Invalid contact format. Provide valid email or phone number",
            status_code=HTTPStatus.BAD_REQUEST,
            details={"contact": contact},
        )


class PasswordRequiredException(DomainException):
    def __init__(self):
        super().__init__(
            message="Password is required for email registration",
            status_code=HTTPStatus.BAD_REQUEST,
        )


class UserEmailRequiredException(DomainException):
    def __init__(self, user_id: str):
        super().__init__(
            message="User does not have email configured",
            status_code=HTTPStatus.BAD_REQUEST,
            details={"user_id": user_id},
        )


class UserPhoneRequiredException(DomainException):
    def __init__(self, user_id: str):
        super().__init__(
            message="User does not have phone configured",
            status_code=HTTPStatus.BAD_REQUEST,
            details={"user_id": user_id},
        )


class UserNotVerifiedException(DomainException):
    def __init__(self, user_id: str):
        super().__init__(
            message="User account is not verified",
            status_code=HTTPStatus.FORBIDDEN,
            details={"user_id": user_id},
        )


class InvalidOtpCodeException(DomainException):
    def __init__(self, reason: str = "Invalid or expired OTP code"):
        super().__init__(
            message=reason,
            status_code=HTTPStatus.BAD_REQUEST,
        )
