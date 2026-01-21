from abc import ABC, abstractmethod
from typing import Any, Protocol
from uuid import UUID

import structlog


class LoggerProtocol(Protocol):
    def debug(self, event: str, **kwargs: Any) -> None:
        ...

    def info(self, event: str, **kwargs: Any) -> None:
        ...

    def warning(self, event: str, **kwargs: Any) -> None:
        ...

    def error(self, event: str, **kwargs: Any) -> None:
        ...

    def critical(self, event: str, **kwargs: Any) -> None:
        ...


class ILogger(ABC):
    @abstractmethod
    def debug(self, event: str, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def info(self, event: str, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def warning(self, event: str, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def error(self, event: str, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def critical(self, event: str, **kwargs: Any) -> None:
        raise NotImplementedError


class StructLogger(ILogger):
    def __init__(self, logger_name: str | None = None):
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer()
            ],
            wrapper_class=structlog.make_filtering_bound_logger(min_level=10),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
        self._logger = structlog.get_logger(logger_name)

    def debug(self, event: str, **kwargs: Any) -> None:
        self._logger.debug(event, **kwargs)

    def info(self, event: str, **kwargs: Any) -> None:
        self._logger.info(event, **kwargs)

    def warning(self, event: str, **kwargs: Any) -> None:
        self._logger.warning(event, **kwargs)

    def error(self, event: str, **kwargs: Any) -> None:
        self._logger.error(event, **kwargs)

    def critical(self, event: str, **kwargs: Any) -> None:
        self._logger.critical(event, **kwargs)


class DatabaseTransactionLoggerProtocol(Protocol):
    def log_transaction(
        self,
        user_id: UUID | None,
        table_name: str,
        operation: str,
        record_id: UUID,
        old_value: dict[str, Any] | None,
        new_value: dict[str, Any] | None,
        transaction_id: UUID
    ) -> None:
        ...


class IDatabaseTransactionLogger(ABC):
    @abstractmethod
    def log_transaction(
        self,
        user_id: UUID | None,
        table_name: str,
        operation: str,
        record_id: UUID,
        old_value: dict[str, Any] | None,
        new_value: dict[str, Any] | None,
        transaction_id: UUID
    ) -> None:
        raise NotImplementedError


class ExternalTransactionLoggerProtocol(Protocol):
    def log_request(
        self,
        user_id: UUID | None,
        external_service: str,
        request_type: str,
        request_payload: dict[str, Any],
        response_status: int,
        response_body: dict[str, Any] | None,
        duration_ms: int,
        idempotency_key: str | None,
        error_message: str | None
    ) -> None:
        ...


class IExternalTransactionLogger(ABC):
    @abstractmethod
    def log_request(
        self,
        user_id: UUID | None,
        external_service: str,
        request_type: str,
        request_payload: dict[str, Any],
        response_status: int,
        response_body: dict[str, Any] | None,
        duration_ms: int,
        idempotency_key: str | None,
        error_message: str | None
    ) -> None:
        raise NotImplementedError


class UserBehaviorLoggerProtocol(Protocol):
    def log_action(
        self,
        user_id: UUID | None,
        action: str,
        service_name: str | None,
        ip_address: str,
        user_agent: str,
        device_fingerprint: str | None,
        geolocation: dict[str, Any] | None,
        metadata: dict[str, Any] | None
    ) -> None:
        ...


class IUserBehaviorLogger(ABC):
    @abstractmethod
    def log_action(
        self,
        user_id: UUID | None,
        action: str,
        service_name: str | None,
        ip_address: str,
        user_agent: str,
        device_fingerprint: str | None,
        geolocation: dict[str, Any] | None,
        metadata: dict[str, Any] | None
    ) -> None:
        raise NotImplementedError
