#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import time
import json
import aiohttp
from lxml import etree
from http import HTTPStatus
from fastapi import HTTPException
# local
from .utils import *
from .schemas import *
from app.common import constants
from app.schemas.request import AccountIn


async def pwd_login(account_info: AccountIn) -> str:
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
    encrypt_pwd = encrypt_des(account_info.password, "u2oh6Vu^").decode('utf-8')
    data = f"fid=314&uname={account_info.phone}&password={encrypt_pwd}&refer=http%253A%252F%252Fi.mooc.chaoxing.com&t=true"
    async with aiohttp.ClientSession(headers=login_headers) as session:
        async with session.post(constants.API_LOGIN_FANYA, data=data) as response:
            if response.status == HTTPStatus.OK.value:
                res_json = json.loads(await response.text())
                if res_json.get("status"):
                    cookie = ""
                    for name in response.cookies.keys():
                        cookie = cookie + name + '=' + response.cookies[name].value + ';'
                    return cookie
                else:
                    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail=res_json.get("msg2"))
            else:
                raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail="后台请求错误")


async def get_qrcode() -> Chaoxing_Qrcode:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(constants.API_LOGIN) as response:
            html = await response.text()
        ele_root = etree.HTML(html)
        qrcode = Chaoxing_Qrcode(uuid=xpath_first(ele_root, "//input[@id='uuid']/@value"),
                                 enc=xpath_first(ele_root, "//input[@id='enc']/@value"))
        # 激活qrcode
        response = await session.get(constants.API_QRCREATE+f'?uuid={qrcode.uuid}&fid=-1')
        response.raise_for_status()
    return qrcode


async def qrcode_login(qrcode: Chaoxing_Qrcode) -> (dict, str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(constants.API_QRLOGIN, data=qrcode.__dict__) as response:
            html = await response.text()
            if response.status == HTTPStatus.OK.value:
                res_json = json.loads(html)
                if res_json.get("status"):
                    cookie = ""
                    for name in response.cookies.keys():
                        cookie = cookie + name + '=' + response.cookies[name].value + ';'
                    return res_json, cookie
            else:
                raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail="后台请求错误")


async def check_cookie(cookie: str) -> bool:
    check_url = constants.API_CHECK + str(time.time())
    check_headers = {
        'Refer': constants.API_CHECK_REFER + str(time.time()),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        "Cookie": cookie
    }
    async with aiohttp.ClientSession(headers=check_headers) as session:
        async with session.get(check_url, allow_redirects=False) as response:
            return response.status == HTTPStatus.OK.value


async def get_account_info(cookie: str) -> Chaoxing_User:
    """get info of chaoxing account"""
    check_url = constants.API_ACCOUNT
    check_headers = {
        'Refer': constants.API_CHAOXING,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        "Cookie": cookie
    }
    async with aiohttp.ClientSession(headers=check_headers) as session:
        async with session.get(check_url) as response:
            html = await response.text()
    resp_json = json.loads(html)
    print(resp_json)
    return Chaoxing_User(
        cookie=cookie,
        uid=str(resp_json['msg'].get("uid")),
        username=resp_json['msg'].get("name"),
        phone=resp_json['msg'].get("phone"),
        department=resp_json['msg'].get("schoolname")
    )



async def get_courses(cookie: str) -> list[Chaoxing_Course]:
    courses = []
    course_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        "Cookie": cookie
    }
    async with aiohttp.ClientSession(headers=course_headers) as session:
        async with session.get(constants.API_COURSE) as response:
            html = await response.text()
            ele = etree.HTML(html)
            course_ele = ele.xpath("//ul[@id='courseList']/li")
            for item in course_ele:
                tmp_url = xpath_first(item, "./div[2]/h3/a/@href")
                if tmp_url.startswith("http"):
                    start_time_str = xpath_first(item, "./div[2]/p[contains(text(), '开课时间')]/text()")
                    course = Chaoxing_Course(course_id=xpath_first(item, "./div[1]/input[@class='courseId']/@value"),
                                             class_id=xpath_first(item, "./div[1]/input[@class='clazzId']/@value"),
                                             url=tmp_url,
                                             classroom=xpath_first(item, "./div[2]/p[@class='overHidden1']/text()").replace("班级：", ""),
                                             start_time=start_time_str.split("开课时间：")[1] if start_time_str else "",
                                             img_url=xpath_first(item, "./div[1]/a/img/@src"),
                                             course_name=xpath_first(item, "./div[2]/h3/a/span/@title"),
                                             course_teacher=xpath_first(item, "./div[2]/p[@class='line2 color3']/@title"),
                                             is_open=(xpath_first(item, "./div[1]/a[@class='not-open-tip']") == ""))
                    courses.append(course)
    return courses

__all__ = ['get_courses', 'get_account_info', 'check_cookie', 'pwd_login', 'qrcode_login', 'get_qrcode']