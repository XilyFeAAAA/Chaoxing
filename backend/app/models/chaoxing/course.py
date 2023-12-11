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
    course_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    account_id: Mapped[str] = mapped_column(String(constants.ACCOUNT_ID_LENGTH), ForeignKey("table_account.account_id"))
    user_id: Mapped[str] = mapped_column(String(constants.USER_ID_LENGTH), nullable=False)
    course_name: Mapped[str] = mapped_column(String(100), nullable=False)
    class_id: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(200), nullable=False)
    img_url: Mapped[str] = mapped_column(String(100), nullable=False)
    classroom: Mapped[str] = mapped_column(String(100), nullable=False)
    start_time: Mapped[str] = mapped_column(String(100), nullable=False)
    is_open: Mapped[bool] = mapped_column(Boolean, nullable=False)
    course_teacher: Mapped[str] = mapped_column(String(100), nullable=False)
    account: Mapped['Account'] = relationship('Account', back_populates='courses')
