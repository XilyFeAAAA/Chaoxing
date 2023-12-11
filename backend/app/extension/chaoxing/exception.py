#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from http import HTTPStatus
from typing import Optional


class ChaoxingException(Exception):
    def __init__(self, detail: str, order_id: Optional[str] = None) -> None:
        self.detail = detail
        self.order_id = order_id


__all__ = ['ChaoxingException']
