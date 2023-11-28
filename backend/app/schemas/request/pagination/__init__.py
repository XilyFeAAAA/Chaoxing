#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Annotated
from pydantic import BaseModel, Field


limit_field = Field(title="limit", gt=0, description="length of queried items")
cursor_field = Field(title="cursor", ge=0, description="current page")


class PaginationIn(BaseModel):
    limit: Annotated[int, limit_field]
    cursor: Annotated[int, cursor_field]
