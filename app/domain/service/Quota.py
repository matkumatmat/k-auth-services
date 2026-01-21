from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Quota:
    id: UUID
    user_id: UUID
    service_name: str
    quota_type: str
    current_usage: int
    limit: int
    reset_at: datetime
    created_at: datetime
    updated_at: datetime

    def is_exceeded(self) -> bool:
        return self.current_usage >= self.limit

    def remaining(self) -> int:
        return max(0, self.limit - self.current_usage)

    def usage_percentage(self) -> float:
        if self.limit == 0:
            return 100.0
        return (self.current_usage / self.limit) * 100.0

    def can_consume(self, amount: int) -> bool:
        return (self.current_usage + amount) <= self.limit

    def needs_reset(self, current_time: datetime) -> bool:
        return current_time >= self.reset_at
