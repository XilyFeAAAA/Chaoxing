#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import traceback
from starlette.requests import Request
# local
from .http import http_exception, HTTPException
from app.extension.logger import logger
from app.core.response import ApiResponse, InternalErrorException


async def global_exception(request: Request, exc: Exception) -> ApiResponse:
    """handle global internal exceptions"""
    if hasattr(request.state, "request_id"):
        request_id = request.state.request_id
    else:
        request_id = None
        logger.warn("request_id 获取失败 请确认对应APIRouter使用了logMiddleware")
    logger.error(f"{request_id} Exception: {exc}")
    return InternalErrorException(data=str(exc))


exception_handlers = {
    Exception: global_exception,
    HTTPException: http_exception,
}
