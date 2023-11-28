#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Annotated
from pydantic import BaseModel, Field
# local
from app.common import constants
# fields
email_field = Field(title="email", example='user@email.com', pattern=r'^\S+@\S+\.\S+$')
password_field = Field(title="password", min_length=constants.USER_PASSWORD_MIN_LENGTH, max_length=constants.USER_PASSWORD_MAX_LENGTH)


class LoginIn(BaseModel):
    email: Annotated[str, email_field]
    password: Annotated[str, password_field]
