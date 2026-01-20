from http import HTTPStatus
from typing import Any


class DomainException(Exception):
    def __init__(
        self,
        message: str,
        status_code: HTTPStatus = HTTPStatus.BAD_REQUEST,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
