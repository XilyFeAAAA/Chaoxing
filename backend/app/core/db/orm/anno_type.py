#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from datetime import datetime
from typing_extensions import Annotated

from sqlalchemy import BigInteger, func
from sqlalchemy.orm import mapped_column

# primary key
intpk = Annotated[int, mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)]
# timestamp key
timestamp = Annotated[datetime, mapped_column(insert_default=func.utc_timestamp(), default=None)]
