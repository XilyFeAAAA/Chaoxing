#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from pydantic import BaseModel
# local
from .permission import PermissionOut


class RoleOut(BaseModel):
    name: str
    code: str
    description: str

    class Config:
        from_attributes = True


class RoleDetailOut(BaseModel):
    role: RoleOut
    permissions: list[PermissionOut]
