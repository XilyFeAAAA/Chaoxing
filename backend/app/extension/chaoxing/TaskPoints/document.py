#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import json
import time
import aiohttp


class Document:
    def __init__(self, attachment: dict, headers: dict, defaults: dict):
        self.headers = headers
        self.defaults = defaults
        self.attachment = attachment
        self.course_id = defaults.get("courseid")
        self.job_id = attachment.get("jobid")

    async def run(self) -> bool:
        _headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Host': 'mooc1-2.chaoxing.com',
            'Referer': 'https://mooc1-2.chaoxing.com/ananas/modules/pdf/index.html?v=2020-1103-1706',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest'
        }
        _headers.update(self.headers)
        _url = "https://mooc1-2.chaoxing.com/ananas/job/document?" \
               f"jobid={self.job_id}" \
               f"&knowledgeid={self.defaults.get('knowledgeid')}" \
               f"&courseid={self.course_id}" \
               f"&clazzid={self.defaults.get('clazzId')}" \
               f"&jtoken={self.attachment.get('jtoken')}" \
               f"&_dc={int(time.time() * 1000)}"
        async with aiohttp.ClientSession(headers=_headers) as session:
            async with session.get(_url) as response:
                html = await response.text()
        return json.loads(html).get("status")

