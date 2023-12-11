#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from sqlalchemy import String, BigInteger, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
# local
from app.common import constants
from app.common.enums import OrderStatusEnum
from app.core.db import Base
from app.core.db.orm.anno_type import intpk


class CourseOrder(Base):
    """orm course_order table"""

    id: Mapped[intpk]
    order_id: Mapped[str] = mapped_column(String(constants.ORDER_ID_LENGTH), index=True)
    course_id: Mapped[str] = mapped_column(String(100), ForeignKey("table_course.course_id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(constants.USER_ID_LENGTH), ForeignKey("table_user.user_id"), nullable=False)
    task_id: Mapped[str] = mapped_column(String(100), nullable=True)
    account_id: Mapped[str] = mapped_column(String(constants.ACCOUNT_ID_LENGTH), ForeignKey("table_account.account_id"),  nullable=False)
    account_phone: Mapped[str] = mapped_column(String(100), nullable=False)
    platform: Mapped[str] = mapped_column(String(100), nullable=False)
    course_name: Mapped[str] = mapped_column(String(100), nullable=False)
    progress: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    order_time: Mapped[int] = mapped_column(BigInteger, nullable=False)
    cost: Mapped[float] = mapped_column(Float, nullable=False)
    state: Mapped[int] = mapped_column(Integer, default=OrderStatusEnum.CONFIRMING.value)  # 0: 确认中 1: 正在进行 2: 结束 3: 失败 4: 取消 6: 补单中

    user: Mapped['User'] = relationship("User", uselist=False, lazy=True)
    course: Mapped['Course'] = relationship("Course", uselist=False, lazy=True)
    account: Mapped['Account'] = relationship("Account", uselist=False, lazy=True)

