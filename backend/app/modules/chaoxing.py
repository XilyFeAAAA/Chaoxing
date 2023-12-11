#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import asyncio
from time import time
from http import HTTPStatus

from dacite import from_dict
from sqlalchemy import select, and_, false, true
from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.orm import selectinload

# local
from app import modules
from app.common import constants
from app.common.enums import PlatformEnum, OrderStatusEnum
from app.core.db import async_session
from app.models import User, UserInfo, Account, Course, CourseOrder, ChaoxingSetting
from app.schemas.request import PaginationIn, AccountRefreshIn, AccountIn, ChaoxingSettingIn
from app.schemas.response import PreOrderOut
from app.utils.number_helper import generate_random_num
from app.utils.string_helper import generate_random_string
from app.utils.sql_helper import patch_query, patch_count
from app.extension.chaoxing import Chaoxing_Config, Chaoxing_User, get_courses, pwd_login, Chaoxing_Worker, ChaoxingException


async def get_active(user: User, require: bool) -> Account | None:
    active_account: Account = None
    for account in (user.accounts or []):
        if account.active:
            active_account = account
    if require and active_account is None:
        raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail="账户不存在")
    else:
        return active_account


async def add_account(user: User, chaoxing_user: Chaoxing_User) -> Account:
    new_account = Account(account_id=generate_random_num(constants.ACCOUNT_ID_LENGTH),
                          user_id=user.user_id,
                          username=chaoxing_user.username,
                          phone=chaoxing_user.phone,
                          uid=chaoxing_user.uid,
                          cookie=chaoxing_user.cookie,
                          department=chaoxing_user.department,
                          bind_time=int(round(time() * 1000)))
    async with async_session.begin() as session:
        stmt = select(Account).filter(Account.uid == chaoxing_user.uid)
        orm_account = (await session.execute(stmt)).scalar_one_or_none()
        if orm_account is not None:
            raise HTTPException(HTTPStatus.CONFLICT.value, detail="账户已经绑定过")
        session.add(new_account)
        await session.flush()
        session.expunge_all()
    await set_active(user, new_account.account_id)
    return new_account


async def update_account(chaoxing_user: Chaoxing_User) -> Account:
    async with async_session.begin() as session:
        stmt = select(Account).filter(Account.uid == chaoxing_user.uid)
        orm_account = (await session.execute(stmt)).scalar_one()
        orm_account.cookie = chaoxing_user.cookie
        orm_account.valid = True
        orm_account.bind_time = int(round(time() * 1000))
        orm_account.username = chaoxing_user.username
        orm_account.department = chaoxing_user.department
        await session.flush()
        session.expunge_all()
    return orm_account


async def del_account(user: User, account_id: str) -> None:
    async with async_session.begin() as session:
        stmt = select(Account).filter(and_(Account.user_id == user.user_id, Account.account_id == account_id, Account.active == false()))
        orm_account = (await session.execute(stmt)).scalar_one_or_none()
        if orm_account is None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail="invalid_account")
        await session.delete(orm_account)


async def set_active(user: User, account_id: str) -> None:
    async with async_session.begin() as session:
        stmt = select(Account).filter(and_(Account.user_id == user.user_id, Account.deleted == false()))
        orm_accounts = (await session.execute(stmt)).scalars().all()
        for orm_account in orm_accounts:
            orm_account.active = True if orm_account.account_id == account_id else False


async def save_courses(account_id: str, user_id, chaoxing_user: Chaoxing_User) -> None:
    courses = await get_courses(cookie=chaoxing_user.cookie)
    async with async_session.begin() as session:
        # delete old courses
        stmt = select(Course).filter(Course.account_id == account_id)
        orm_courses = (await session.execute(stmt)).scalars().all()
        for orm_course in orm_courses:
            session.delete(orm_course)
        for course in courses:
            new_course = Course(account_id=account_id, user_id=user_id,  **course.__dict__)
            session.add(new_course)


