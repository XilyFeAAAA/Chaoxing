#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import jwt
from http import HTTPStatus
from fastapi import HTTPException
from passlib.context import CryptContext
# local
from app.core.config import settings

pwd_context = CryptContext(
    schemes=settings.CRYPT_SCHEMAS, deprecated=settings.CRYPT_DEPRECATED
)


async def create_token(subject: str) -> str:
    """create jwt token: contains user_id and expire_date"""
    payload = {"sub": subject}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return str(token)


def check_token(token: str) -> dict:
    """check the validity of token"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except Exception:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="invalid_token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """compare given password with hased password"""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    """get given password hashed"""
    return pwd_context.hash(plain_password)

