from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import DomainException
from app.shared.Exceptions import DatabaseException


async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details if hasattr(exc, "details") else None
        }
    )


async def database_exception_handler(request: Request, exc: DatabaseException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
