#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import json
import aiohttp
from yarl import URL
# local
from app.extension.chaoxing.Searcher.base import BaseSearcher
from app.common import constants
from app.extension.chaoxing.schemas import Chaoxing_Question, Search_Response


class EverySearcher(BaseSearcher):

    paid = True
    enable = True
    doc = "Every题库: 10000点/10元 高级模式搜索正确率较高"
    web = "https://q.icodef.com/"

    def __init__(self, question: Chaoxing_Question):
        super().__init__()
        self.base_url = "https://q.icodef.com/api/v1/q/"
        self.token = constants.EVERY_TOKEN
        self.question = question
        self.response = None

    async def run(self) -> Search_Response:
        url = str(URL(self.base_url + self.question.title).with_query(
            token=self.token,
            simple="true"
        ))
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
        res_json = json.loads(html)
        self.response = Search_Response(
            status=res_json.get("code") == 0,
            question=self.question,
            times=0,  # EveryApi 没有返回剩余调用次数
            message=res_json.get("msg"),
            ans=res_json.get("data")
        )
        # 如果返回了答案,则处理
        if self.response.status:
            self.process_answer()
        return self.response
