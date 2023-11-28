#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Generic, TypeVar
from pydantic import Field, BaseModel

T = TypeVar('T')


class PaginationOut(BaseModel, Generic[T]):
    size: int = Field(description='Number of items returned in the response')
    total: int = Field(description='Number of total items in database')
    items: list[T] = Field(description='List of items returned in the response following given criteria')