async def course_refresh(user: User) -> None:
    async with async_session.begin() as session:
        stmt = select(Account).filter(and_(Account.user_id == user.user_id, Account.active == true()))
        orm_account = (await session.execute(stmt)).scalar_one_or_none()
        if orm_account is None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail="请绑定超星账号后刷新。")
    await save_courses(orm_account.account_id, user.user_id, orm_account.cookie)


async def get_course(user: User) -> list[Course]:
    if (active_account := await get_active(user, require=False)) is None:
        return []
    async with async_session.begin() as session:
        stmt = select(Course).filter(Course.account_id == active_account.account_id)
        orm_courses = (await session.execute(stmt)).scalars().all()
        session.expunge_all()
    return orm_courses


async def refresh(user: User, refresh_info: AccountRefreshIn) -> str:
    async with async_session.begin() as session:
        stmt = select(Account).filter(and_(Account.account_id == refresh_info.account_id, Account.user_id == user.user_id))
        orm_account = (await session.execute(stmt)).scalar_one()
    return await pwd_login(AccountIn(phone=orm_account.phone, password=refresh_info.password))


async def pre_order(course_id: str, user: User) -> str:
    """
    1. 检查course是不是属于这个user
    2. 检查money够不够
    3. 新建订单
    """
    async with async_session.begin() as session:
        stmt = select(Account).filter(and_(Account.user_id == user.user_id, Account.active == true())).options(selectinload(Account.courses))
        orm_account = (await session.execute(stmt)).scalar_one_or_none()
        if orm_account is None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail="账户异常。")
        orm_course = next((course for course in orm_account.courses if course.course_id == course_id), None)
        if orm_course is None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail="不存在此课程")
        new_course_order = CourseOrder(order_id=generate_random_string(constants.ORDER_ID_LENGTH),
                                       course_id=course_id,
                                       user_id=user.user_id,
                                       account_id=orm_account.account_id,
                                       account_phone=orm_account.phone,
                                       platform=PlatformEnum.chaoxing.value,
                                       course_name=orm_course.course_name,
                                       order_time=int(round(time() * 1000)),
                                       cost=constants.COST_ONCE)
        session.add(new_course_order)
    return new_course_order.order_id


async def get_pre_order(order_id: str, user_id: str) -> PreOrderOut:
    async with async_session.begin() as session:
        stmt = select(CourseOrder).filter(and_(CourseOrder.order_id == order_id, CourseOrder.user_id == user_id, CourseOrder.state == OrderStatusEnum.CONFIRMING.value)).options(selectinload(CourseOrder.course)).options(selectinload(CourseOrder.user))
        orm_order = (await session.execute(stmt)).scalar_one_or_none()
        if orm_order is None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail="订单不存在")
    return PreOrderOut(
        platform=orm_order.platform,
        phone=orm_order.account_phone,
        course_name=orm_order.course_name,
        course_id=orm_order.course_id,
        cost=constants.COST_ONCE,
        email=orm_order.user.email,
        is_open=orm_order.course.is_open
    )


async def cancel_order(order_id: str, user_id: str) -> None:
    async with async_session.begin() as session:
        stmt = select(CourseOrder).filter(and_(CourseOrder.order_id == order_id, CourseOrder.user_id == user_id, CourseOrder.state == OrderStatusEnum.CONFIRMING.value))
        orm_order = (await session.execute(stmt)).scalar_one_or_none()
        if orm_order is None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail="订单不存在")
        orm_order.state = OrderStatusEnum.CANCELLED.value


