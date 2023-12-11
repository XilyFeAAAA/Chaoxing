#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Body, HTTPException

# local
from app import modules
from app.common import constants
from app.core.dependency import permission_required, paginated_params
from app.core.middleware import logMiddleware
from app.core.response import CustomizeApiResponse
from app.core.security import create_token
from app.schemas.request import PaginationIn, LoginIn
from app.schemas.response import *

router = APIRouter(route_class=logMiddleware)


@router.post("/login", response_model=UserOut)
async def login_access_token(form_data: Annotated[LoginIn, Body()]):
    """OAuth2: get an access token for further requests
    In the production environment, use `return CustomizeApiResponse` instead of another one
    """
    if (user := await modules.auth.authenticate(account=form_data.email, password=form_data.password, admin=True)) is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    access_token = await create_token(user.user_id)
    response = CustomizeApiResponse(data=UserOut.model_validate(user))
    response.set_cookie(
        key="access-token",
        value=access_token,
        max_age=constants.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="none",
        secure=True
    )
    return response


@router.post('/order/course', response_model=PaginationOut[list[ChaoxingOrderOut]], dependencies=[Depends(permission_required)])
async def get_order_course(pagination: Annotated[PaginationIn, Depends(paginated_params)]) -> CustomizeApiResponse:
    """return orders of course"""
    total, orm_orders = await modules.admin.get_chaoxing_order(pagination)
    res = PaginationOut(size=len(orm_orders), total=total, items=[ChaoxingOrderOut(
        course_order=CourseOrderOut.model_validate(order),
        user=UserInfoOut.model_validate(order.user.userinfo),
        account=AccountOut.model_validate(order.account)
    ) for order in orm_orders])
    return CustomizeApiResponse(data=res)


@router.post('/user/member', response_model=PaginationOut[list[UserOut]], dependencies=[Depends(permission_required)])
async def get_user_list(pagination: Annotated[PaginationIn, Depends(paginated_params)]) -> CustomizeApiResponse:
    """return list of user info"""
    total, orm_users = await modules.admin.get_user_list(pagination)
    return CustomizeApiResponse(data=PaginationOut(
        size=len(orm_users),
        total=total,
        items=[UserOut.model_validate(user) for user in orm_users]
    ))


@router.post('/permissions', response_model=PaginationOut[PermissionOut], dependencies=[Depends(permission_required)])
async def get_permission_list(pagination: Annotated[PaginationIn, Depends(paginated_params)]) -> CustomizeApiResponse:
    """return list of permissions"""
    total, orm_permissions = await modules.admin.get_permission_list(pagination)
    return CustomizeApiResponse(data=PaginationOut(
        size=len(orm_permissions),
        total=total,
        items=[PermissionOut.model_validate(permission) for permission in orm_permissions]
    ))


@router.get('/roles', response_model=PaginationOut[RoleOut], dependencies=[Depends(permission_required)])
async def get_roles(pagination: Annotated[PaginationIn, Depends(paginated_params)]) -> CustomizeApiResponse:
    """return list of roles"""
    total, orm_roles = await modules.admin.get_role_list(pagination)
    return CustomizeApiResponse(data=PaginationOut(
        size=len(orm_roles),
        total=total,
        items=[RoleOut.model_validate(role) for role in orm_roles]
    ))


@router.post('/logs', response_model=PaginationOut[LogOut], dependencies=[Depends(permission_required)])
async def get_logs(pagination: Annotated[PaginationIn, Depends(paginated_params)]) -> CustomizeApiResponse:
    """return list of roles"""
    total, orm_logs = await modules.admin.get_log_list(pagination)
    return CustomizeApiResponse(data=PaginationOut(
        size=len(orm_logs),
        total=total,
        items=[LogOut.model_validate(log) for log in orm_logs]
    ))
