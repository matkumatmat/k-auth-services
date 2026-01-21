from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class ExternalTransactionLog:
    id: UUID
    user_id: UUID | None
    external_service: str
    request_type: str
    request_payload: dict[str, str | int | bool]
    response_status: int
    response_body: dict[str, str | int | bool] | None
    duration_ms: int
    idempotency_key: str | None
    error_message: str | None
    created_at: datetime

    def is_successful(self) -> bool:
        return 200 <= self.response_status < 300

    def is_client_error(self) -> bool:
        return 400 <= self.response_status < 500

    def is_server_error(self) -> bool:
        return self.response_status >= 500

    def has_error(self) -> bool:
        return self.error_message is not None
