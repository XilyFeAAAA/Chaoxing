#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from typing import Annotated
from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends, Body, BackgroundTasks, Request, Response, Path

# local
from app import modules
from app.models import User
from app.schemas.request import AccountIn, PaginationIn, AccountRefreshIn
from app.schemas.response import AccountOut, CourseOut, CourseOrderOut, PaginationOut, UserInfoOut, PreOrderOut
from app.core.dependency import login_required, captcha_required, paginated_params
from app.core.middleware import logMiddleware
from app.core.response import CustomizeApiResponse, ApiResponse
from app.extension.chaoxing import Chaoxing_Qrcode, pwd_login, check_cookie, get_account_info, qrcode_login, get_qrcode_img, get_qrcode, Chaoxing_Config

router = APIRouter(route_class=logMiddleware)


@router.post('/pwd-bind', response_model=AccountOut, dependencies=[Depends(captcha_required)])
async def pwd_bind_account(account_info: Annotated[AccountIn, Body()], user: Annotated[User, Depends(login_required)], background_tasks: BackgroundTasks) -> ApiResponse:
    """bind user with chaoxing account"""
    cookie = await pwd_login(account_info)
    if not await check_cookie(cookie):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="无效的Cookie")
    chaoxing_user = await get_account_info(cookie)
    orm_account = await modules.chaoxing.add_account(user, chaoxing_user)
    # get account's courses in the background
    background_tasks.add_task(modules.chaoxing.save_courses, orm_account.account_id, user.user_id, chaoxing_user)
    return CustomizeApiResponse(data=AccountOut.model_validate(orm_account))


@router.post('/qrcode-bind', response_model=AccountOut)
async def qrcode_bind_account(request: Request, user: Annotated[User, Depends(login_required)], background_tasks: BackgroundTasks) -> ApiResponse:
    if not (uuid := request.session.get('qrcode_uuid')) or not (enc := request.session.get('qrcode_enc')):
        raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail="无效的二维码")
    qr_status, cookie = await qrcode_login(Chaoxing_Qrcode(uuid=uuid, enc=enc))
    if not qr_status["status"]:
        raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail=qr_status.get("type"))
    chaoxing_user = await get_account_info(cookie)
    orm_account = await modules.chaoxing.add_account(user, chaoxing_user)
    # get account's courses in the background
    background_tasks.add_task(modules.chaoxing.save_courses, orm_account.account_id, user.user_id, chaoxing_user)
    return CustomizeApiResponse(data=AccountOut.model_validate(orm_account))


@router.get('/qrcode', dependencies=[Depends(login_required)])
async def qrcode_img(request: Request) -> Response:
    """获取qrcode,将信息存在session里,前端就不用管理uuid和enc"""
    qrcode = await get_qrcode()
    request.session['qrcode_uuid'] = qrcode.uuid
    request.session['qrcode_enc'] = qrcode.enc
    img = get_qrcode_img(qrcode)
    return Response(content=img, media_type="image/png")


@router.post('/accounts/refresh', response_model=AccountOut)
async def account_refresh(refresh_info: Annotated[AccountRefreshIn, Body()], user: Annotated[User, Depends(login_required)]) -> ApiResponse:
    """refresh account's cookie"""
    cookie = await modules.chaoxing.refresh(user, refresh_info)
    if not await check_cookie(cookie):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="无效的Cookie")
    chaoxing_user = await get_account_info(cookie)
    orm_account = await modules.chaoxing.update_account(chaoxing_user)
    return CustomizeApiResponse(data=AccountOut.model_validate(orm_account))


@router.post('/courses/refresh', response_model=list[CourseOut])
async def course_refresh(user: Annotated[User, Depends(login_required)]) -> ApiResponse:
    """refresh active account's courses"""
    await modules.chaoxing.course_refresh(user)
    return CustomizeApiResponse()


@router.get('/accounts', response_model=list[AccountOut])
async def get_accounts(user: Annotated[User, Depends(login_required)]) -> ApiResponse:
    """get user's accounts"""
    return CustomizeApiResponse(data=[AccountOut.model_validate(account) for account in user.accounts])


@router.post('/account/del')
async def del_account(account_id: Annotated[str, Body(embed=True)], user: Annotated[User, Depends(login_required)]) -> ApiResponse:
    """del user's account"""
    await modules.chaoxing.del_account(user, account_id)
    return CustomizeApiResponse()


@router.post('/account/active')
async def active_account(account_id: Annotated[str, Body(embed=True)], user: Annotated[User, Depends(login_required)]) -> ApiResponse:
    """set account active"""
    await modules.chaoxing.set_active(user, account_id)
    return CustomizeApiResponse()


@router.get('/courses', response_model=list[CourseOut])
async def get_courses(user: Annotated[User, Depends(login_required)]):
    """get courses of user's active account"""
    courses = await modules.chaoxing.get_course(user)
    return CustomizeApiResponse(data=[CourseOut.model_validate(course) for course in courses])


@router.post('/order/pre')
async def pre_submit_order(course_id: Annotated[str, Body(embed=True)], user: Annotated[User, Depends(login_required)]) -> ApiResponse:
    """pre confrim"""
    pre_order = await modules.chaoxing.pre_order(course_id, user)
    return CustomizeApiResponse(data=pre_order)


@router.get('/order/{order_id}', response_model=PreOrderOut)
async def get_pre_order(order_id: Annotated[str, Path()], user: Annotated[User, Depends(login_required)]) -> ApiResponse:
    pre_order = await modules.chaoxing.get_pre_order(order_id, user.user_id)
    return CustomizeApiResponse(data=pre_order)


@router.post('/order/cancel/{order_id}')
async def cancel_order(order_id: Annotated[str, Path()], user: Annotated[User, Depends(login_required)]) -> ApiResponse:
    await modules.chaoxing.cancel_order(order_id, user.user_id)
    return CustomizeApiResponse()


@router.post('/order/submit', response_model=UserInfoOut)
async def submit_course_order(order_id: Annotated[str, Body(embed=True)], user: Annotated[User, Depends(login_required)], backgrounds: BackgroundTasks) -> ApiResponse:
    """submit order"""
    orm_userinfo = await modules.chaoxing.submit_order(order_id, user, backgrounds)
    return CustomizeApiResponse(data=UserInfoOut.model_validate(orm_userinfo))


@router.get('/order',  response_model=PaginationOut[list[CourseOrderOut]])
async def get_course_order(user: Annotated[User, Depends(login_required)], pagination: Annotated[PaginationIn, Depends(paginated_params)]) -> ApiResponse:
    """get orders"""
    total, orm_orders = await modules.chaoxing.get_orders(pagination, user)
    res = PaginationOut(size=len(orm_orders), total=total, items=[CourseOrderOut.model_validate(order) for order in orm_orders])
    return CustomizeApiResponse(data=res)