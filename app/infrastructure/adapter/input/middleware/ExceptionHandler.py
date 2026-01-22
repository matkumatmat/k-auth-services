import structlog
from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import DomainException
from app.shared.Exceptions import DatabaseException


async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    logger = structlog.get_logger()
    logger.warning(
        "domain_exception_caught",
        exception_type=type(exc).__name__,
        status_code=exc.status_code,
        message=exc.message,
        method=request.method,
        path=str(request.url.path)
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )


async def database_exception_handler(request: Request, exc: DatabaseException) -> JSONResponse:
    logger = structlog.get_logger()
    logger.exception(
        "database_exception_caught",
        exception_type=type(exc).__name__,
        message=exc.message,
        method=request.method,
        path=str(request.url.path)
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": exc.message}
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger = structlog.get_logger()
    logger.exception(
        "unhandled_exception_caught",
        exception_type=type(exc).__name__,
        method=request.method,
        path=str(request.url.path)
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error"}
    )
