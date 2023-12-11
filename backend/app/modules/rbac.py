#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import time
from http import HTTPStatus
from typing import Union
from fastapi import HTTPException
from sqlalchemy import select, false, true, and_, func
from sqlalchemy.orm import selectinload

# local
from app.core.db import async_session
from app.models import Role, Permission, RolePermission
from app.schemas.request import RoleIn, RoleUpdateIn


async def get_roles_with_permission(resource: str, method: str) -> list[Role]:
    """query roles with specific permission"""
    async with async_session.begin() as session:
        stmt = select(Role).join(Role.permissions) \
            .filter(Permission.resource == resource) \
            .filter(Permission.method == method) \
            .filter(Permission.disabled == false())
        roles = (await session.execute(stmt)).scalars().all()
        session.expunge_all()
    return roles


async def get_role(code: str) -> tuple[Role, Permission]:
    """query role and ites permissions"""
    async with async_session.begin() as session:
        stmt = select(Role)\
            .filter(and_(Role.code == code, Role.deleted == false()))\
            .options(selectinload(Role.permissions))
        role = (await session.execute(stmt)).scalar_one_or_none()
        if role is None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="invaild_role_code")
        permissions = role.permissions
        session.expunge_all()
    return role, permissions


async def del_roles(codes: list[str]) -> int:
    """delete roles in banches"""
    async with async_session.begin() as session:
        stmt = select(Role).filter(and_(Role.code.in_(codes), Role.deleted == false()))
        roles = (await session.execute(stmt)).scalars().all()
        for role in roles:
            role.deleted = true()
    return len(roles)


async def create_role(new_role: RoleIn) -> Role:
    """create a new role"""
    async with async_session.begin() as session:
        count = (await session.execute(select(func.count()).select_from(Role))).scalar()
        code = f"r{count+1}00"
        orm_role = Role(name=new_role.name, code=code, description=new_role.description)
        session.add(orm_role)
        await session.flush()
        role_permissions = []
        for permission_code in new_role.permissions:
            stmt = select(Permission).filter(and_(Permission.code == permission_code, Permission.deleted == false()))
            orm_permission = (await session.execute(stmt)).scalar_one_or_none()
            if orm_permission is None:
                raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="invaild_role_code")
            role_permission = RolePermission(role_code=orm_role.code, permission_code=permission_code)
            role_permissions.append(role_permission)
        session.add_all(role_permissions)
        session.expunge(orm_role)
    return orm_role


async def disable_permissions(codes: list[str], disabled: bool) -> int:
    """update status of disablity"""
    async with async_session.begin() as session:
        stmt = select(Permission).filter(and_(Permission.code.in_(codes), Permission.deleted == false()))
        permissions = (await session.execute(stmt)).scalars().all()
        for permission in permissions:
            permission.disabled = true() if disabled else false()
    return len(permissions)


async def update_role(update: RoleUpdateIn) -> Role:
    """update role"""
    async with async_session.begin() as session:
        stmt = select(Role).filter(and_(Role.code == update.code, Role.deleted == false()))
        orm_role = (await session.execute(stmt)).scalar_one_or_none()
        if orm_role is None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="invaild_role_code")
        # update common attributes
        for key, value in update.model_dump(exclude=["permissions"]).items():
            if value is not None:
                orm_role.__setattr__(key, value)
        # update permissions
        if update.permissions is not None:
            # delete old role_permission
            stmt = select(RolePermission).filter(RolePermission.role_code == orm_role.code)
            orm_role_permissions = (await session.execute(stmt)).scalars().all()
            for orm_role_permission in orm_role_permissions:
                session.delete(orm_role_permission)
            # add new role_permission
            role_permissions = []
            for permission_code in update.permissions:
                role_permissions.append(RolePermission(role_code=orm_role.code, permission_code=permission_code))
            session.add_all(role_permissions)
        await session.flush()
        session.expunge(orm_role)
    return orm_role

