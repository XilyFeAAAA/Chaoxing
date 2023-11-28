#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from sqlalchemy import String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.core.db import Base
from app.core.db.orm.anno_type import intpk, timestamp


class Permission(Base):
    """orm permission table"""

    id: Mapped[intpk]
    code: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    resource: Mapped[str] = mapped_column(String(100), nullable=False)
    method: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(300), default="")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    roles: Mapped[list['Role']] = relationship('Role', secondary='table_rolepermission', back_populates='permissions')
