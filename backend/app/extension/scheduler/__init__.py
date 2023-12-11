#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import asyncio
from functools import wraps
from asyncio import ensure_future
from typing import Optional, Callable
from starlette.concurrency import run_in_threadpool
# local
from app.extension.logger import logger


def scheduler(
        *,
        seconds: float,
        immediate: bool = False,
        raise_exceptions: bool = True,
        max_repetitions: Optional[int] = None,
) -> Callable:
    """
    usage: execute the function periodically
    @scheduler(seconds=60, immediate=True)
    async def backup():
        pass
    """
    def decorator(func: Callable) -> Callable:
        is_coroutine = asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def wrapped() -> None:
            repetitions = 0

            async def loop() -> None:
                nonlocal repetitions
                if immediate:
                    await asyncio.sleep(seconds)
                while max_repetitions is None or repetitions < max_repetitions:
                    try:
                        if is_coroutine:
                            await func()
                        else:
                            await run_in_threadpool(func)
                        repetitions += 1
                    except Exception as exc:
                        logger.error(f"执行重复任务异常: {exc}")
                        if raise_exceptions:
                            raise exc
                    await asyncio.sleep(seconds)

            ensure_future(loop())

        return wrapped

    return decorator
