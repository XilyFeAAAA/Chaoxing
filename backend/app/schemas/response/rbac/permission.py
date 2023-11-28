#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from pydantic import BaseModel


class PermissionOut(BaseModel):
    name: str
    code: str
    resource: str
    method: str
    description: str

    class Config:
        from_attributes = True
