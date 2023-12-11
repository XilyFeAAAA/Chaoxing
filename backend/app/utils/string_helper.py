#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import string
import random
from app.core.config import settings


def url_to_resource(url: str) -> str:
    res = url.removeprefix(settings.API_V1_STR)
    res = res[1:].replace("/", ":")
    return res


def generate_random_string(length) -> str:
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string