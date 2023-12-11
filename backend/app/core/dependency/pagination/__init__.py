#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from fastapi import Query, Body
from typing import Annotated
# local
from app.schemas.request import PaginationIn


async def paginated_params(
        limit: Annotated[int | None, Query()],
        cursor: Annotated[int | None, Query()],
        keyword: Annotated[dict | None, Body()] = {}) -> PaginationIn:
    """dependency to get parameters for pagination"""
    return PaginationIn(limit=limit, cursor=cursor, keyword=keyword)
