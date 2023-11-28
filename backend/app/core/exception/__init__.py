#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from fastapi import HTTPException
from starlette.requests import Request

from app.core.extension.logger import logger
from app.core.response import ApiResponse, InternalErrorException, response_dict


async def global_exception(request: Request, exc: Exception) -> ApiResponse:
    """handle global internal exceptions"""
    if hasattr(request.state, "request_id"):
        request_id = request.state.request_id
    else:
        request_id = None
        logger.warn("request_id 获取失败 请确认对应APIRouter使用了logMiddleware")
    logger.error(f"{request_id} Exception: {exc}")
    return InternalErrorException(data=str(exc))


async def http_exception(request: Request, exc: HTTPException) -> ApiResponse:
    """handle http exceptions"""
    return response_dict[exc.status_code](data=str(exc), msg=exc.detail)


exception_handlers = {Exception: global_exception, HTTPException: http_exception}
