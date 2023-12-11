#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import json
import aiohttp
from yarl import URL
# local
from app.extension.chaoxing.Searcher.base import BaseSearcher
from app.common import constants
from app.extension.chaoxing.schemas import Chaoxing_Question, Search_Response


class HeibookSearcher(BaseSearcher):

    paid = False
    enable = True
    doc = "嘿课题库: 免费 高并发未知 准确率较低"
    web = "http://dj.heibook.cn/"

    def __init__(self, question: Chaoxing_Question):
        super().__init__()
        self.base_url = "http://dj.heibook.cn/userapi"
        self.token = constants.HEIBOOK_TOKEN
        self.question = question
        self.response = None

    async def run(self) -> Search_Response:
        url = str(URL(self.base_url).with_query(
            token=self.token,
            question=self.question.title
        ))
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
        res_json = json.loads(html)
        status=res_json.get("code") == 1
        self.response = Search_Response(
            status=status,
            question=self.question,
            times=0,
            message=res_json.get("msg"),
            ans=res_json.get("data").get("answer") if status else None
        )
        # 如果返回了答案,则处理
        if self.response.status:
            self.process_answer()
        return self.response
