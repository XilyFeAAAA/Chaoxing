#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import secrets
from pathlib import Path
from datetime import timedelta
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """global app config"""
    # project
    HOST: str = "127.0.0.1"
    PORT: int = 7070
    SERVER_NAME: str = "ChaoXing"
    API_V1_STR: str = ""
    API_V1_TAG: list[str] = ["api"]
    # cors
    BACKEND_CORS_CREDENTIALS: bool = True
    BACKEND_CORS_ORIGINS: list = ["http://localhost:5173"]
    BACKEND_CORS_METHODS: list = ["*"]
    BACKEND_CORS_HEADERS: list = ["*"]
    # logger
    LOG_PATH: Path = Path(".") / "app/logs"
    # auth
    OAUTH2_PATH: str = "/auth/access-token"
    CRYPT_SCHEMAS: list[str] = ["bcrypt"]
    CRYPT_DEPRECATED: str = "auto"
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SESSION_KEY: str = secrets.token_urlsafe(32)
    # db
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: str = "3306"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "123456"
    MYSQL_DB: str = "chaoxing"
    # email
    SMTP_TLS: bool = True
    SMTP_PORT: int = 465
    SMTP_HOST: str = "smtp.qq.com"
    SMTP_USER: str = "ENTER_EMAIL_USER_HERE"
    SMTP_PASSWORD: str = "ENTER_EMAIL_CREDIT_HERE"
    EMAILS_FROM_EMAIL: str = "Email"
    EMAILS_FROM_NAME: str = "Smart HealthCare"
    # redis
    REDIS_HOST: str = "localhost"
    REDIS_TIMEOUT: int = 5
    REDIS_KEY_EXPIRE_TIMEDELTA: timedelta = timedelta(minutes=5)

    class Config:
        case_sensitive = True


settings = Settings()
