#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import json
import aiohttp
# local
from app.extension.chaoxing.Searcher.base import BaseSearcher
from app.extension.chaoxing.schemas import Chaoxing_Question, Search_Response


class CxSearcher(BaseSearcher):

    paid = False
    enable = True
    doc = "慕课题库: 免费 高并发未知 准确率未知"
    web = "https://cx.icodef.com/"

    def __init__(self, question: Chaoxing_Question):
        super().__init__()
        self.base_url = "https://cx.icodef.com/wyn-nb?v=4"
        self.question = question
        self.response = None

    async def run(self) -> Search_Response:
        data = {
            "question": self.question.title
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.base_url, data=data) as response:
                html = await response.text()
        res_json = json.loads(html)
        self.response = Search_Response(
            status=res_json.get("code") == 1,
            question=self.question,
            times=0,  # Cx 没有返回剩余调用次数
            message=res_json.get("msg"),
            ans=res_json.get("data")
        )
        # 如果返回了答案,则处理
        if self.response.status:
            self.process_answer()
        return self.response
