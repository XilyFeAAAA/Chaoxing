#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import time
from http import HTTPStatus
from typing import Annotated
from starlette.requests import Request
from datetime import datetime, timezone
from fastapi import Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer
# local
from app.models import User
from app.common import constants
from app.common.enums import MsgEnum
from app.core.config import settings
from app.core.security import check_token
from app.modules.user import get_user_by_userid
from app.modules.rbac import get_roles_with_permission
from app.utils.string_helper import url_to_resource


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}{settings.OAUTH2_PATH}"
)


async def login_required(token: Annotated[str, Depends(reusable_oauth2)]) -> User:
    """dependency to check login state"""
    payload = check_token(token)
    user = await get_user_by_userid(payload["sub"])
    return user


async def permission_required(request: Request, user: Annotated[User, Depends(login_required)]) -> User:
    """dependency to check role permission"""
    auth = url_to_resource(request.url.path)
    method = request.method.upper()
    required_roles = await get_roles_with_permission(auth, method)
    if user.role.name in [role.name for role in required_roles]:
        return user
    else:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)


async def captcha_required(request: Request, captcha: Annotated[str, Body(description="captcha", embed=True)]):
    """dependency to check captcha """
    stored_captcha = request.session.get("captcha", None)
    captcha_expire = request.session.get("captcha_expire", None)
    if constants.IGNORE_CASE:
        captcha = captcha.lower()
        stored_captcha = stored_captcha.lower()
    if stored_captcha is None or captcha != stored_captcha:
        raise HTTPException(status_code=401, detail="invalid captcha")
    elif captcha_expire is None or time.time() > captcha_expire:
        raise HTTPException(status_code=401, detail="expired captcha")
    else:
        request.session.pop("captcha")
        request.session.pop("captcha_expire")
