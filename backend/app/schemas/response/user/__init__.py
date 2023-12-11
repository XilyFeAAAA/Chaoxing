#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserInfoOut(BaseModel):
    nickname: Optional[str] = None
    money: Optional[float] = None

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    userinfo: Optional[UserInfoOut] = None
    created_time: Optional[int] = None

    class Config:
        from_attributes = True

