#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import time
import logging
from app.core.config import settings


class Log(object):
    def __init__(self, logger=None):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)
        self.log_time = time.strftime("%Y_%m_%d")
        if not settings.LOG_PATH.exists():
            settings.LOG_PATH.mkdir()
        self.log_path = settings.LOG_PATH / f"{self.log_time}.log"
        error_handler = logging.FileHandler(self.log_path.absolute())
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d %(message)s')
        error_handler.setFormatter(error_formatter)
        info_handler = logging.StreamHandler()
        info_handler.setLevel(logging.INFO)
        info_formatter = logging.Formatter(
            '[%(levelname)s][%(asctime)s]  %(message)s')
        info_handler.setFormatter(info_formatter)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(info_handler)
        error_handler.close()
        info_handler.close()

    def getlog(self):
        return self.logger


logger = Log().getlog()
