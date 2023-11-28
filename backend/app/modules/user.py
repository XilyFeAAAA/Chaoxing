#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy import select, false, and_, true, update
# local
from app.common import constants
from app.models import User, UserInfo
from app.core.db import async_session
from app.core.security import hash_password
from app.schemas.request import UserIn, UserInfoIn
from app.utils.number_helper import generate_random_num


async def get_user_by_userid(user_id: str) -> User | None:
    """obtain user info through its id"""
    async with async_session.begin() as session:
        stmt = select(User).filter(and_(User.user_id == user_id, User.deleted == false()))
        orm_user = (await session.execute(stmt)).scalar_one_or_none()
        session.expunge(orm_user)
        return orm_user


async def get_user_by_email(email: str) -> User | None:
    """obtain user info through its email"""
    async with async_session.begin() as session:
        stmt = select(User).filter(and_(User.email == email, User.deleted == false()))
        orm_user = (await session.execute(stmt)).scalar_one_or_none()
        session.expunge(orm_user)
        return orm_user


async def create_user(user_in: UserIn) -> User:
    """create a new user"""
    async with async_session.begin() as session:
        # async_session.begin() maintains a begin/commit/rollback block
        stmt = select(User).filter(and_(User.email == user_in.email, User.deleted == false()))
        orm_user = (await session.execute(stmt)).scalar_one_or_none()
        if orm_user is not None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="invaild_user_emial")
        hashed_password = hash_password(user_in.password)
        # convert basemodel into dict
        # not all the fields are needed, redundant fields should be discarded
        user_data = user_in.model_dump(include=["email"])  # whitelist is always better than blacklist
        user_data["hashed_password"] = hashed_password
        user_data["user_id"] = generate_random_num(constants.USER_ID_LENGTH)
        orm_userinfo = UserInfo(user_id=user_data["user_id"], nickname=user_in.nickname)
        orm_user = User(**user_data)
        session.add_all([orm_user, orm_userinfo])
        await session.flush()
        await session.refresh(orm_user)  # update orm_user.info
        session.expunge_all()  # keep alive
    return orm_user


async def del_user(user_id: str) -> None:
    """delete user"""
    async with async_session.begin() as session:
        stmt = select(User).filter(and_(User.user_id == user_id, User.deleted == false()))
        orm_user = (await session.execute(stmt)).scalar_one_or_none()
        if orm_user is None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="the user doesn't exist")
        orm_user.deleted = true()


async def pwd_change(user_id: str, new_pwd: str) -> None:
    """change password"""
    async with async_session.begin() as session:
        stmt = select(User).filter(and_(User.user_id == user_id, User.deleted == false()))
        orm_user = (await session.execute(stmt)).scalar_one_or_none()
        if orm_user is None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="the user doesn't exist")
        orm_user.hashed_password = hash_password(new_pwd)


async def verify_email(email: str) -> None:
    """No return value, but raise exception if email exists"""
    async with async_session.begin() as session:
        stmt = select(User).filter(and_(User.email == email, User.deleted == false()))
        orm_user = (await session.execute(stmt)).scalar_one_or_none()
        if orm_user is not None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="the email is invaild")


async def update_info(user_id: str, new_info: UserInfoIn) -> UserInfo:
    """update user's info """
    async with async_session.begin() as session:
        stmt = select(User).filter(and_(User.user_id == user_id, User.deleted == false()))
        orm_user = (await session.execute(stmt)).scalar_one_or_none()
        if orm_user is None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="the user doesn't exist")
        stmt = update(UserInfo).filter(and_(UserInfo.user_id == user_id, UserInfo.deleted == false())).values(new_info.model_dump())
        await session.execute(stmt)
        await session.flush()
        await session.refresh(orm_user)
        session.expunge(orm_user)
    return orm_user.info
