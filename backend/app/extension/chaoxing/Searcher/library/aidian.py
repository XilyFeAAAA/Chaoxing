#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import json
import aiohttp
# local
from app.common import constants
from app.extension.chaoxing.Searcher.base import BaseSearcher
from app.extension.chaoxing.schemas import Chaoxing_Question, Search_Response


class AiDianSearcher(BaseSearcher):

    paid = False
    enable = True
    doc = "爱点题库: 区分免费和付费 免费限制速率4s/次 付费题库 1000次/10元"
    web = "https://www.51aidian.com/"

    def __init__(self, question: Chaoxing_Question):
        super().__init__()
        self.base_url = "http://new.api.51aidian.com/publics/newapi/freedirect"
        self.token = constants.AIDIAN_TOKEN
        self.question = question
        self.response = None

    async def run(self) -> Search_Response:
        data = {
            "question": self.question.title,
            "token": self.token
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.base_url, data=data) as response:
                html = await response.text()
        res_json = json.loads(html)
        status = res_json.get("code") == 1
        self.response = Search_Response(
            status=status,
            question=self.question,
            times=0,  # 没有返回剩余调用次数
            message=res_json.get("msg"),
            ans="#".join(res_json.get("qlist")[0].get("answer")) if status else None
        )
        # 如果返回了答案,则处理
        if self.response.status:
            self.process_answer()
        return self.response
