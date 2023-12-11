#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import asyncio
# local
from .book import Book
from .media import Media
from .read import Read
from .document import Document
from .live import Live
from .quiz import Quiz
from app.extension.chaoxing.schemas import Chaoxing_Config


class Task:

    def __init__(self, task: dict, headers: dict, config: Chaoxing_Config):
        self.task = task
        self.headers = headers
        self.config = config

    async def run(self) -> bool:
        attachments = self.task['attachments']
        defaults = self.task['defaults']
        asyncio_tasks = []
        for attachment in attachments:
            if attachment.get('job') is None:
                continue
            attachment_type = attachment.get("type")
            attachment_module = attachment.get('property').get('module')
            attachment_name = attachment.get('property').get('name')
            if attachment_type == 'video':
                if attachment_module == 'insertaudio' and self.config.task.audio_enable:
                    asyncio_tasks.append(asyncio.create_task(Media(attachment, self.headers, defaults, attachment_name, dtype="Audio").run()))
                elif self.config.task.video_enable:
                    asyncio_tasks.append(asyncio.create_task(Media(attachment, self.headers, defaults, attachment_name).run()))
            elif attachment_type == "read" and self.config.task.read_enable:
                asyncio_tasks.append(asyncio.create_task(Read(attachment, self.headers, defaults).run()))
            elif attachment_type == "document" and self.config.task.document_enable:
                asyncio_tasks.append(asyncio.create_task(Document(attachment, self.headers, defaults).run()))
            elif attachment_type == "live" and self.config.task.live_enable:
                asyncio_tasks.append(asyncio.create_task(Live(attachment, self.headers, defaults).run()))
            elif attachment_type == "workid" and self.config.task.quiz_enable:
                asyncio_tasks.append(asyncio.create_task(Quiz(attachment, self.headers, defaults, self.config).run()))
            elif "bookname" in attachment.get("property") and self.config.task.book_enable:
                asyncio_tasks.append(asyncio.create_task(Book(attachment, self.headers, defaults).run()))
            else:
                print(f"不支持的任务点类型:{attachment_type}")
                continue
        ret = await asyncio.gather(*asyncio_tasks)
        # 如果返回的task结果数组, True的数量和附件数一样就是ok了
        return ret.count(True) == len(attachments)
