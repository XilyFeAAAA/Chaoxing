#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from pathlib import Path
BASE_FOLDER: Path = Path('app')
# docs
PROJECT_NAME: str = "ChaoXing"
VERSION: str = "1.0.0"
# schema
USER_NICKNAME_MIN_LENGTH: int = 3
USER_NICKNAME_MAX_LENGTH: int = 10
USER_PASSWORD_MIN_LENGTH: int = 6
USER_PASSWORD_MAX_LENGTH: int = 20
# captcha
IGNORE_CASE: bool = True
CAPTCHA_LENGTH: int = 4
CAPTCHA_MIN_TIMEDELTA: int = 5
# auth
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 12
REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
# model
USER_ID_LENGTH: int = 12
# upload
SMALL_CHUNK_SIZE: int = 1024
TEMPFILE_FOLDER_PATH: Path = BASE_FOLDER / 'temps'
TEMPFILE_ID_LENGTH: int = 8
# api
API_LOGIN: str = "https://passport2.chaoxing.com/fanyalogin"
API_CHECK: str = "https://i.chaoxing.com/base/settings?t="
API_CHECK_REFER: str = "https://i.chaoxing.com/base?t="