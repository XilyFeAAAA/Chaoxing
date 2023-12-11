#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from sqlalchemy import String, Boolean, ForeignKey, Text, BigInteger, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
# local
from app.core.db import Base
from app.common import constants
from app.core.db.orm.anno_type import intpk


class Log(Base):
    """orm logger table"""

    id: Mapped[intpk]
    order_id: Mapped[str] = mapped_column(String(constants.ORDER_ID_LENGTH), ForeignKey("table_courseorder.order_id"))
    info: Mapped[str] = mapped_column(Text, nullable=False)
    log_time: Mapped[int] = mapped_column(BigInteger, nullable=False)
