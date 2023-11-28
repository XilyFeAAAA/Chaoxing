#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from fastapi import Query
from typing import Annotated
# local
from app.schemas.request import PaginationIn


async def paginated_params(
        limit: Annotated[int, Query()],
        cursor: Annotated[int, Query()]) -> PaginationIn:
    """dependency to get parameters for pagination"""
    return PaginationIn(limit=limit, cursor=cursor)
