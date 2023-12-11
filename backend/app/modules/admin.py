#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from sqlalchemy.orm import selectinload
# local
from app.models import CourseOrder, User, Permission, Role, Log
from app.core.db import async_session
from app.schemas.request import PaginationIn
from app.utils.sql_helper import patch_query, patch_count


async def get_chaoxing_order(pagination: PaginationIn) -> tuple[int, list[CourseOrder]]:
    stmt_query = patch_query(CourseOrder, pagination).options(selectinload(CourseOrder.user)).options(selectinload(CourseOrder.account))
    stmt_count = patch_count(CourseOrder, pagination)
    async with async_session.begin() as session:
        orm_orders = (await session.execute(stmt_query)).scalars().all()
        total = (await session.execute(stmt_count)).scalar()
        session.expunge_all()
    return total, orm_orders


async def get_user_list(pagination: PaginationIn) -> tuple[int, list[User]]:
    stmt_query = patch_query(User, pagination)
    stmt_count = patch_count(User, pagination)
    async with async_session.begin() as session:
        orm_users = (await session.execute(stmt_query)).scalars().all()
        total = (await session.execute(stmt_count)).scalar()
        session.expunge_all()
    return total, orm_users


async def get_permission_list(pagination: PaginationIn) -> tuple[int, list[Permission]]:
    stmt_query = patch_query(Permission, pagination)
    stmt_count = patch_count(Permission, pagination)
    async with async_session.begin() as session:
        orm_permissions = (await session.execute(stmt_query)).scalars().all()
        total = (await session.execute(stmt_count)).scalar()
        session.expunge_all()
    return total, orm_permissions


async def get_role_list(pagination: PaginationIn) -> tuple[int, list[Role]]:
    stmt_query = patch_query(Role, pagination)
    stmt_count = patch_count(Role, pagination)
    async with async_session.begin() as session:
        orm_roles = (await session.execute(stmt_query)).scalars().all()
        total = (await session.execute(stmt_count)).scalar()
        session.expunge_all()
    return total, orm_roles


async def get_log_list(pagination: PaginationIn) -> tuple[int, list[Log]]:
    stmt_query = patch_query(Log, pagination)
    stmt_count = patch_count(Log, pagination)
    async with async_session.begin() as session:
        orm_logs = (await session.execute(stmt_query)).scalars().all()
        total = (await session.execute(stmt_count)).scalar()
        session.expunge_all()
    return total, orm_logs