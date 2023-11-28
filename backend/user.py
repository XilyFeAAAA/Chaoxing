#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import json
import re
import time
from lxml import etree

import requests
import http
from course import Course
from utils import encrypt_des, xpath_first


class User:

    def __init__(self, phone: str = "", password: str = "", cookie: str = ""):
        self._cookie: str = cookie
        self._headers: dict = {}
        self.courses: list[Course] = []
        self.username: str = ""
        self._phone: str = phone
        self._password: str = password
        self.uid: str = ""
        self._session = requests.session()

    def get(self, url: str, headers: dict, full: bool = False) -> str | requests.Response:
        """package the get request"""
        self._session.headers.clear()
        self._session.headers.update(headers)
        response = self._session.get(url=url)
        return response if full else response.text

    def post(self, url: str, headers: dict, data: str | dict = None, full: bool = False) -> str | requests.Response:
        """package the post request"""
        self._session.headers.clear()
        self._session.headers.update(headers)
        response = self._session.post(url=url, data=data)
        return response if full else response.text

    def sign(self):
        """login"""
        if self._cookie:
            self._headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
                "Cookie": self._cookie
            }
            if self._check():
                self.uid = re.findall(r"_uid=(\d+);", self._cookie)[0] if re.findall(r"_uid=(\d+);", self._cookie) else ""
            else:
                print("cookie失效")
        else:
            login_headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'passport2.chaoxing.com',
                'Origin': 'https://passport2.chaoxing.com',
                'Referer': 'https://passport2.chaoxing.com/login?loginType=4&fid=314&newversion=true&refer=http://i.mooc.chaoxing.com',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
                'X-Requested-With': 'XMLHttpRequest'
            }
            encrypt_pwd = encrypt_des(self._password, "u2oh6Vu^").decode('utf-8')
            response = self.post(url="https://passport2.chaoxing.com/fanyalogin",
                                 headers=login_headers,
                                 data=f"fid=314&uname={self._phone}&password={encrypt_pwd}&refer=http%253A%252F%252Fi.mooc.chaoxing.com&t=true",
                                 full=True)
            if response.status_code == http.HTTPStatus.OK.value:
                res_json = json.loads(response.text)
                if res_json.get("status"):
                    self.username = res_json.get("name")
                    self.uid = response.cookies.get("_uid")
                    cookie = ""
                    for item in response.cookies:
                        cookie = cookie + item.name + '=' + item.value + ';'
                    self._cookie = cookie
                    self._headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51'
                    }
                else:
                    print(res_json.get("msg2"))
            else:
                print("request请求错误")

    def _check(self) -> bool:
        """check if logined"""
        check_url = f"https://i.chaoxing.com/base/settings?t={time.time()}"
        check_headers = {
            'Refer': f'https://i.chaoxing.com/base?t={time.time()}'
        }
        check_headers.update(self._headers)
        response = requests.get(url=check_url, headers=check_headers, allow_redirects=False)
        return response.status_code == http.HTTPStatus.OK.value


    def get_courses(self):
        self.courses.clear()
        html = self.get(
            url="https://mooc2-ans.chaoxing.com/mooc2-ans/visit/courses/list?v=1675234609566&rss=1&start=0&size=500&catalogId=0&superstarClass=0&searchname=",
            headers=self._headers)
        ele = etree.HTML(html)
        course_ele = ele.xpath("//ul[@id='courseList']/li")
        for item in course_ele:
            tmp_url = xpath_first(item, "./div[2]/h3/a/@href")
            if tmp_url.startswith("http"):
                # 如果为自己教授的课则无协议头
                course = Course(course_id=xpath_first(item, "./div[1]/input[@class='courseId']/@value"),
                                class_id=xpath_first(item, "./div[1]/input[@class='clazzId']/@value"),
                                url=tmp_url,
                                course_name=xpath_first(item, "./div[2]/h3/a/span/@title"),
                                course_author=xpath_first(item, "./div[2]/p[@class='line2 color3']/@title"),
                                headers=self._headers,
                                ifOpen=(xpath_first(item, "./div[1]/a[@class='not-open-tip']") == ""))
                self.courses.append(course)


user = User(phone="18960973410", password="XUsl142536897")
user.sign()