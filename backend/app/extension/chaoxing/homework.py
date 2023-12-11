#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import json
from urllib import parse
from urllib.parse import urlparse
from yarl import URL
from lxml import etree
# local
from app.models import Course
from app.common import constants
from app.modules.notification import set_logger
from app.extension.chaoxing.utils import *
from app.extension.chaoxing.schemas import *
from app.extension.chaoxing.Searcher import SearcherManager
from app.extension.chaoxing.exception import ChaoxingException


class HomeworkWorker:

    def __init__(self, order_id: str, session, course: Course, config: Chaoxing_Config):
        self.order_id = order_id
        self.session = session
        self.course = course
        self.config = config
        self.homeworks: list[Chaoxing_Homework] = []

    async def run(self):
        await set_logger(self.order_id, f"开始获取作业信息")
        await self.get_homework_info()
        await set_logger(self.order_id, f"成功获取作业信息")
        for homework in self.homeworks:
            await self.complete(homework)

    async def complete(self, homework: Chaoxing_Homework) -> None:
        if not homework.available:
            return False
        done = 0
        async for index, response in SearcherManager(config=self.config.searcher, questions=homework.questions):
            if response.status:
                homework.questions[index].answer = parser(response)
                done += 1
        await set_logger(self.order_id, f"共完成{done}项作业")
        form = await self.create_form()
        if done == len(homework.questions):
            await set_logger(self.order_id, f"作业{homework.name}全部完成")
            if not self.config.work.save:
                try:
                    # 提交前还要发送一个请求
                    if await self.precommit_form(form):
                        res = await self.commit_form(form)
                        return res.get('status')
                    else:
                        error = f"作业{homework.name}预提交失败"
                        await set_logger(self.order_id, error)
                        raise ChaoxingException(detail=error)
                except Exception as e:
                    error = f"作业{homework.name}提交失败"
                    await set_logger(self.order_id, error)
                    raise ChaoxingException(detail=error)
        res = await self.temp_commit(form)
        if not res.get("status"):
            error = f"作业{homework.name}暂存失败"
            await set_logger(self.order_id, error)
            raise ChaoxingException(detail=error)

    async def create_form(self, homework: Chaoxing_Homework) -> Homework_Form:
        async with self.session.get(homework.url) as response:
            html = await response.text()
        ele_root = etree.HTML(html)
        action_url = xpath_first(ele_root, "//form[@id='submitForm']/@action")
        # 构造action-url查询参数的字典
        action_params = urlparse(action_url)
        action_query_dict = parse.parse_qs(action_params.query)
        # 构造homework_url查询参数的字典
        homework_params = urlparse(homework.url)
        homework_query_dict = parse.parse_qs(homework_params.query)
        ele_inputs = ele_root.xpath('//input')
        datas = {}
        for ele_input in ele_inputs:
            _id = xpath_first(ele_input, './@id')
            _value = xpath_first(ele_input, './@value')
            if _id:
                datas[_id] = _value
        datas = {
            "_classId": action_query_dict.get("_classId", "")[0],
            "courseid": action_query_dict.get("courseid", "")[0],
            "token": action_query_dict.get("token", "")[0],
            "totalQuestionNum": action_query_dict.get("totalQuestionNum", ""),
            "ua": "pc",
            "formType": "post",
            "saveStatus": "1",
            "version": "1",
            "workRelationId": homework_query_dict.get("workId", "")[0],
            "workAnswerId": homework_query_dict.get("answerId", "")[0],
            "standardEnc": homework_query_dict.get("standardEnc", ""),
            **datas
        }
        params = {
            "_classId": datas.get("_classId"),
            "courseid": datas.get("courseid"),
            "token": datas.get("token"),
            "totalQuestionNum": datas.get("totalQuestionNum"),
            "ua": "pc",
            "formType": "post",
            "saveStatus": "1",
            "version": "1",
        }
        data = {
            "courseId": datas.get("courseid"),
            "classId": datas.get("_classId"),
            "knowledgeId": datas.get("knowledgeId"),
            "cpi": datas.get("cpi"),
            "workRelationId": datas.get("workRelationId"),
            "workAnswerId": datas.get("workAnswerId"),
            "jobid": datas.get("jobid"),
            "standardEnc": datas.get("standardEnc"),
            "enc_work": datas.get("token"),
            "totalQuestionNum": datas.get("totalQuestionNum"),
            "pyFlag": datas.get("pyFlag"),
            "answerwqbid": all_question_id(homework.questions),
            "mooc2": datas.get("mooc2"),
            "randomOptions": datas.get("randomOptions"),
        }
        # 把答案添加进data
        return Homework_Form(params, transform_question(data, homework.questions))

    async def commit_form(self, form: Homework_Form) -> dict:
        commit_url = str(URL(constants.URL_COMMIT_HOMEWORK).with_query(**form.params))
        async with self.session.post(commit_url, data=form.data) as response:
            html = await response.text()
        return json.loads(html)

    async def precommit_form(self, form: Homework_Form) -> bool:
        precommit_url = str(URL(constants.URL_PRECOMMIT_HOMEWORK).with_query(
            courseId=form.data.get("courseId"),
            classId=form.data.get("classId"),
            cpi=form.data.get("cpi"),
        ))
        async with self.session.get(precommit_url) as response:
            html = await response.text()
        return json.loads(html).get("status") == 3

    async def temp_commit(self, form: Homework_Form) -> dict:
        temp_url = str(URL(constants.URL_COMMIT_HOMEWORK).with_query(pyFlag=1, **form.params))
        temp_data = form.data.copy()
        temp_data['pyFlag'] = 1
        async with self.session.post(temp_url, data=temp_data) as response:
            html = await response.text()
        return json.loads(html)

    async def get_homework_info(self):

        def get_options(element, qtype) -> dict:
            options = {}
            ele_options = element.xpath("./div[contains(@class, 'stem_answer')]/div")
            if qtype in ["单选题", "多选题", "判断题"]:
                for ele_option in ele_options:
                    key = xpath_first(ele_option, './span[1]/text()')
                    value = xpath_first(ele_option, './div[1]/p[1]/text()')
                    options[key] = value
            elif qtype in ["填空题"]:
                # 填空题几个option就是几个空
                for ele_option in ele_options:
                    key = xpath_first(ele_option, "./span[@class='tiankong fl']/text()")
                    options[key] = ""
            return options

        self.homeworks.clear()
        await self.get_homeworks()
        for homework in self.homeworks:
            if homework.available:
                async with self.session.get(homework.url) as response:
                    html = await response.text()
                ele_root = etree.HTML(html)
                ele_questions = ele_root.xpath("//div[@class='padBom50 m fontLabel']")
                for ele_question in ele_questions:
                    qtype = xpath_first(ele_question, "./@typename")
                    homework.questions.append(Chaoxing_Question(
                        id=xpath_first(ele_question, './@data'),
                        title=xpath_first(ele_question, "./h3[1]/text()[2]"),
                        type=qtype,
                        answer=None,
                        options=get_options(ele_question, qtype),
                    ))

    async def get_homeworks(self):
        cpi = parse.parse_qs(parse.urlparse(self.course.url).query).get("cpi")[0]
        course_url = str(URL("https://mooc1.chaoxing.com/visit/stucoursemiddle").with_query(
            courseid=self.course.class_id,
            clazzid=self.course.class_id,
            cpi=cpi,
            ismooc2=1
        ))
        async with self.session.get(course_url) as response:
            html = await response.text()
        ele_root = etree.HTML(html)
        work_enc = xpath_first(ele_root, "//input[@id='workEnc']/@value")
        homework_url = str(URL("https://mooc1.chaoxing.com/mooc2/work/list").with_query(
            classId=self.course.class_id,
            courseId=self.course.course_id,
            ut='s',
            cpi=cpi,
            enc=work_enc,
        ))
        async with self.session.get(homework_url, allow_redirects=True) as response:
            html = await response.text()
        ele_root = etree.HTML(html)
        ele_lis = ele_root.xpath("//div[@class='bottomList']/ul/li")
        for ele_li in ele_lis:
            url = xpath_first(ele_li, "./@data")
            name = xpath_first(ele_li, "./div[@class='right-content']/p[@class='overHidden2 fl']/text()")
            state = xpath_first(ele_li, "./div[@class='right-content']/p[@class='status fl']/text()")
            query = parse.parse_qs(parse.urlparse(url).query)
            icon_class = xpath_first(ele_li, "./div[1]/@class")
            self.homeworks.append(Chaoxing_Homework(
                name=name,
                url=url,
                work_id=query.get("workId"),
                answer_id=query.get("answerId"),
                enc=query.get("enc"),
                available=state == '未交' and "icon-zy-g" not in icon_class,
                questions=[]
            ))

