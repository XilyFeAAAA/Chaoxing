#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from pydantic import BaseModel
# local
from .account import AccountOut
from app.schemas.response.user import UserInfoOut


class CourseOrderOut(BaseModel):
    order_id: str
    user_id: str
    account_id: str
    account_phone: str
    platform: str
    course_name: str
    progress: float
    order_time: int
    cost: float
    state: int

    class Config:
        from_attributes = True


class ChaoxingOrderOut(BaseModel):
    course_order: CourseOrderOut
    user: 'UserInfoOut'
    account: 'AccountOut'


class PreOrderOut(BaseModel):
    email: str
    platform: str
    phone: str
    course_name: str
    course_id: str
    cost: float
    is_open: bool

    class Config:
        from_attributes = True
