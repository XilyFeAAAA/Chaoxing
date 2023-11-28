#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from app.core.db import async_session
from app.models import User, Account
from app.core.extension.chaoxing.util import Chaoxing_User


async def add_account(user: User, account_info: Chaoxing_User) -> Account:
    new_account = Account(user_id=user.user_id,
                          username=account_info.username,
                          phone=account_info.phone,
                          uid=account_info.uid,
                          cookie=account_info.cookie)
    async with async_session.begin() as session:
        session.add(new_account)
        await session.flush()
        session.expunge(new_account)
    return new_account