async def submit_order(order_id: str, user: User, backgrounds: BackgroundTasks) -> UserInfo:
    async with async_session.begin() as session:
        stmt = select(CourseOrder).filter(and_(CourseOrder.order_id == order_id, CourseOrder.user_id == user.user_id)).options(selectinload(CourseOrder.user))
        orm_order = (await session.execute(stmt)).scalar_one_or_none()
        try:
            if orm_order is None:
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED.value, detail="订单错误")
            if orm_order.user.userinfo.money < orm_order.cost:
                raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail="硬币不足")
            orm_order.user.userinfo.money -= orm_order.cost
            orm_order.state = OrderStatusEnum.IN_PROGRESS.value
            orm_setting = await modules.chaoxing.get_task_setting(user.user_id)
        except:
            orm_order.state = OrderStatusEnum.CANCELLED.value
            await session.commit()
            raise
    backgrounds.add_task(modules.chaoxing.complete_task, orm_order, from_dict(data_class=Chaoxing_Config, data=orm_setting.__dict__))
    backgrounds.add_task(modules.notification.send_notification,
                         user.user_id, constants.TIP_COURSEORDER_COMMIT_TITLE,
                         constants.TIP_COURSEORDER_COMMIT_MESSAGE.format(orm_order.order_id, f"{orm_order.account_phone}-{orm_order.course_name}"))
    return orm_order.user.userinfo


async def complete_task(order: CourseOrder, config: Chaoxing_Config) -> None:
    async with async_session.begin() as session:
        stmt = select(Course).filter(and_(Course.account_id == order.account_id, Course.course_id == order.course_id)).options(selectinload(Course.account))
        orm_course = (await session.execute(stmt)).scalar_one_or_none()
        if orm_course is None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT.value, detail="不存在此课程")
        session.expunge_all()
    try:
        await Chaoxing_Worker(order.order_id, orm_course, config)
        # 返回订单结果
        await modules.notification.send_notification(order.user_id, constants.TIP_COURSEORDER_OVER_TITLE, constants.TIP_COURSEORDER_OVER_MESSAGE.format(
            order.order_id,
            f"{order.account_phone}-{order.course_name}"
        ))
        await update_progress(order.order_id, 100, OrderStatusEnum.COMPLETED.value)
    except ChaoxingException as exc:
        await chaoxing_exception(ChaoxingException(order_id=order.order_id, detail=exc.detail))
    except Exception as exc:
        await chaoxing_exception(ChaoxingException(order_id=order.order_id, detail=f"未知错误:{exc}"))


async def chaoxing_exception(exc: ChaoxingException) -> None:
    # 记录日志
    await modules.notification.set_logger(exc.order_id, exc.detail)
    # 更新状态
    await modules.chaoxing.update_progress(exc.order_id, None, OrderStatusEnum.FAILED.value)
    # 发送im和notification
    await modules.notification.chaoxing_notification(exc.order_id, exc.detail)



async def update_progress(order_id: str, progress: int, state: int) -> None:
    async with async_session.begin() as session:
        stmt = select(CourseOrder).filter(CourseOrder.order_id == order_id)
        orm_order = (await session.execute(stmt)).scalar_one_or_none()
        orm_order.state = state
        if progress is not None:
            orm_order.progress = progress


async def get_orders(pagination: PaginationIn, user: User) -> (int, list[CourseOrder]):
    async with async_session.begin() as session:
        stmt_query = patch_query(CourseOrder, pagination).filter(CourseOrder.user_id == user.user_id)
        stmt_count = patch_count(CourseOrder, pagination).filter(CourseOrder.user_id == user.user_id)
        total = (await session.execute(stmt_count)).scalar()
        orm_orders = (await session.execute(stmt_query)).scalars().all()
        session.expunge_all()
    return total, orm_orders


async def get_task_setting(user_id: str) -> ChaoxingSetting:
    async with async_session.begin() as session:
        stmt = select(ChaoxingSetting).filter(ChaoxingSetting.user_id == user_id)
        orm_setting = (await session.execute(stmt)).scalar_one_or_none()
        session.expunge_all()
    return orm_setting


async def set_task_setting(user_id: str, setting: ChaoxingSettingIn) -> None:
    async with async_session.begin() as session:
        stmt = select(ChaoxingSetting).filter(ChaoxingSetting.user_id == user_id)
        orm_setting = (await session.execute(stmt)).scalar_one_or_none()
        orm_setting.work = setting.work
        orm_setting.exam = setting.exam
        orm_setting.task = setting.task
        orm_setting.searcher = setting.searcher
        orm_setting.sign = setting.sign
    return orm_setting

