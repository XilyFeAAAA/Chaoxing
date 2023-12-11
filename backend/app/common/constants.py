#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from pathlib import Path

BASE_FOLDER: Path = Path('app')
# docs
PROJECT_NAME: str = "ChaoXing"
VERSION: str = "1.0.0"
# celery
CELERY_BROKER_URL: str = "redis://localhost:6379"
CELERY_RESULT_BACKEND: str = "redis://localhost:6379"
# schema
USER_NICKNAME_MIN_LENGTH: int = 3
USER_NICKNAME_MAX_LENGTH: int = 10
USER_PASSWORD_MIN_LENGTH: int = 6
USER_PASSWORD_MAX_LENGTH: int = 20
# captcha
IGNORE_CASE: bool = True
CAPTCHA_LENGTH: int = 4
CAPTCHA_MIN_TIMEDELTA: int = 5
# auth
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 12
REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
# model
USER_ID_LENGTH: int = 12
ACCOUNT_ID_LENGTH: int = 12
ORDER_ID_LENGTH: int = 8
MESSAGE_ID_LENGTH: int = 8
# upload
SMALL_CHUNK_SIZE: int = 1024
TEMPFILE_FOLDER_PATH: Path = BASE_FOLDER / 'temps'
TEMPFILE_ID_LENGTH: int = 8
# api
API_LOGIN: str = "https://passport2.chaoxing.com/login"
API_QRCREATE: str = "https://passport2.chaoxing.com/createqr"
API_QRLOGIN: str = "https://passport2.chaoxing.com/getauthstatus"
API_LOGIN_FANYA: str = "https://passport2.chaoxing.com/fanyalogin"
API_CHECK: str = "https://i.chaoxing.com/base/settings?t="
API_CHECK_REFER: str = "https://i.chaoxing.com/base?t="
API_ACCOUNT: str = "https://sso.chaoxing.com/apis/login/userLogin4Uname.do"
API_CHAOXING: str = "https://i.chaoxing.com/"
API_COURSE: str = "https://mooc2-ans.chaoxing.com/mooc2-ans/visit/courses/list"
API_WORK: str = "https://mooc1.chaoxing.com/mooc-ans/api/work"
API_MISSION_STATUS: str = "https://mooc1-1.chaoxing.com/ananas/status/{}?k=&flag=normal&_dc=1600850935908"
API_MISSION_REFERER: str = "https://mooc1.chaoxing.com/ananas/modules/video/index.html?v=2022-0329-1945"
# url
URL_QRLOGIN: str = "https://passport2.chaoxing.com/toauthlogin"
URL_COMMIT_HOMEWORK: str = "https://mooc1.chaoxing.com/mooc-ans/work/addStudentWorkNewWeb"
URL_PRECOMMIT_HOMEWORK: str = "https://mooc1.chaoxing.com/mooc-ans/work/validate"
URL_LIVE_STATUS: str = "https://mooc1.chaoxing.com/ananas/live/liveinfo?liveid"
URL_LIVE: str = "https://zhibo.chaoxing.com/saveTimePc"
# others
COST_ONCE: float = 1
# token
ENNCY_TOKEN: str = "67b3fc8d603d4fc489af1037b968dc5e"
EVERY_TOKEN: str = "wKahq8krieBbZDbK"
HEIBOOK_TOKEN: str = "4099239fdfd8765e22720ee75ab7fdb3"
AIDIAN_TOKEN: str = "LOM9CwAV0BBnPRSKOIZt"
WANNENG_TOKEN: str = "92D34C44DF"
# question
CORRECT_THRESHOLD: float = 0.7
# http
HEADER_USERAGENT_PC: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51'
# tip
TIP_ADDUSER_WELCOME_TITLE: str = "欢迎注册!"
TIP_ADDUSER_WELCOME_MESSAGE: str = "感谢您选择加入我们的平台！在开始使用之前，我们强烈建议您阅读我们提供的帮助文档和配置设置。这些资源将帮助您更好地了解系统的各个方面，包括功能、界面操作和个性化设置。"
TIP_COURSEORDER_COMMIT_TITLE: str = "下单成功!"
TIP_COURSEORDER_COMMIT_MESSAGE: str = """感谢您选择我们的服务并下单成功！我们很高兴地通知您，您的订单已经成功生成。以下是您的订单详细信息：

订单号：{}
订单信息：{}

为了让您能够及时了解订单的进度和状态，请随时登录到我们的平台订单页面，其中包含有关您订单的最新信息。"""
TIP_COURSEORDER_FAIL_TITLE: str = "订单错误!"
TIP_COURSEORDER_FAIL_MESSAGE: str = """非常抱歉地通知您，出现了一些问题导致您的订单无法完成。我们深感抱歉给您带来不便。以下是有关您的订单的详细信息：

订单号：{}
订单信息：{}
具体原因: {}

我们发现在处理您的订单时遇到了一些错误或异常情况。为了解决这个问题，我们建议您采取以下步骤之一：
补单：请您前往订单页面,对发生问题的订单选择补单(多次补单可能导致学习通被锁定, 补单失败请联系管理员)。
联系管理员：如果您对订单发生的错误或问题感到困惑，或者需要进一步的帮助，请您联系我们的管理员团队"""
TIP_COURSEORDER_OVER_TITLE: str = "订单完成!"
TIP_COURSEORDER_OVER_MESSAGE: str = """您的订单已成功完成。以下是您的订单详细信息：

订单号：{}
订单信息：{}

请尽快登录学习通平台, 了解订单的完成情况和进展。如果您发现任何问题或需要补充相关信息，请及时补单或者联系我们的管理员团队。"""