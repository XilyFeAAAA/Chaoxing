#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Annotated
from fastapi import APIRouter, Depends
# local
from app.models import User
from app.schemas.request import PaginationIn
from app.schemas.response import UserOut, PaginationOut, UserInfoOut
from app.core.middleware import logMiddleware
from app.core.dependency import permission_required, captcha_required, throttle, login_required, paginated_params
from app.core.response import CustomizeApiResponse
from app.core.extension.scheduler import scheduler

router = APIRouter(route_class=logMiddleware)


@router.post("/action-with-permission", response_model=UserOut)
async def permission_test(current_user: Annotated[User, Depends(permission_required)]) -> CustomizeApiResponse:
    """test function related to permissions"""
    return CustomizeApiResponse(data=UserOut.model_validate(current_user))


@router.post("/action-with-captcha", dependencies=[Depends(captcha_required)])
async def captcha_test() -> CustomizeApiResponse:
    """test function related to permissions"""
    return CustomizeApiResponse()


@router.post("/action-with-logger")
async def logger_test() -> CustomizeApiResponse:
    """test function related to logger"""
    a = int("ddwadw")
    return CustomizeApiResponse()


@router.post("/action-with-throttle", dependencies=[Depends(throttle(times=3, seconds=10))])
async def throttle_test() -> CustomizeApiResponse:
    """test function related to throttle"""
    return CustomizeApiResponse()


@router.get("/action-with-pagination", response_model=PaginationOut[UserInfoOut])
async def pagination_test(current_user: Annotated[User, Depends(login_required)], pagination: Annotated[PaginationIn, Depends(paginated_params)]) -> CustomizeApiResponse:
    """test function related to pagination"""
    res = PaginationOut(size=10, total=100, items=[UserInfoOut.model_validate(current_user.info)])
    return CustomizeApiResponse(data=res)


@scheduler(seconds=5, immediate=True)
async def async_schedule_test():
    print("test_async")


@scheduler(seconds=3, immediate=False)
def sync_schedule_test():
    print("test")


@router.get('/action-with-schedule')
async def schedule_test() -> CustomizeApiResponse:
    """test function related to schedule"""
    await async_schedule_test()
    await sync_schedule_test()
    return CustomizeApiResponse()
