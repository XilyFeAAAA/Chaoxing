#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import string
import random
from captcha.image import ImageCaptcha
# local
from app.common import constants


def create_code() -> str:
    """create code for captcha"""
    characters = string.digits + string.ascii_letters
    return "".join(random.choices(characters, k=constants.CAPTCHA_LENGTH))


def generate_captcha(code: str) -> bytes:
    """generate captcha image"""
    image = ImageCaptcha(width=160, height=40, font_sizes=[30])
    return image.generate(code).getvalue()
