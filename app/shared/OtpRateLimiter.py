from uuid import UUID

from app.infrastructure.config.database.redis.RedisClient import RedisClient
from app.domain.exceptions import TooManyRequestsException


class OtpRateLimiter:
    def __init__(self, redis_client: RedisClient, max_requests: int = 3, window_seconds: int = 900):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def check_rate_limit(self, user_id: UUID, operation: str = "otp_resend") -> None:
        key = f"{operation}:{str(user_id)}"
        count = await self.redis.incr(key, ex=self.window_seconds)

        if count > self.max_requests:
            remaining_ttl = await self.redis.ttl(key)
            retry_after = remaining_ttl if remaining_ttl > 0 else self.window_seconds
            raise TooManyRequestsException(
                retry_after=retry_after,
                limit_type=operation.replace('_', ' ')
            )

    async def reset_rate_limit(self, user_id: UUID, operation: str = "otp_resend") -> None:
        key = f"{operation}:{str(user_id)}"
        await self.redis.delete(key)
