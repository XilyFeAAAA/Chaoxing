#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import time
import json
import pyDes
import aiohttp
import binascii
from http import HTTPStatus
from fastapi import HTTPException
from dataclasses import dataclass
from lxml.etree import _ElementUnicodeResult
# local
from app.common import constants
from app.schemas.request import AccountIn


@dataclass
class Chaoxing_User:
    phone: str
    username: str
    uid: str
    cookie: str


async def get_cookie(account_info: AccountIn) -> Chaoxing_User:
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
        async with session.post(constants.API_LOGIN, data=data) as response:
            if response.status == HTTPStatus.OK.value:
                res_json = json.loads(await response.text())
                if res_json.get("status"):
                    username = res_json.get("name")
                    uid = response.cookies["_uid"].value
                    cookie = ""
                    for name in response.cookies.keys():
                        cookie = cookie + name + '=' + response.cookies[name].value + ';'
                    return Chaoxing_User(account_info.phone, username, uid, cookie)
                else:
                    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail=res_json.get("msg2"))
            else:
                raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail="error_request")


async def check_cookie(cookie: str) -> bool:
    check_url = constants.API_CHECK + str(time.time())
    check_headers = {
        'Refer': constants.API_CHECK_REFER + str(time.time()),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
        "Cookie": cookie
    }
    async with aiohttp.ClientSession(headers=check_headers, ) as session:
        async with session.get(check_url, allow_redirects=False) as response:
            return response.status == HTTPStatus.OK.value



def encrypt_des(msg: str, key: str) -> bytes:
    des_obj = pyDes.des(key, key, pad=None, padmode=pyDes.PAD_PKCS5)
    secret_bytes = des_obj.encrypt(msg, padmode=pyDes.PAD_PKCS5)
    return binascii.b2a_hex(secret_bytes)


def xpath_first(element, path):
    """
    返回xpath获取到的第一个元素，如果没有则返回空字符串
    由于 lxml.etree._Element._Element 为私有类，所以不予设置返回值类型

    :param element: etree.HTML实例
    :param path: xpath路径
    :return: 第一个元素或空字符串
    """
    if type(element) in (str, int):
        return element
    res = element.xpath(path)
    if type(res) == _ElementUnicodeResult:
        return res
    if len(res) == 1:
        return res[0]
    else:
        return ""
