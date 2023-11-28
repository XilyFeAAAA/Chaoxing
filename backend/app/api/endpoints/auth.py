#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Annotated
from datetime import datetime
from http import HTTPStatus
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Request, Response, Depends

# local
from app import modules
from app.models import User
from app.common import constants
from app.schemas.response import AccessTokenOut, RefreshTokenOut
from app.core.security import create_token
from app.core.dependency import login_required
from app.core.middleware import logMiddleware
from app.utils.captcha_helper import generate_captcha, create_code
from app.core.response import CustomizeApiResponse, ApiResponse
router = APIRouter(route_class=logMiddleware)


@router.post("/access-token")
async def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """OAuth2: get an access token for further requests
    In the production environment, use `return CustomizeApiResponse` instead of another one
    """
    user = await modules.auth.authenticate(account=form_data.username, password=form_data.password)
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    access_token = await create_token(user.user_id, expire_delta=timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = await create_token(user.user_id, expire_delta=timedelta(minutes=constants.REFRESH_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": 'bearer'}
    # return CustomizeApiResponse(data=AccessTokenOut(access_token=access_token, refresh_token=refresh_token, token_type="bearer"))


@router.post("/refresh-token", response_model=RefreshTokenOut)
async def refresh(current_user: Annotated[User, Depends(login_required)]):
    """generate short-live token
    When access-token(short-live) expired, refresh-token can be used to generate a new access-token
    """
    access_token = await create_token(current_user.user_id, expire_delta=timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES))
    return CustomizeApiResponse(data=RefreshTokenOut(access_token=access_token, token_type="bearer"))


# TODO: 图形验证码接口限流
@router.get('/captcha', response_description="return png format captcha")
async def image_code(request: Request):
    """get captcha image
    The expired time of capthca can be modified in constant.py
    """
    code = create_code()
    print(code)
    expire_time = datetime.now() + timedelta(minutes=constants.CAPTCHA_MIN_TIMEDELTA)
    request.session['captcha'] = code
    request.session['captcha_expire'] = int(expire_time.timestamp())
    img = generate_captcha(code)
    return Response(content=img, media_type="image/png")
