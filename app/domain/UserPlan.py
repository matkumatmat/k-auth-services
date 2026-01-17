from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.ValueObjects import UserPlanStatus


@dataclass
class UserPlan:
    id: UUID
    user_id: UUID
    plan_id: UUID
    status: UserPlanStatus
    started_at: datetime
    expires_at: datetime | None
    auto_renew: bool
    payment_gateway: str | None
    payment_gateway_subscription_id: str | None
    created_at: datetime
    updated_at: datetime

    def is_active(self, current_time: datetime) -> bool:
        if self.status != UserPlanStatus.ACTIVE:
            return False
        if self.expires_at is None:
            return True
        return current_time < self.expires_at

    def is_expired(self, current_time: datetime) -> bool:
        if self.expires_at is None:
            return False
        return current_time > self.expires_at

    def is_suspended(self) -> bool:
        return self.status == UserPlanStatus.SUSPENDED

    def is_cancelled(self) -> bool:
        return self.status == UserPlanStatus.CANCELLED
