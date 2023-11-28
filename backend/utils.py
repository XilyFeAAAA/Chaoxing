#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import binascii

import pyDes
from lxml.etree import _ElementUnicodeResult


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
