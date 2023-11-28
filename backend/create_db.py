#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import asyncio
# local
from app.api import api_router
from app.models import User, Role, Permission, RolePermission
from app.core.db.base.engine import async_engine, async_session


async def insert_objects() -> None:
    async with async_session.begin() as session:
        session.add_all([
            Role(name="admin", code="r100", description="管理员"),
            User(role_id=1, user_id="123456789123", email="2782458700@qq.com", hashed_password="$2b$12$aUh2pemEOHhnvswho3gdn.jcBU6W6.xYTDfG45k9PHpAmtrztmThK"),
        ])


async def insert_permission() -> None:
    permissions = []
    for index, route in enumerate(api_router.routes):
        parts = route.path.split("/", 2)
        permissions.append(Permission(code=f"p{index+1}00", name=route.name, resource=f"{parts[1]}:{parts[2]}", method=list(route.methods)[0], description=route.description))
    async with async_session.begin() as session:
        session.add_all(permissions)


async def init_models():
    async with async_engine.begin() as session:
        await session.run_sync(User.metadata.drop_all)
        await session.run_sync(User.metadata.create_all)
    await insert_objects()
    await insert_permission()

asyncio.run(init_models())
