from dataclasses import dataclass
from datetime import timedelta


@dataclass
class QuotaDefaults:
    fallback_limit: int
    anonymous_limit: int
    reset_period: timedelta

    @staticmethod
    def default() -> "QuotaDefaults":
        return QuotaDefaults(
            fallback_limit=50,
            anonymous_limit=1,
            reset_period=timedelta(days=1)
        )

    @staticmethod
    def from_config(
        fallback_limit: int,
        anonymous_limit: int,
        reset_days: int
    ) -> "QuotaDefaults":
        return QuotaDefaults(
            fallback_limit=fallback_limit,
            anonymous_limit=anonymous_limit,
            reset_period=timedelta(days=reset_days)
        )

    def get_limit_for_plan(self, plan_limit: int | None) -> int:
        return plan_limit if plan_limit is not None else self.fallback_limit

    def get_anonymous_limit(self) -> int:
        return self.anonymous_limit

    def get_reset_period(self) -> timedelta:
        return self.reset_period
