from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.ValueObjects import DatabaseOperation


@dataclass
class DatabaseTransactionLog:
    id: UUID
    user_id: UUID | None
    table_name: str
    operation: DatabaseOperation
    record_id: UUID
    old_value: dict[str, str | int | bool | None] | None
    new_value: dict[str, str | int | bool | None] | None
    transaction_id: UUID
    created_at: datetime

    def is_insert_operation(self) -> bool:
        return self.operation == DatabaseOperation.INSERT

    def is_update_operation(self) -> bool:
        return self.operation == DatabaseOperation.UPDATE

    def is_delete_operation(self) -> bool:
        return self.operation == DatabaseOperation.DELETE
