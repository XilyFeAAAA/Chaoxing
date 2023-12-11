#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import time
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select, false, and_, func, true

# local
from app.common import constants
from app.core.db import async_session
from app.models import Notification, CourseOrder, Log
from app.utils.number_helper import generate_random_num


async def get_notification(user_id: str) -> (int, list[Notification]):
    async with async_session.begin() as session:
        stmt = select(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_time.desc())
        not_read = (
            await session.execute(select(func.count(Notification.id)).filter(and_(Notification.user_id == user_id, Notification.read == false())))).scalar()
        orm_notifications = (await session.execute(stmt)).scalars().all()
        session.expunge_all()
    return not_read, orm_notifications


async def send_notification(user_id: str, title: str, message: str) -> None:
    new_notification = Notification(
        notification_id=generate_random_num(constants.MESSAGE_ID_LENGTH),
        title=title,
        user_id=user_id,
        message=message,
        created_time=int(round(time.time() * 1000))
    )
    async with async_session.begin() as session:
        session.add(new_notification)


async def chaoxing_notification(order_id: str, detail: str) -> None:
    async with async_session.begin() as session:
        stmt = select(CourseOrder).filter(CourseOrder.order_id == order_id)
        orm_order = (await session.execute(stmt)).scalar_one_or_none()
        if orm_order is None:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail="订单不存在")
    await send_notification(orm_order.user_id,
                            constants.TIP_COURSEORDER_FAIL_TITLE,
                            constants.TIP_COURSEORDER_FAIL_MESSAGE.format(
                                orm_order.order_id,
                                f"{orm_order.account_phone}-{orm_order.course_name}",
                                detail
                            ))


async def del_notification(user_id: str) -> int:
    async with async_session.begin() as session:
        stmt = select(Notification).filter(Notification.user_id == user_id)
        orm_notificaions = (await session.execute(stmt)).scalars().all()
        count = len(orm_notificaions)
        for _ in orm_notificaions:
            await session.delete(_)
    return count


async def batch_read(ids: list[str], user_id: str) -> int:
    async with async_session.begin() as session:
        stmt = select(Notification).filter(and_(Notification.user_id == user_id, Notification.read == false(), Notification.notification_id.in_(ids)))
        orm_notifications = (await session.execute(stmt)).scalars().all()
        count = len(orm_notifications)
        for orm_notification in orm_notifications:
            orm_notification.read = true()
    return count


async def set_logger(order_id: str, info: str) -> None:
    new_log = Log(order_id=order_id, info=info, log_time=int(round(time.time() * 1000)))
    async with async_session.begin() as session:
        session.add(new_log)
