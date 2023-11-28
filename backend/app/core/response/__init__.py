#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import sys
import inspect
from http import HTTPStatus
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class ApiResponse(JSONResponse):
    """define generic http response"""
    http_status_code: int = HTTPStatus.BAD_GATEWAY
    code: int = HTTPStatus.BAD_GATEWAY
    data: any = None
    msg: str = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, http_status_code=None, data=None, msg=None, **options):
        if msg:
            self.msg = msg
        if data:
            if isinstance(data, BaseModel):
                self.data = jsonable_encoder(data)
            else:
                self.data = data
        if http_status_code:
            self.http_status_code = http_status_code

        # return content body
        body = dict(
            msg=self.msg,
            code=self.code,
            data=self.data
        )
        super(ApiResponse, self).__init__(status_code=self.http_status_code, content=body, **options)


class BadrequestException(ApiResponse):
    http_status_code = HTTPStatus.BAD_REQUEST
    code = HTTPStatus.BAD_REQUEST
    msg = HTTPStatus.BAD_REQUEST.description


class ParameterException(ApiResponse):
    http_status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    msg = HTTPStatus.UNPROCESSABLE_ENTITY.description


class UnauthorizedException(ApiResponse):
    http_status_code = HTTPStatus.UNAUTHORIZED
    code = HTTPStatus.UNAUTHORIZED
    msg = HTTPStatus.UNAUTHORIZED.description


class ForbiddenException(ApiResponse):
    http_status_code = HTTPStatus.FORBIDDEN
    code = HTTPStatus.FORBIDDEN
    msg = HTTPStatus.FORBIDDEN.description


class NotfoundException(ApiResponse):
    http_status_code = HTTPStatus.NOT_FOUND
    code = HTTPStatus.NOT_FOUND
    msg = HTTPStatus.NOT_FOUND.description


class MethodnotallowedException(ApiResponse):
    http_status_code = HTTPStatus.METHOD_NOT_ALLOWED
    code = HTTPStatus.METHOD_NOT_ALLOWED
    msg = HTTPStatus.METHOD_NOT_ALLOWED.description


class InternalErrorException(ApiResponse):
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    data = None
    msg = HTTPStatus.INTERNAL_SERVER_ERROR.description


class RateLimitApiException(ApiResponse):
    http_status_code = HTTPStatus.TOO_MANY_REQUESTS
    code = HTTPStatus.TOO_MANY_REQUESTS
    msg = HTTPStatus.TOO_MANY_REQUESTS.description


class ConflictException(ApiResponse):
    http_status_code = HTTPStatus.CONFLICT
    code = HTTPStatus.CONFLICT
    msg = HTTPStatus.CONFLICT.description


class CustomizeApiResponse(ApiResponse):
    http_status_code = HTTPStatus.OK
    code = HTTPStatus.OK
    data = None
    msg = HTTPStatus.OK.description


module_classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
response_classes = [cls for name, cls in module_classes if issubclass(cls, ApiResponse)]
response_dict = {cls.code: cls for cls in response_classes}
