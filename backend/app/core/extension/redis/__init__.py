#! /usr/bin/env python
# -*- coding: utf-8 -*-#-

# python 3.11 competitive pattern
from redis import asyncio as aioredis

# local
from app.core.config import settings


class redisCli:
    def __init__(self):
        self.redis: aioredis.Redis = None

    def init_redis_connect(self) -> aioredis.Redis:
        """initialize connection"""
        if self.redis is None:
            self.redis = aioredis.from_url(
                f"redis://{settings.REDIS_HOST}", encoding="utf-8", decode_responses=True
            )

    async def close_redis_connect(self) -> None:
        """close connection"""
        if self.redis is not None:
            await self.redis.close()
            self.redis = None


cli = redisCli()

__all__ = ["cli"]
