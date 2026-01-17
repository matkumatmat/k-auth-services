from dataclasses import dataclass


@dataclass
class ServiceAccessResult:
    is_allowed: bool
    allowed_features: list[str] | None = None
    error_message: str | None = None
