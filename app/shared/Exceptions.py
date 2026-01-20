from http import HTTPStatus
from typing import Any


class BaseApplicationException(Exception):
    def __init__(self, message: str, status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR, details: dict[str, Any] | None = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class EncryptionException(BaseApplicationException):
    def __init__(self, message: str = "Encryption operation failed", details: dict[str, Any] | None = None):
        super().__init__(message=message, status_code=HTTPStatus.INTERNAL_SERVER_ERROR, details=details)


class DecryptionException(BaseApplicationException):
    def __init__(self, message: str = "Decryption operation failed", details: dict[str, Any] | None = None):
        super().__init__(message=message, status_code=HTTPStatus.INTERNAL_SERVER_ERROR, details=details)


class DatabaseException(BaseApplicationException):
    def __init__(self, message: str = "Database operation failed", details: dict[str, Any] | None = None):
        super().__init__(message=message, status_code=HTTPStatus.INTERNAL_SERVER_ERROR, details=details)
