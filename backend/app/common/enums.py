#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def val_list(cls):
        return list(map(lambda c: c.value, cls))


class SexEnum(int, BaseEnum):
    unknown = 0
    man = 1
    woman = 2


class StatusEnum(int, BaseEnum):
    uploading = 0
    uploaded = 1
    error = 2


class MsgEnum(str, BaseEnum):
    expired_session = "EXPIRE_SESSION"
    invalid_token = "INVAILD_TOKEN"
