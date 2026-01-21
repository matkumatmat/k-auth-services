from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Service:
    id: UUID
    name: str
    display_name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    def can_be_accessed(self) -> bool:
        return self.is_active
