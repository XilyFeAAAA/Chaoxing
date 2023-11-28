#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import aiofiles
import aiosmtplib
from typing import Any
from jinja2 import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# local
from app.core.config import settings


async def send_email(
        email_to: str,
        subject_template: str = "",
        html_template: str = "",
        environment: dict[str, Any] = None) -> None:
    # 创建带有HTML内容的邮件消息对象
    message = MIMEMultipart('related')
    message['Subject'] = Template(subject_template).render(environment)
    message['From'] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
    message['To'] = email_to

    html = Template(html_template).render(environment)
    html_part = MIMEText(html, 'html')
    message.attach(html_part)

    # 设置SMTP服务器选项
    smtp_options = {
        'hostname': settings.SMTP_HOST,
        'port': settings.SMTP_PORT,
        'use_tls': settings.SMTP_TLS,
    }
    if settings.SMTP_USER:
        smtp_options['username'] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options['password'] = settings.SMTP_PASSWORD

    # 异步连接SMTP服务器并发送邮件
    async with aiosmtplib.SMTP(**smtp_options) as smtp:
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        await smtp.send_message(message)


async def send_register_email() -> None:
    """send email when new user registered"""
    pass
