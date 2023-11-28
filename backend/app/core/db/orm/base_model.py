#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.ext.declarative import declared_attr


class Base(DeclarativeBase):
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return f"table_{cls.__name__.lower()}"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
