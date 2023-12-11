#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import time
from http import HTTPStatus
from fastapi import Request, HTTPException
# local
from app.core.config import settings
from app.utils.string_helper import url_to_resource
from app.extension.redis import cli as redisCli


class throttle:
    """Dependency to limit rate"""

    def __init__(self, times: int, seconds: int):
        self.times = times
        self.seconds = seconds

    async def __call__(self, request: Request):
        async with redisCli.redis.client() as conn:
            current_time = int(time.time())
            path = url_to_resource(request.url.path)
            project_name = settings.PROJECT_NAME.replace(' ', '')
            key = f"{project_name}:throttle:{request.client.host}-{path}"
            count = await conn.zcount(key, current_time - self.seconds, current_time)
            if count >= self.times:
                raise HTTPException(status_code=HTTPStatus.TOO_MANY_REQUESTS)
            await conn.zadd(key, {current_time: current_time})
            await conn.zremrangebyscore(key, 0, current_time - self.seconds)
