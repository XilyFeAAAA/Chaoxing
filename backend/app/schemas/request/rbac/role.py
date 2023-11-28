#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Annotated
from pydantic import BaseModel, Field

code_field = Field(title="code", description="code of role")
name_field = Field(title="name", description="name of role")
permissions_field = Field(title="permissions", description="list of permissions")
description_field = Field(title="description", description="description of role")


class RoleIn(BaseModel):
    name: Annotated[str, name_field]
    description: Annotated[str, description_field]
    permissions: Annotated[list[str], permissions_field]


class RoleUpdateIn(BaseModel):
    code: Annotated[str, code_field]
    name: Annotated[str | None, name_field] = None
    description: Annotated[str | None, description_field] = None
    permissions: Annotated[list[str] | None, permissions_field] = None
