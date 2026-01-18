from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.shared.Exceptions import (
    AuthenticationException,
    DatabaseException,
    DomainException,
    InsufficientQuotaException,
    InvalidCredentialsException,
    TokenExpiredException,
    TokenInvalidException,
    UserAlreadyExistsException,
    UserNotFoundException
)


async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    exception_status_mapping = {
        UserNotFoundException: status.HTTP_404_NOT_FOUND,
        UserAlreadyExistsException: status.HTTP_409_CONFLICT,
        InvalidCredentialsException: status.HTTP_401_UNAUTHORIZED,
        AuthenticationException: status.HTTP_403_FORBIDDEN,
        TokenExpiredException: status.HTTP_401_UNAUTHORIZED,
        TokenInvalidException: status.HTTP_401_UNAUTHORIZED,
        InsufficientQuotaException: status.HTTP_429_TOO_MANY_REQUESTS,
        DatabaseException: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }

    status_code = exception_status_mapping.get(type(exc), status.HTTP_400_BAD_REQUEST)

    return JSONResponse(
        status_code=status_code,
        content={
            "error": exc.message,
            "details": exc.details if hasattr(exc, "details") else None
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "details": str(exc)
        }
    )
