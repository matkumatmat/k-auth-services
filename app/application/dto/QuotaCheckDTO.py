from dataclasses import dataclass


@dataclass
class QuotaCheckResult:
    can_proceed: bool
    current_usage: int
    limit: int
    remaining: int
    reset_at: str | None = None
    error_message: str | None = None
