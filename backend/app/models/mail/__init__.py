#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from sqlalchemy import String, BigInteger, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column


from app.core.db import Base
from app.common import constants
from app.core.db.orm.anno_type import intpk


class Notification(Base):
    """orm notification table"""

    id: Mapped[intpk]
    notification_id: Mapped[str] = mapped_column(String(constants.MESSAGE_ID_LENGTH), index=True, nullable=False)
    user_id: Mapped[str] = mapped_column(String(constants.USER_ID_LENGTH), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_time: Mapped[int] = mapped_column(BigInteger, nullable=False)
