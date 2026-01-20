import json
from typing import Any

import redis.asyncio as aioredis

from app.infrastructure.config.EnvConfig import RedisConfig


class RedisClient:
    def __init__(self, config: RedisConfig):
        self._pool = aioredis.ConnectionPool(
            host=config.host,
            port=config.port,
            db=config.db,
            password=config.password,
            decode_responses=config.decode_responses,
            max_connections=config.max_connections
        )
        self._client = aioredis.Redis(connection_pool=self._pool)

    async def get(self, key: str) -> str | None:
        return await self._client.get(key)

    async def set(self, key: str, value: str | dict, ex: int | None = None) -> None:
        if isinstance(value, dict):
            value = json.dumps(value)
        await self._client.set(key, value, ex=ex)

    async def delete(self, key: str) -> None:
        await self._client.delete(key)

    async def exists(self, key: str) -> bool:
        return await self._client.exists(key) > 0

    async def incr(self, key: str, ex: int | None = None) -> int:
        value = await self._client.incr(key)
        if ex and value == 1:
            await self._client.expire(key, ex)
        return value

    async def ttl(self, key: str) -> int:
        return await self._client.ttl(key)

    async def close(self):
        await self._client.aclose()
        await self._pool.aclose()
