#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from app.core.security import verify_password
from app.models import User
from app.modules.user import get_user_by_email


async def authenticate(account: str, password: str, admin: bool = False) -> User | None:
    """judge if account exists and password compares"""
    cnt_user = await get_user_by_email(account)
    if cnt_user and verify_password(password, cnt_user.hashed_password):
        if admin and cnt_user.role.name != 'admin':
            return None
        return cnt_user
    else:
        return None
