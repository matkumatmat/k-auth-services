from dataclasses import dataclass
from datetime import timedelta

@dataclass
class TokenPolicy:
    access_token_expiry: timedelta
    refresh_token_expiry: timedelta

    @staticmethod
    def default() -> 'TokenPolicy':
        return TokenPolicy(
            access_token_expiry=timedelta(hours=1),
            refresh_token_expiry=timedelta(days=7)
        )

    @staticmethod
    def from_config(
        access_hours: int,
        refresh_days: int
    ) -> 'TokenPolicy':
        return TokenPolicy(
            access_token_expiry=timedelta(hours=access_hours),
            refresh_token_expiry=timedelta(days=refresh_days)
        )

    def get_access_token_expiry(self) -> timedelta:
        return self.access_token_expiry

    def get_refresh_token_expiry(self) -> timedelta:
        return self.refresh_token_expiry

    def get_access_token_expiry_seconds(self) -> int:
        return int(self.access_token_expiry.total_seconds())