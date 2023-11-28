#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Annotated
from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Request, Response, Depends, Body

# local
from app import modules
from app.models import User
from app.schemas.request import AccountIn
from app.schemas.response import AccountOut
from app.core.dependency import login_required
from app.core.middleware import logMiddleware
from app.core.response import CustomizeApiResponse, ApiResponse
from app.core.extension.chaoxing.util import get_cookie, check_cookie
router = APIRouter(route_class=logMiddleware)


@router.post('/bind', response_model=AccountOut)
async def bind_account(account_info: Annotated[AccountIn, Body()], user: Annotated[User, Depends(login_required)]) -> ApiResponse:
    """bind user with chaoxing account"""
    chaoxing_user = await get_cookie(account_info)
    if not await check_cookie(chaoxing_user.cookie):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="invalid_cookie")
    orm_account = await modules.chaoxing.add_account(user, chaoxing_user)
    return CustomizeApiResponse(data=AccountOut.model_validate(orm_account))

