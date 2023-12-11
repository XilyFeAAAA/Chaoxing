#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from pydantic import BaseModel
from datetime import datetime


class AccountOut(BaseModel):
    account_id: str
    username: str
    phone: str
    uid: str
    department: str
    bind_time: int
    active: bool
    valid: bool

    class Config:
        from_attributes = True


class ChaoxingSettingOut(BaseModel):
    work: dict
    exam: dict
    task: dict
    sign: dict
    searcher: dict

    class Config:
        from_attributes = True
