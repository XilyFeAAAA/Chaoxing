#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import aiohttp
# local
from .schemas import *
from .utils import *
from .account import *
from .exception import *
from .course import CourseWorker
from .homework import HomeworkWorker
from app.models import Course
from app.common import constants


async def Chaoxing_Worker(order_id: str, course: Course, config: Chaoxing_Config):
    headers: dict = {
        'User-Agent': constants.HEADER_USERAGENT_PC,
        "Cookie": course.account.cookie
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        if config.task.enable:
            await CourseWorker(order_id, session, headers, course, config).run()
        if config.work.enable:
            await HomeworkWorker(order_id, session, course, config).run()
