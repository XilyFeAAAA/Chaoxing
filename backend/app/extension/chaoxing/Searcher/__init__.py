#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from app.extension.chaoxing.Searcher.base import BaseSearcher
from app.extension.chaoxing.Searcher.library import searchers
from app.extension.chaoxing.schemas import Searcher_Config, Chaoxing_Question, Search_Response


class SearcherManager:
    """
    class SearcherManager works to generate an async iterator
    usage:
        async for item in SearcherManager(setting, questions):
            print(item)  # Search_Response
    """

    def __init__(self, config: Searcher_Config, questions: list[Chaoxing_Question]):
        self.index = 0
        self.questions = questions
        self.searchers: list = searchers
        if not config.use_paid:
            self.searchers = filter(lambda searcher: not searcher.paid, self.searchers)

    def __aiter__(self):
        return self

    async def __anext__(self) -> (int, Search_Response):
        if self.index >= len(self.questions):
            raise StopAsyncIteration
        response = Search_Response(status=False, message=None, question=None, times=None, ans=None)
        for searcher in self.searchers:
            response = await searcher(self.questions[self.index]).run()
            if response.status:
                break
        self.index += 1
        return self.index - 1, response
