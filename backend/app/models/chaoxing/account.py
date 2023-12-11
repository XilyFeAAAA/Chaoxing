#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from sqlalchemy import String, Boolean, ForeignKey, Text, BigInteger, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
# local
from app.core.db import Base
from app.common import constants
from app.core.db.orm.anno_type import intpk


class Account(Base):
    """orm account table"""

    id: Mapped[intpk]
    account_id: Mapped[str] = mapped_column(String(constants.ACCOUNT_ID_LENGTH), index=True)
    user_id: Mapped[str] = mapped_column(String(constants.USER_ID_LENGTH), ForeignKey("table_user.user_id"))
    username: Mapped[str] = mapped_column(String(100), nullable=True)
    phone: Mapped[str] = mapped_column(String(100), nullable=False)
    uid: Mapped[str] = mapped_column(String(100), nullable=False)
    cookie: Mapped[str] = mapped_column(Text, nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    valid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    bind_time: Mapped[int] = mapped_column(BigInteger, nullable=False)
    courses: Mapped[list['Course']] = relationship("Course", back_populates="account")
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)


class ChaoxingSetting(Base):
    """orm chaoxing setting table"""

    id: Mapped[intpk]
    user_id: Mapped[str] = mapped_column(String(constants.USER_ID_LENGTH), nullable=False)
    work: Mapped[dict] = mapped_column(JSON, nullable=False)
    exam: Mapped[dict] = mapped_column(JSON, nullable=False)
    task: Mapped[dict] = mapped_column(JSON, nullable=False)
    sign: Mapped[dict] = mapped_column(JSON, nullable=False)
    searcher: Mapped[dict] = mapped_column(JSON, nullable=False)

