from http import HTTPStatus

from app.domain.exceptions.BaseException import DomainException


class AuthenticationException(DomainException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=HTTPStatus.UNAUTHORIZED,
        )


class InvalidCredentialsException(DomainException):
    def __init__(self):
        super().__init__(
            message="Invalid credentials provided",
            status_code=HTTPStatus.UNAUTHORIZED,
        )


class TokenExpiredException(DomainException):
    def __init__(self):
        super().__init__(
            message="Token has expired",
            status_code=HTTPStatus.UNAUTHORIZED,
        )


class TokenInvalidException(DomainException):
    def __init__(self, reason: str = "Token is invalid"):
        super().__init__(
            message=reason,
            status_code=HTTPStatus.UNAUTHORIZED,
        )


class SessionNotFoundException(DomainException):
    def __init__(self, session_id: str):
        super().__init__(
            message="Session not found",
            status_code=HTTPStatus.UNAUTHORIZED,
            details={"session_id": session_id},
        )


class SessionExpiredException(DomainException):
    def __init__(self, session_id: str):
        super().__init__(
            message="Session has expired",
            status_code=HTTPStatus.UNAUTHORIZED,
            details={"session_id": session_id},
        )


class SessionInactiveException(DomainException):
    def __init__(self, session_id: str):
        super().__init__(
            message="Session is inactive",
            status_code=HTTPStatus.UNAUTHORIZED,
            details={"session_id": session_id},
        )
