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


class PlatformEnum(str, BaseEnum):
    chaoxing = "超星学习通"


class OrderStatusEnum(int, BaseEnum):
    # 0: 提交中 1: 正在进行 2: 结束 3: 失败 4: 取消 5: 补单中
    CONFIRMING = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    FAILED = 3
    CANCELLED = 4
    REMEDY = 5
