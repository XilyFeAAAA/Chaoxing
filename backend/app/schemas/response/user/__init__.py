#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Optional
from pydantic import BaseModel


class UserInfoOut(BaseModel):
    nickname: Optional[str] = None
    sex: Optional[int] = None
    created_time: Optional[int] = None

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    info: Optional[UserInfoOut] = None

    class Config:
        from_attributes = True
