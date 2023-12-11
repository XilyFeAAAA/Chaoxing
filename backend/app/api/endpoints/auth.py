#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Annotated
from datetime import datetime
from http import HTTPStatus
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Request, Response, Depends, Body

# local
from app import modules
from app.models import User
from app.common import constants
from app.schemas.request import LoginIn
from app.schemas.response import UserOut
from app.core.security import create_token
from app.core.dependency import login_required
from app.core.middleware import logMiddleware
from app.utils.captcha_helper import generate_captcha, create_code
from app.core.response import CustomizeApiResponse, ApiResponse
router = APIRouter(route_class=logMiddleware)


@router.post("/access-token", response_model=UserOut)
async def login_access_token(form_data: Annotated[LoginIn, Body()]):
    """OAuth2: get an access token for further requests
    In the production environment, use `return CustomizeApiResponse` instead of another one
    """
    user = await modules.auth.authenticate(account=form_data.email, password=form_data.password)
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    access_token = await create_token(user.user_id)
    response = CustomizeApiResponse(data=UserOut.model_validate(user))
    response.set_cookie(
        key="access-token",
        value=access_token,
        max_age=constants.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="none",
        secure=True
    )
    return response


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
