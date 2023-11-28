#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Optional
from pydantic import BaseModel


class RefreshTokenOut(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None


class AccessTokenOut(RefreshTokenOut):
    refresh_token: Optional[str] = None