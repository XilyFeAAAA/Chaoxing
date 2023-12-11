#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
# local
import uuid
import time
from typing import Callable
from starlette.requests import Request
from starlette.responses import Response
from fastapi.routing import APIRoute
from app.extension.logger import logger


class logMiddleware(APIRoute):
    """middleware to create an uid for each request and add log"""

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request_id = str(uuid.uuid4())
            request.state.request_id = request_id
            logger.info(
                f"from {request.client} to {request.url} {request.method} uuid: {request_id} "
            )
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            logger.info(f"{request_id} Response Log {duration}s\n")
            return response

        return custom_route_handler
