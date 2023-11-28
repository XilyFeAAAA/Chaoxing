#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from sqlalchemy import String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.core.db import Base
from app.core.db.orm.anno_type import intpk, timestamp


class Role(Base):
    """orm role table"""

    id: Mapped[intpk]
    code: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(100), index=True, default="")
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    users: Mapped[list['User']] = relationship('User', back_populates='role')
    permissions: Mapped[list['Permission']] = relationship('Permission', secondary='table_rolepermission', back_populates='roles')
