#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Annotated
from pydantic import BaseModel, Field
# local
from app.common import constants
from app.common.enums import SexEnum
# fields
email_field = Field(title="email", example='user@email.com', pattern=r'^\S+@\S+\.\S+$')
nickname_field = Field(title="nickname", min_length=constants.USER_NICKNAME_MIN_LENGTH, max_length=constants.USER_NICKNAME_MAX_LENGTH)
password_field = Field(title="password", min_length=constants.USER_PASSWORD_MIN_LENGTH, max_length=constants.USER_PASSWORD_MAX_LENGTH)
sex_field = Field(title="sex", examples=SexEnum.val_list())


class UserIn(BaseModel):
    email: Annotated[str, email_field]
    nickname: Annotated[str, nickname_field]
    password: Annotated[str, password_field]


class UserInfoIn(BaseModel):
    nickname: Annotated[str | None, nickname_field]
    sex: Annotated[SexEnum | None, sex_field]
