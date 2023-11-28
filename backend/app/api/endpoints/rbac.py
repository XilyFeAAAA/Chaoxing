#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Annotated
from datetime import datetime
from http import HTTPStatus
from datetime import timedelta
from fastapi import APIRouter, Depends, Body

# local
from app import modules
from app.models import Permission, Role
from app.schemas.request import PaginationIn, RoleIn, RoleUpdateIn
from app.schemas.response import RoleOut, RoleDetailOut, PaginationOut, PermissionOut, ResultOut
from app.core.middleware import logMiddleware
from app.core.dependency import permission_required, paginated_params
from app.core.response import CustomizeApiResponse, ApiResponse

router = APIRouter(route_class=logMiddleware)


@router.get('/roles', response_model=PaginationOut[RoleOut])
async def get_roles(pagination: Annotated[PaginationIn, Depends(paginated_params)]) -> ApiResponse:
    """get data of all roles with pagination"""
    roles, total = await modules.rbac.get_multi(model=Role, cursor=pagination.cursor, limit=pagination.limit)
    res = PaginationOut(size=len(roles), total=total, items=[RoleOut.model_validate(role) for role in roles])
    return CustomizeApiResponse(data=res)


@router.get('/role/{code}', response_model=RoleDetailOut)
async def get_role_info(code: str) -> ApiResponse:
    """get data of certain role with its permissions"""
    role, permissions = await modules.rbac.get_role(code=code)
    role = RoleOut.model_validate(role)
    permissions = [PermissionOut.model_validate(permission) for permission in permissions]
    return CustomizeApiResponse(data=RoleDetailOut(role=role, permissions=permissions))


@router.post('/role/add')
async def add_role(new_role: Annotated[RoleIn, Body()]) -> ApiResponse:
    """create new role"""
    role = await modules.rbac.create_role(new_role)
    return CustomizeApiResponse(data=RoleOut.model_validate(role))


@router.post('/role/update')
async def update_role(update: Annotated[RoleUpdateIn, Body()]) -> ApiResponse:
    """update role"""
    role = await modules.rbac.update_role(update)
    return CustomizeApiResponse(data=RoleOut.model_validate(role))


@router.post('/role/delete', response_model=ResultOut)
async def del_roles(codes: Annotated[list[str], Body(embed=True, description="code list of roles")]) -> ApiResponse:
    """delete roles in batches"""
    count = await modules.rbac.del_roles(codes)
    return CustomizeApiResponse(data=ResultOut(rows=count))


@router.get('/permissions', response_model=PaginationOut[PermissionOut])
async def get_roles(pagination: Annotated[PaginationIn, Depends(paginated_params)]) -> ApiResponse:
    """get data of all permissions with pagination"""
    permissions, total = await modules.rbac.get_multi(model=Permission, cursor=pagination.cursor, limit=pagination.limit)
    res = PaginationOut(size=len(permissions), total=total, items=[PermissionOut.model_validate(permission) for permission in permissions])
    return CustomizeApiResponse(data=res)


@router.post('/permission/disable', response_model=ResultOut)
async def disable_permissions(codes: Annotated[list[str], Body(description="code list of permissions")], disabled: Annotated[bool, Body()]) -> ApiResponse:
    """change the status disablity in batches"""
    count = await modules.rbac.disable_permissions(codes, disabled)
    return CustomizeApiResponse(data=ResultOut(rows=count))
