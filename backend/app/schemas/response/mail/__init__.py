#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from pydantic import BaseModel


class NotificationOut(BaseModel):
    notification_id: str
    title: str
    message: str
    read: bool
    created_time: int

    class Config:
        from_attributes = True


class NotificationInfoOut(BaseModel):
    not_read: int
    notifications: list[NotificationOut]

    class Config:
        from_attributes = True
