#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import jwt
from http import HTTPStatus
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
# local
from app.common import constants
from app.core.config import settings

pwd_context = CryptContext(
    schemes=settings.CRYPT_SCHEMAS, deprecated=settings.CRYPT_DEPRECATED
)


async def create_token(subject: str, expire_delta: timedelta = timedelta(
    minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES
        )) -> str:
    """create jwt token: contains user_id and expire_date"""
    expire_date = datetime.utcnow() + expire_delta
    payload = {"exp": expire_date, "sub": str(subject)}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return str(token)


def check_token(token: str) -> dict:
    """check the validity of token"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        expire_date = datetime.fromtimestamp(payload["exp"])
        if datetime.utcnow() > expire_date.astimezone(timezone.utc).replace(tzinfo=None):
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="token expired")
        return payload
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="invaild token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """compare given password with hased password"""
    print(plain_password, hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    """get given password hashed"""
    return pwd_context.hash(plain_password)

