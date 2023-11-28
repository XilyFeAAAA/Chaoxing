#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from pydantic import BaseModel


class ResultOut(BaseModel):
    rows: int
