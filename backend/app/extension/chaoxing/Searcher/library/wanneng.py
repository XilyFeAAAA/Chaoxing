#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import json
import aiohttp
# local
from app.extension.chaoxing.Searcher.base import BaseSearcher
from app.common import constants
from app.extension.chaoxing.schemas import Chaoxing_Question, Search_Response


class WannengSearcher(BaseSearcher):

    paid = True
    enable = False
    doc = "万能题库: 1000/10元 余额不足转免费题库 限制高并发 准确率较高"
    web = "https://lyck6.cn/pay"

    def __init__(self, question: Chaoxing_Question):
        super().__init__()
        self.base_url = "http://lyck6.cn/scriptService/api/autoAnswer"
        self.token = constants.ENNCY_TOKEN
        self.question = question
        self.response = None

    async def run(self) -> Search_Response:
        url = f"{self.base_url}/{constants.WANNENG_TOKEN}"
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

