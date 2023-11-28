#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from pydantic import BaseModel


class AccountOut(BaseModel):
    username: str | None
    phone: str
    uid: str

    class Config:
        from_attributes = True
