#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import json

import aiohttp
from lxml import etree
from yarl import URL
from urllib import parse
from urllib.parse import urlparse
# local
from app.common import constants
from app.extension.chaoxing.Searcher import SearcherManager
from app.extension.chaoxing.schemas import Chaoxing_Question, Homework_Form, Chaoxing_Config
from app.extension.chaoxing.utils import xpath_first, transform_question, parser
from app.extension.chaoxing.decoder import Decoder

qtype_dict = {
    '0': "单选题",
    '1': "多选题",
    '2': "填空题",
    '3': "判断题",
    '4': "简答题",
    '6': "论述题"
}


class Quiz:
    def __init__(self, attachment: dict, headers: dict, defaults: dict, config: Chaoxing_Config):
        self.config = config
        self.headers = headers
        self.defaults = defaults
        self.attachment = attachment
        self.questions: list[Chaoxing_Question] = []
        self.font_dict: dict = {}
        self.html: str = ""

    async def run(self) -> bool:
        """
        1. 获取所有参数
        2. 获取所有题目
        """
        await self.get_quiz()
        await self.get_questions()
        # 先遍历每一个题目 再遍历所有searcher, 这样没答案的题目就会补上
        done = 0
        async for index, response in SearcherManager(config=self.config.searcher, questions=self.questions):
            if response.status:
                self.questions[index].answer = parser(response)
                done += 1
        form = await self.create_form()
        if done == len(self.questions):
            if not self.config.work.save:
                try:
                    # 提交前还要发送一个请求
                    if await self.precommit_form(form):
                        res = await self.commit_form(form)
                        return res.get('status')
                    else:
                        print("预提交失败")
                except Exception as e:
                    print("提交随堂测验错误", e)
                    raise e
        elif not self.config.work.save:
            # 如果设置了直接提交, 但是有题目搜不到答案, 应该暂存 并且提醒用户
            print("搜不到答案,提交暂存了")
        res = await self.temp_commit(form)
        return res.get("status")

    async def create_form(self) -> Homework_Form:
        ele_root = etree.HTML(self.html)
        ele_form = xpath_first(ele_root, "//div[@class='CeYan']/form[1]")
        action_url = xpath_first(ele_form, './@action')
        action_params = urlparse(action_url)
        datas = parse.parse_qs(action_params.query)
        ele_inputs = ele_form.xpath('//input')
        for ele_input in ele_inputs:
            _id = xpath_first(ele_input, './@id')
            _value = xpath_first(ele_input, './@value')
            if _id:
                datas[_id] = _value
        params = {
            "_classId": datas.get("classId"),
            "courseid": datas.get("courseId"),
            "token": datas.get("token"),
            "totalQuestionNum": datas.get("totalQuestionNum"),
            "ua": "pc",
            "formType": "post",
            "saveStatus": "1",
            "version": "1",
        }
        data = {
            "courseId": datas.get("courseId"),
            "classId": datas.get("classId"),
            "knowledgeId": datas.get("knowledgeId"),
            "cpi": datas.get("cpi"),
            "workRelationId": datas.get("workRelationId"),
            "workAnswerId": datas.get("workAnswerId"),
            "jobid": datas.get("jobid"),
            # "standardEnc": datas.get("standardEnc"),
            "enc_work": datas.get("enc_work"),
            "totalQuestionNum": datas.get("totalQuestionNum"),
            "pyFlag": datas.get("pyFlag"),
            "answerwqbid": self.all_question_id,
            "mooc2": datas.get("mooc2"),
            "randomOptions": datas.get("randomOptions"),
        }
        data = transform_question(data, self.questions)
        return Homework_Form(params, data)

    async def get_quiz(self):
        quiz_url = str(URL(constants.API_WORK).with_query(
            api=1,
            workId=self.attachment.get("property").get("workid"),
            jobid=self.attachment.get("jobid"),
            needRedirect="true",
            skipHeader="true",
            knowledgeid=self.defaults.get("knowledgeid"),
            ktoken=self.defaults.get("ktoken"),
            cpi=self.defaults.get("cpi"),
            ut="s",
            clazzId=self.defaults.get("clazzId"),
            type="",
            enc=self.attachment.get("enc"),
            mooc2=1,
            courseid=self.defaults.get("courseid")
        ))
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(quiz_url) as response:
                self.html = await response.text()

    async def get_questions(self):

        def get_options(element):
            options = {}
            if qtype in ["单选题", "多选题", "判断题"]:
                for ele_option in element.xpath(f'//li[@qid="{qid}"]'):
                    key = xpath_first(ele_option, './label[@class="fl before"]/span/text()')
                    value = xpath_first(ele_option, './a[@class="fl after"]/text()')
                    options[key] = value
            elif qtype in ["填空题"]:
                # 填空题可能有多个空
                for ele_option in element.xpath("//ul[1]/div[@class='blankItemDiv']"):
                    key = xpath_first(ele_option, "./span[1]/text()")
                    options[key] = ""
            return options

        decoder = Decoder(self.html)
        ele_root = etree.HTML(self.html)
        ele_questions = ele_root.xpath("//div[@class='TiMu newTiMu']")
        for ele_question in ele_questions:
            qid = xpath_first(ele_question, "./div[2]/input[starts-with(@id, 'answertype')]/@id")[10:]
            qtype = qtype_dict.get(xpath_first(ele_question, "./@data"))
            # 学习通字体加密
            self.questions.append(Chaoxing_Question(
                id=qid,
                title=decoder.translate(xpath_first(ele_question, "./div[1]/div/text()[2]").replace("\t", "")),
                type=qtype,
                answer=None,
                options=get_options(ele_question),
            ))

    @property
    def all_question_id(self) -> str:
        ids = ""
        for question in self.questions:
            ids += question.id + ','
        return ids

    async def commit_form(self, form: Homework_Form) -> dict:
        commit_url = str(URL(constants.URL_COMMIT_HOMEWORK).with_query(**form.params))
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(commit_url, data=form.data) as response:
                html = await response.text()
        return json.loads(html)

    async def precommit_form(self, form: Homework_Form) -> bool:
        precommit_url = str(URL(constants.URL_PRECOMMIT_HOMEWORK).with_query(
            courseId=form.data.get("courseId"),
            classId=form.data.get("classId"),
            cpi=form.data.get("cpi"),
        ))
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(precommit_url) as response:
                html = await response.text()
        return json.loads(html).get("status") == 3

    async def temp_commit(self, form: Homework_Form) -> dict:
        temp_url = str(URL(constants.URL_COMMIT_HOMEWORK).with_query(tempsave=1, **form.params))
        temp_data = form.data.copy()
        temp_data['pyFlag'] = 1
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(temp_url, data=temp_data) as response:
                html = await response.text()
        return json.loads(html)