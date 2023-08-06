from typing import Any, Union, Optional

from datetime import datetime
from redis.asyncio import Redis

from .base import BaseAsyncBackend


class RedisBackend(BaseAsyncBackend):

    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def get(self, key: str) -> Optional[Any]:
        return await self.redis.get(key)

    async def set(self, key: str, value: Any, ex: Union[int, datetime, None] = None) -> Optional[bool]:
        return await self.redis.set(key, value, ex)

    async def update(self, key: str, value: Any) -> Optional[bool]:
        return await self.redis.set(key, value, keepttl=True)

    async def delete(self, key: str) -> int:
        return await self.redis.delete(key)
