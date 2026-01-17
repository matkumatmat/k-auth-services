from http import HTTPStatus
from typing import Any


class BaseApplicationException(Exception):
    def __init__(self, message: str, status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR, details: dict[str, Any] | None = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationException(BaseApplicationException):
    def __init__(self, message: str = "Authentication failed", details: dict[str, Any] | None = None):
        super().__init__(message=message, status_code=HTTPStatus.UNAUTHORIZED, details=details)


class AuthorizationException(BaseApplicationException):
    def __init__(self, message: str = "Authorization failed", details: dict[str, Any] | None = None):
        super().__init__(message=message, status_code=HTTPStatus.FORBIDDEN, details=details)


class InvalidCredentialsException(AuthenticationException):
    def __init__(self, message: str = "Invalid credentials", details: dict[str, Any] | None = None):
        super().__init__(message=message, details=details)


class TokenExpiredException(AuthenticationException):
    def __init__(self, message: str = "Token has expired", details: dict[str, Any] | None = None):
        super().__init__(message=message, details=details)


class TokenInvalidException(AuthenticationException):
    def __init__(self, message: str = "Token is invalid", details: dict[str, Any] | None = None):
        super().__init__(message=message, details=details)


class UserNotFoundException(BaseApplicationException):
    def __init__(self, message: str = "User not found", details: dict[str, Any] | None = None):
        super().__init__(message=message, status_code=HTTPStatus.NOT_FOUND, details=details)


class UserAlreadyExistsException(BaseApplicationException):
    def __init__(self, message: str = "User already exists", details: dict[str, Any] | None = None):
        super().__init__(message=message, status_code=HTTPStatus.CONFLICT, details=details)


class InsufficientQuotaException(AuthorizationException):
    def __init__(self, message: str = "Insufficient quota", details: dict[str, Any] | None = None):
        super().__init__(message=message, details=details)


class PlanLimitExceededException(AuthorizationException):
    def __init__(self, message: str = "Plan limit exceeded", details: dict[str, Any] | None = None):
        super().__init__(message=message, details=details)


class EncryptionException(BaseApplicationException):
    def __init__(self, message: str = "Encryption operation failed", details: dict[str, Any] | None = None):
        super().__init__(message=message, status_code=HTTPStatus.INTERNAL_SERVER_ERROR, details=details)


class DecryptionException(BaseApplicationException):
    def __init__(self, message: str = "Decryption operation failed", details: dict[str, Any] | None = None):
        super().__init__(message=message, status_code=HTTPStatus.INTERNAL_SERVER_ERROR, details=details)
