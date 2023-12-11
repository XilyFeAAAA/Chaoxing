#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import asyncio
import re
import json
import time
from yarl import URL
from lxml import etree
from urllib import parse
# local
from app.models import Course
from app.modules.notification import set_logger
from app.extension.chaoxing.utils import *
from app.extension.chaoxing.schemas import *
from app.extension.chaoxing.TaskPoints import Task
from app.extension.chaoxing.exception import ChaoxingException


class CourseWorker:

    def __init__(self, order_id: str, session, headers: dict, course: Course, config: Chaoxing_Config):
        self.order_id = order_id
        self.headers = headers
        self.session = session
        self.course = course
        self.config = config
        self.cpi = parse.parse_qs(parse.urlparse(course.url).query).get("cpi")[0]
        self.unlocked_chapters: list[Chaoxing_Chapter] = []
        self.locked_chapters: list[Chaoxing_Chapter] = []
        self.catalogs: list[Chaoxing_Catalog] = []

    async def run(self):
        await self.get_course_info()
        temp_chapters = [*self.locked_chapters, *self.unlocked_chapters]
        if self.unlocked_chapters:
            for chapter in self.unlocked_chapters:
                await set_logger(self.order_id, f"开始处理任务点{chapter.name}")
                if await self.complete(chapter):
                    # 全部任务点完成,则移除该任务
                    temp_chapters.remove(chapter)
                else:
                    await set_logger(self.order_id, f"任务点{chapter.name}完成失败")
        for chapter in self.locked_chapters:
            if chapter.last_chapter in temp_chapters:
                error = f"章节{chapter.name}的前置任务未完成,无法解锁。"
                await set_logger(self.order_id, error)
                raise ChaoxingException(detail=error)
            if await self.complete(chapter):
                # 全部任务点完成,则移除该任务
                temp_chapters.remove(chapter)
            else:
                await set_logger(self.order_id, f"任务点{chapter.name}完成失败")
    async def get_course_info(self):
        print("开始获取章节信息")
        await set_logger(self.order_id, "开始获取章节信息")
        await self.get_chapters()
        await set_logger(self.order_id, "成功获取课程信息")
        print("成功获取课程信息")
        for catalog in self.catalogs:
            for index, chapter in enumerate(catalog.chapters):
                # 还没完成和锁定的都要加进去
                if chapter.state != 0:
                    # 如果是锁定的, 记录上一章节
                    if not chapter.state == 2 and index:
                        chapter.last_chapter = catalog.chapters[index - 1]
                        self.locked_chapters.append(chapter)
                    # 区分锁定章节和未锁定
                    self.unlocked_chapters.append(chapter)

    async def get_chapters(self):

        def recursion_chapter(element, depth):
            nonlocal child_chapters
            knowledge_id = xpath_first(element, "./div[1]/div[1]/div[@class='inputCheck fl']/input/@value") or ""
            progress_class = xpath_first(element, "./div[1]/div[1]/div[@class='catalog_task']/div[1]/@class")
            state = 0 if 'catalog_tishi56' in progress_class else 1 if 'catalog_tishi120' in progress_class else 2
            child_chapters.append(Chaoxing_Chapter(name=("🔒  " if state == 2 else '') + xpath_first(
                xpath_first(element, "./div/div/div[@class='catalog_name newCatalog_name']/a[@class='clicktitle']"), "string(.)").strip(),
                                                   depth=depth,
                                                   knowledge_id=knowledge_id,
                                                   job_count=int(xpath_first(element, "./div[1]/div[1]/div[@class='catalog_task']/input/@value") or "0"),
                                                   state=state,
                                                   last_chapter=None))
            ele_chapters = element.xpath("./ul/li")
            if ele_chapters:
                for ele_chapter in ele_chapters:
                    recursion_chapter(ele_chapter, depth + 1)

        self.catalogs.clear()
        _url = str(URL("https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/studentcourse").with_query(
            courseid=self.course.course_id,
            clazzid=self.course.class_id,
            cpi=self.cpi,
            ut="s",
            t=int(round(time.time() * 1000))
        ))
        async with self.session.get(_url) as response:
            html = await response.text()
        ele = etree.HTML(html)
        ele_root = xpath_first(ele, "//div[@class='fanyaChapterWhite']")
        ele_units = ele_root.xpath("./div[2]/div[@class='chapter_td']/div[@class='chapter_unit']")
        child_chapters = []
        for ele_unit in ele_units:
            unit_catalog_name = xpath_first(ele_unit, "./div[1]/div[1]/div[@class='catalog_name newCatalog_name']/a/span/text()").strip()
            for ele_li in ele_unit.xpath("./div[2]/ul/li"):
                recursion_chapter(ele_li, 0)
            self.catalogs.append(Chaoxing_Catalog(name=unit_catalog_name, chapters=child_chapters.copy()))
            child_chapters.clear()

    async def get_chapter_info(self, chapter: Chaoxing_Chapter) -> list:
        """获得章节任务点"""
        page_count = await self.read_count(chapter.knowledge_id)
        tasks = []
        for page in range(page_count):
            try:
                media_url = str(URL("https://mooc1.chaoxing.com/knowledge/cards").with_query(
                    clazzid=self.course.class_id,
                    courseid=self.course.course_id,
                    knowledgeid=chapter.knowledge_id,
                    num=page,
                    ut="s",
                    cpi=self.cpi,
                    v="20160407-1"
                ))
                async with self.session.get(media_url) as response:
                    html = await response.text()
                media_HTML = etree.HTML(html)
                media_text = xpath_first(media_HTML, "//body/script[1]/text()")
                datas_raw = re.findall(r"mArg = ({[\s\S]*)}catch", media_text).pop()
                datas = json.loads(datas_raw.strip()[:-1])
                tasks.append(datas)
            except:
                continue
        return tasks

    async def read_count(self, chapterId: str) -> int:
        _url = str(URL("https://mooc1.chaoxing.com/mycourse/studentstudyAjax").with_query(
            courseId=self.course.course_id,
            clazzid=self.course.class_id,
            chapterId=chapterId,
            cpi=self.cpi,
            verificationcode="",
            mooc2=1
        ))
        async with self.session.get(_url) as response:
            html = await response.text()
        rsp_HTML = etree.HTML(html)
        return int(xpath_first(rsp_HTML, "//input[@id='cardcount']/@value"))

    async def complete(self, chapter: Chaoxing_Chapter) -> bool:
        await set_logger(self.order_id, f"开始获取{chapter.name}任务点")
        tasks = await self.get_chapter_info(chapter)
        await set_logger(self.order_id, f"成功获取{chapter.name}任务点")
        if tasks:
            asyncio_tasks = []
            # 处理章节里的每个任务
            for task in tasks:
                asyncio_tasks.append(asyncio.create_task(Task(task, self.headers, self.config).run()))
            ret = await asyncio.gather(*asyncio_tasks)
            return ret.count(True) == len(tasks)
        return True
