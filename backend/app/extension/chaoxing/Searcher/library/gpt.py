#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import json

import aiohttp

# local
from app.extension.chaoxing.Searcher.base import BaseSearcher
from app.extension.chaoxing.schemas import Chaoxing_Question, Search_Response


class GptSearcher(BaseSearcher):
    paid = False
    enable = True
    doc = "ChatAnyWhere: GPT分付费和免费"
    web = "https://github.com/chatanywhere/GPT_API_free"

    def __init__(self, question: Chaoxing_Question):
        super().__init__()
        self.base_url = "https://api.chatanywhere.com.cn/v1/chat/completions"
        self.question = question
        self.response = None

    async def run(self) -> Search_Response:
        if self.question.type != "简答题":
            return Search_Response(
                status=False,
                question=self.question,
                times=0,
                message="GPT仅支持简答题",
                ans=None
            )
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{
                "role": "user",
                "content": f"简述下面问题:{self.question.options.keys()[0]}"
            }]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.base_url, data=data) as response:
                html = await response.text()
        res_json = json.loads(html)
        return Search_Response(
            status=True,
            question=self.question,
            times=0,
            message="gpt回答仅供参考",
            ans=res_json.get("choices")[0]["message"]["content"]
        )
