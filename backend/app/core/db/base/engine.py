#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings

async_engine = create_async_engine(
    f"mysql+aiomysql://"
    f"{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}"
    f"@{settings.MYSQL_HOST}/{settings.MYSQL_DB}"
)

# async version sessionmaker
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
