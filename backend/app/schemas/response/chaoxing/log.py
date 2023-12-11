#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from pydantic import BaseModel


class LogOut(BaseModel):
    order_id: str
    info: str
    log_time: int

    class Config:
        from_attributes = True