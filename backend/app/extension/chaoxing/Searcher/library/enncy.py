#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import json
import aiohttp
from yarl import URL
# local
from app.extension.chaoxing.Searcher.base import BaseSearcher
from app.common import constants
from app.extension.chaoxing.schemas import Chaoxing_Question, Search_Response


class EnncySearcher(BaseSearcher):

    paid = True
    enable = True
    doc = "言溪题库: 1w/10元 限制高并发 准确率较高"
    web = "https://tk.enncy.cn"

    def __init__(self, question: Chaoxing_Question):
        super().__init__()
        self.base_url = "https://tk.enncy.cn/query"
        self.token = constants.ENNCY_TOKEN
        self.question = question
        self.response = None

    async def run(self) -> Search_Response:
        url = str(URL(self.base_url).with_query(
            token=self.token,
            title=self.question.title
        ))
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
        res_json = json.loads(html)
        self.response = Search_Response(
            status=res_json.get("code") == 1,
            question=self.question,
            times=res_json.get("data").get("times"),
            message=res_json.get("message"),
            ans=res_json.get("data").get("answer")
        )
        # 如果返回了答案,则处理
        if self.response.status:
            self.process_answer()
        return self.response
