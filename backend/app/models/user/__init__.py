#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from datetime import datetime
from sqlalchemy import String, BigInteger, Boolean, ForeignKey, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
# local
from app.core.db import Base
from app.common import constants
from app.common.enums import SexEnum
from app.core.db.orm.anno_type import intpk, timestamp


class User(Base):
    """orm user table"""

    id: Mapped[intpk]
    user_id: Mapped[str] = mapped_column(String(constants.USER_ID_LENGTH), primary_key=True, index=True)
    role_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("table_role.id"), nullable=True)
    email: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    created_time: Mapped[timestamp]
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    info: Mapped['UserInfo'] = relationship("UserInfo", uselist=False, lazy="joined")
    role: Mapped['Role'] = relationship('Role', back_populates='users', lazy="joined")
    account: Mapped['Account'] = relationship("Account", uselist=False)

class UserInfo(Base):
    """orm user info table"""

    id: Mapped[intpk]
    user_id: Mapped[str] = mapped_column(String(constants.USER_ID_LENGTH), ForeignKey("table_user.user_id"), nullable=False)
    nickname: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    sex: Mapped[SexEnum] = mapped_column(Enum(SexEnum), nullable=False, default=SexEnum.unknown)
    money: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
