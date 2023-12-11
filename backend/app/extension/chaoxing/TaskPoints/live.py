#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import json
import asyncio
import time
import aiohttp
from yarl import URL
# local
from app.common import constants


class Live:
    def __init__(self, attachment: dict, headers: dict, defaults: dict):
        self.headers = headers
        self.defaults = defaults
        self.attachment = attachment
        self.course_id = defaults.get("courseid")
        self.job_id = attachment.get("jobid")

    async def run(self) -> bool:
        status = await self.live_status()
        if status:
            duration = status.get("temp").get("data").get('duration')
            _dis = (duration + 59) // 60
            for i in range(int(_dis)):
                print(f"'当前刷取时长{i + 1}分钟,总时长{_dis}分钟")

                _url = str(URL(constants.URL_LIVE).with_query(
                    streamName=self.attachment.get("property").get("streamName"),
                    vdoid=self.attachment.get("property").get("vdoid"),
                    userId=self.defaults.get("userid"),
                    isStart=0,
                    courseId=self.course_id,
                    t=int(round(time.time() * 1000))
                ))
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(_url) as response:
                        html = await response.text()
                if html != "@success":
                    return False
                await asyncio.sleep(59)
            return True
        else:
            print("直播状态获取失败")
            return False

    async def live_status(self) -> dict | None:
        _url = str(URL(constants.URL_LIVE_STATUS).with_query(
            liveid=self.attachment.get('property').get('liveId'),
            userid=self.defaults.get('userid'),
            clazzid=self.defaults.get('clazzId'),
            knowledgeid=self.defaults.get('knowledgeid'),
            courseid=self.course_id,
            jobid=self.job_id,
            ut="s"
        ))
        _headers = {
            "Referer": "https://mooc1.chaoxing.com/ananas/modules/live/index.html?v=2022-1214-1139"
        }
        _headers.update(self.headers)
        async with aiohttp.ClientSession(headers=_headers) as session:
            async with session.get(_url) as response:
                html = await response.text()
        try:
            status_json = json.loads(html)
            return status_json
        except Exception as e:
            print(e)
            return
