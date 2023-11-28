#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
# local
from app.core.config import settings
from .logger import logMiddleware


middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=settings.BACKEND_CORS_CREDENTIALS,
        allow_methods=settings.BACKEND_CORS_METHODS,
        allow_headers=settings.BACKEND_CORS_HEADERS,
    )
]
