#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from urllib import parse


class Course:
    def __init__(self, course_id: str, class_id: str, url: str, course_name: str, course_author: str, cpi: str = "", headers: dict = {}, ifOpen: bool = True):
        self.course_id = course_id
        self.class_id = class_id
        self.url = url
        self.course_name = course_name
        self.course_author = course_author
        if cpi == "":
            self.cpi = parse.parse_qs(parse.urlparse(self.url).query).get("cpi")[0]
        self.chapter_list = []
        self.mission_all = 0
        self.mission_fn = 0
        self._child_chapter_list = []
        self.url_log = ""
        self.headers = headers
        self.ifOpen = ifOpen
        self._jobEnc = None
