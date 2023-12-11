#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from dataclasses import dataclass
# local


@dataclass
class Chaoxing_User:
    username: str
    phone: str
    uid: str
    cookie: str
    department: str


@dataclass
class Chaoxing_Course:
    course_id: str
    class_id: str
    url: str
    img_url: str
    course_name: str
    classroom: str
    start_time: str
    course_teacher: str
    is_open: bool


@dataclass
class Chaoxing_Chapter:
    name: str
    depth: int
    knowledge_id: ""
    job_count: int
    state: int  # 0:已完成, 1:待完成, 2:锁定
    last_chapter: "Chaoxing_Chapter"


@dataclass
class Chaoxing_Catalog:
    name: str
    chapters: list[Chaoxing_Chapter]


@dataclass
class Chaoxing_Question:
    id: str
    type: str
    title: str
    options: dict
    answer: str | list[str]


@dataclass
class Chaoxing_Homework:
    name: str
    url: str
    available: bool
    work_id: str
    answer_id: str
    enc: str
    questions: list[Chaoxing_Question]


@dataclass
class Chaoxing_Qrcode:
    uuid: str
    enc: str


@dataclass
class Search_Response:
    status: bool
    message: str
    question: Chaoxing_Question
    times: int | None  # 接口剩余次数
    ans: str | list[str]


@dataclass
class Homework_Form:
    params: dict
    data: dict


@dataclass
class Searcher_Config:
    use_paid: bool  # 是否使用付费题库


@dataclass
class Task_Config:
    enable: bool  # 完成章节
    interval: int  # 间隔时间
    video_enable: bool  # 是否完成视频
    audio_enable: bool  # 是否完成音频
    read_enable: bool  # 是否完成阅读
    document_enable: bool  # 是否完成文档
    live_enable: bool  # 是否完成直播
    book_enable: bool  # 是否完成书籍
    quiz_enable: bool  # 是否完成章节测试


@dataclass
class Exam_Config:
    enable: bool  # 完成考试


@dataclass
class Sign_Config:
    enable: bool  # 完成签到


@dataclass
class Work_Config:
    enable: bool  # 完成作业
    random: bool  # 没有答案随机选择
    save: bool  # 保存不提交


@dataclass
class Chaoxing_Config:
    work: Work_Config
    exam: Exam_Config
    task: Task_Config
    sign: Sign_Config
    searcher: Searcher_Config



__all__ = ['Chaoxing_User',
           'Chaoxing_Course',
           'Chaoxing_Chapter',
           'Chaoxing_Catalog',
           'Chaoxing_Homework',
           'Chaoxing_Question',
           'Chaoxing_Qrcode',
           'Search_Response',
           'Homework_Form',
           'Chaoxing_Config',
           'Work_Config',
           'Exam_Config',
           'Task_Config',
           'Searcher_Config',
           'Sign_Config'
           ]
