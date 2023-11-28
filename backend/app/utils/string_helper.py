#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from app.core.config import settings


def url_to_resource(url: str) -> str:
    res = url.removeprefix(settings.API_V1_STR)
    res = res[1:].replace("/", ":")
    return res
