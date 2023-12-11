#! /usr/bin/env python
# -*- coding: utf-8 -*-#-

import pyDes
import qrcode
import binascii
from io import BytesIO
from qrcode.image.base import BaseImage
from qrcode.image.pil import PilImage
from qrcode.image.pure import PyPNGImage
from yarl import URL
from lxml.etree import _ElementUnicodeResult
# local
from app.common import constants
from .schemas import Chaoxing_Qrcode, Chaoxing_Question, Search_Response


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


def get_qrcode_img(qrcode_info: Chaoxing_Qrcode) -> BaseImage | PilImage | PyPNGImage:
    url = str(URL(constants.URL_QRLOGIN).with_query(
        uuid=qrcode_info.uuid,
        enc=qrcode_info.enc,
        xxtrefer="",
        clientid="",
        mobiletip=""
    ))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    # 创建字节流
    byte_stream = BytesIO()
    qr.make_image(fill_color="black", back_color="white").save(byte_stream, format='PNG')
    # 获取字节流的内容
    byte_stream.seek(0)
    return byte_stream.read()


id_dict = {
    "单选题": '0',
    "多选题": '1',
    "填空题": '2',
    "判断题": '3',
    "简答题": '4',
    "论述题": '6'
}


def transform_question(data: dict, questions: list[Chaoxing_Question]) -> dict:
    for question in questions:
        key_one = f"answertype{question.id}"
        data[key_one] = id_dict.get(question.type)
        if question.type == '填空题':
            key_two = f"tiankongsize{question.id}"
            data[key_two] = len(question.options)
            for index in range(len(question.options)):
                _key = f"answerEditor{question.id}{str(index)}"
                if question.answer is None:
                    data[_key] = ""
                else:
                    data[_key] = f"<p>{question.answer[index]}<br/></p>"
        elif question.type == '简答题':
            key_two = f"answer{question.id}"
            data[key_two] = f"<p>{question.answer or ''}</p>"
        else:
            key_two = f"answer{question.id}"
            data[key_two] = question.answer or ""
    return data


def parser(search: Search_Response) -> str | list[str]:
    """解析search的ans, 返回提交的答案"""
    match search.question.type:
        case "单选题":
            for option, answer in search.question.options.items():
                if answer == search.ans:
                    return option
        case "多选题":
            answer_str = ""
            for option, answer in search.question.options.items():
                if answer in search.ans:
                    answer_str += option
            return answer_str
        case "填空题" | "判断题":
            return search.ans


def all_question_id(questions: list[Chaoxing_Question]) -> str:
    ids = ""
    for question in questions:
        ids += question.id + ','
    return ids



__all__ = ['encrypt_des', 'xpath_first', 'get_qrcode_img', 'transform_question', 'parser', 'all_question_id']

