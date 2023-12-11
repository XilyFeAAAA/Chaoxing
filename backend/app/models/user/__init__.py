#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import json

from sqlalchemy import String, BigInteger, Boolean, ForeignKey, Enum, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
# local
from app.core.db import Base
from app.common import constants
from app.core.db.orm.anno_type import intpk, timestamp


class User(Base):
    """orm user table"""

    id: Mapped[intpk]
    user_id: Mapped[str] = mapped_column(String(constants.USER_ID_LENGTH), primary_key=True, index=True)
    role_code: Mapped[int] = mapped_column(String(100), ForeignKey("table_role.code"), default="r100")
    email: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    created_time: Mapped[int] = mapped_column(BigInteger, nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    userinfo: Mapped['UserInfo'] = relationship("UserInfo", uselist=False, lazy="joined")
    role: Mapped['Role'] = relationship('Role', back_populates='users', lazy="joined")
    accounts: Mapped[list['Account']] = relationship("Account")


class UserInfo(Base):
    """orm user info table"""

    id: Mapped[intpk]
    user_id: Mapped[str] = mapped_column(String(constants.USER_ID_LENGTH), ForeignKey("table_user.user_id"), nullable=False)
    nickname: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    money: Mapped[float] = mapped_column(Float, nullable=False, default=10)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

