from http import HTTPStatus

from app.domain.exceptions.BaseException import DomainException


class TooManyRequestsException(DomainException):
    def __init__(self, retry_after: int | None = None, limit_type: str = "requests"):
        message = f"Too many {limit_type}"
        details = {"limit_type": limit_type}

        if retry_after:
            details["retry_after_seconds"] = retry_after
            message = f"{message}. Retry after {retry_after} seconds"

        super().__init__(
            message=message,
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
            details=details,
        )
