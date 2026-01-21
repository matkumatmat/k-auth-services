from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.ValueObjects import BillingCycle


@dataclass
class Plan:
    id: UUID
    name: str
    billing_cycle: BillingCycle
    features: list[str]
    rate_limits: dict[str, int]
    quota_limits: dict[str, int]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    def has_feature(self, feature: str) -> bool:
        return feature in self.features

    def get_rate_limit(self, limit_type: str) -> int | None:
        return self.rate_limits.get(limit_type)

    def get_quota_limit(self, quota_type: str) -> int | None:
        return self.quota_limits.get(quota_type)

    def is_lifetime_plan(self) -> bool:
        return self.billing_cycle == BillingCycle.LIFETIME
