#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from datetime import datetime
from sqlalchemy import String, BigInteger, Boolean, ForeignKey, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
# local
from app.core.db import Base
from app.common import constants
from app.core.db.orm.anno_type import intpk, timestamp


class Course(Base):
    """orm course table"""

    id: Mapped[intpk]
    user_id: Mapped[str] = mapped_column(String(constants.USER_ID_LENGTH), ForeignKey("table_user.user_id"), nullable=False)
    account_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("table_account.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    course_id: Mapped[str] = mapped_column(String(100), nullable=False)
    class_id: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(100), nullable=False)
    cpi: Mapped[str] = mapped_column(String(100), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    account: Mapped['Account'] = relationship('Account', back_populates='courses')
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
