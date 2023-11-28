#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.core.db.orm.anno_type import intpk


class RolePermission(Base):
    """orm rolepermission relationship table"""

    id: Mapped[intpk]
    role_code: Mapped[str] = mapped_column(String(100), ForeignKey("table_role.code"), nullable=True)
    permission_code: Mapped[str] = mapped_column(String(100), ForeignKey("table_permission.code"), nullable=True)
