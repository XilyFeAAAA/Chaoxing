#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from fastapi import APIRouter
from app.api.endpoints import test, auth, user, rbac, chaoxing

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(test.router, prefix="/test", tags=["test"])
api_router.include_router(rbac.router, prefix="/rbac", tags=["rbac"])
api_router.include_router(chaoxing.router, prefix="/chaoxing", tags=["chaoxing"])