#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from fastapi import HTTPException
from starlette.requests import Request
# local
from app.core.response import ApiResponse, response_dict


async def http_exception(request: Request, exc: HTTPException) -> ApiResponse:
    """handle http exceptions"""
    return response_dict[exc.status_code](data=str(exc), msg=exc.detail)

