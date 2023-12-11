#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import random
import re
from difflib import SequenceMatcher
# local
from app.common import constants
from app.extension.chaoxing.schemas import Chaoxing_Question, Search_Response


class BaseSearcher:

    def __init__(self):
        self.base_url: str = None
        self.token: str = None
        self.question: Chaoxing_Question = None
        self.response: Search_Response = None

    async def run(self) -> Search_Response:
        pass

    def process_answer(self) -> None:
        self.response.status = True
        correct_answer = self.response.ans
        # 根据题目类型处理答案, 用字符串匹配算法计算相似度
        match self.question.type:
            case "单选题":
                best_match = (0, None)
                for option in self.question.options.values():
                    ratio = SequenceMatcher(a=option, b=correct_answer).ratio()
                    if ratio > best_match[0]:
                        best_match = (ratio, option)
                if best_match[0] >= constants.CORRECT_THRESHOLD:
                    self.response.ans = best_match[1]
                    print(f"选中了{self.response.ans}")
                else:
                    self.response.ans = random.choice(list(self.question.options.values()))
                    print(f"随机选择了{self.response.ans}")
            case "多选题":
                # 如果给定的答案不能分开的话,就算一个
                matches = []
                if len(answers := correct_answer.split('#')) < 1:
                    if len(answers := correct_answer.split(';')) < 1:
                        answers = correct_answer
                for option in self.question.options.values():
                    for answer in answers:
                        if SequenceMatcher(a=option, b=answer).ratio() > constants.CORRECT_THRESHOLD:
                            matches.append(option)
                self.response.ans = matches if matches else random.choice(list(self.question.options.values()))
            case "判断题":
                if re.search(r"(错|否|错误|false|×)", correct_answer):
                    self.response.ans = 'false'
                elif re.search(r"(对|是|正确|true|√)", correct_answer):
                    self.response.ans = 'true'
                else:
                    self.response.ans = random.choice(['true', 'false'])
            case "填空题":
                answer = correct_answer.split(";")
                self.response.ans = [answer[i] if i < len(answer) else "" for i in range(len(self.question.options))]
            case "简答题":
                self.response.ans = correct_answer
            case _:
                self.response.status = False
                print(f"不支持该题型:{self.question.type}")

