#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, Body, HTTPException
# local
from app import modules
from app.models import User
from app.schemas.request import UserIn, UserInfoIn
from app.schemas.response import UserOut, UserInfoOut
from app.core.middleware import logMiddleware
from app.core.dependency import login_required, captcha_required
from app.core.response import CustomizeApiResponse, ApiResponse


router = APIRouter(route_class=logMiddleware)


@router.get("/me", response_model=UserOut)
async def get_me(current_user: Annotated[User, Depends(login_required)]) -> ApiResponse:
    """get current user data"""
    return CustomizeApiResponse(data=UserOut.model_validate(current_user))


@router.post('/add', response_model=UserOut)
async def register(user_in: Annotated[UserIn, Body(title="user register model")]) -> ApiResponse:
    """register a new user"""
    new_user = await modules.user.create_user(user_in)
    return CustomizeApiResponse(data=UserOut.model_validate(new_user))


@router.post('/del')
async def delete(current_user: Annotated[User, Depends(login_required)]) -> ApiResponse:
    """delete user"""
    await modules.user.del_user(current_user.user_id)
    return CustomizeApiResponse()


@router.post('/pwd-change')
async def change_password(current_user: Annotated[User, Depends(login_required)], new_pwd: Annotated[str, Body(title='new password', embed=True)]) -> ApiResponse:
    """change the password"""
    await modules.user.pwd_change(current_user.user_id, new_pwd)
    return CustomizeApiResponse(msg="change password successfully")


@router.get('/verify/email/{email}')
async def verify_email(email: str) -> ApiResponse:
    """check whether the email exists"""
    await modules.user.verify_email(email)
    return CustomizeApiResponse(msg="the email is vaild")


@router.get('/profile/{user_id}', response_model=UserInfoOut)
async def get_profile(user_id: str) -> ApiResponse:
    """get user's info"""
    user = await modules.user.get_user_by_userid(user_id)
    if user is None:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="can not find user")
    return CustomizeApiResponse(data=UserInfoOut.model_validate(user.info))


@router.post('/profile', response_model=UserInfoOut)
async def set_profile(current_user: Annotated[User, Depends(login_required)], new_info: Annotated[UserInfoIn, Body(title="profile update model")]) -> ApiResponse:
    """update user's info"""
    info = await modules.user.update_info(user_id=current_user.user_id, new_info=new_info)
    return CustomizeApiResponse(data=UserInfoOut.model_validate(info))
