#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import asyncio
import hashlib
import json
import time
import aiohttp
# local
from app.common import constants


class Media:

    def __init__(self, attachment: dict, headers: dict, defaults: dict, name: str, dtype: str = "Video"):
        self.headers = headers
        self.defaults = defaults
        self.attachment = attachment
        self.dtype = dtype
        self.object_id = attachment.get("objectId")
        self.report_url = defaults.get("reportUrl")
        self.rt = attachment.get("property").get("rt") or 0.9
        self.job_id = attachment.get("jobid")
        self.name = name

    async def get_status(self) -> dict | None:
        status_url = constants.API_MISSION_STATUS.format(self.object_id)
        mission_headers = {
            "Referer": constants.API_MISSION_REFERER
        }
        mission_headers.update(self.headers)
        async with aiohttp.ClientSession(headers=mission_headers) as session:
            async with session.get(status_url) as response:
                html = await response.text()
        try:
            status_json = json.loads(html)
            return status_json
        except Exception as e:
            print(e)
            return

    async def get_url(self, time_end: int, duration: int, dtoken: str, play_type: int) -> str:
        enc_raw = "[{0}][{1}][{2}][{3}][{4}][{5}][{6}][0_{7}]". \
            format(self.defaults.get("clazzId"), self.defaults.get("userid"), self.job_id, self.object_id, int(time_end) * 1000, "d_yHJ!$pdA~5",
                   duration * 1000,
                   duration)
        enc = hashlib.md5(enc_raw.encode()).hexdigest()
        url_former = self.report_url
        url_later = f"/{dtoken}?clazzId={self.defaults.get('clazzId')}" \
                    f"&playingTime={time_end}" \
                    f"&duration={duration}" \
                    f"&clipTime=0_{duration}" \
                    f"&objectId={self.object_id}" \
                    f"&otherInfo={self.attachment.get('otherInfo')}" \
                    f"&courseId={self.defaults.get('courseid')}" \
                    f"&jobid={self.job_id}" \
                    f"&userid={self.defaults.get('userid')}" \
                    f"&isdrag={play_type}" \
                    f"&view=pc" \
                    f"&enc={enc}" \
                    f"&rt={self.rt}" \
                    f"&dtype={self.dtype}" \
                    f"&_t={int(time.time() * 1000)}"
        return url_former + url_later

    async def run(self) -> bool:
        video_status = await self.get_status()
        if video_status:
            duration = video_status.get('duration')
            dtoken = video_status.get('dtoken')
            _url = await self.get_url(duration, duration, dtoken, 4)
            _headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Sec-Fetch-Dest': 'empty',
                'Host': 'mooc1.chaoxing.com',
                'Referer': 'https://mooc1.chaoxing.com/ananas/modules/video/index.html?v=2023-1117-1610',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
            }
            _headers.update(self.headers)
            async with aiohttp.ClientSession(headers=_headers) as session:
                async with session.get(_url) as response:
                    html = await response.text()
            if json.loads(html).get("isPassed"):
                return True
            else:
                return await self.run_duration()
        return False

    async def run_duration(self) -> bool:
        video_status: dict = await self.get_status()
        if video_status:
            duration = video_status.get('duration')
            dtoken = video_status.get('dtoken')
            _headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Sec-Fetch-Dest': 'empty',
                'Host': 'mooc1.chaoxing.com',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Referer': 'https://mooc1.chaoxing.com/ananas/modules/video/index.html?v=2023-0519-2354'
            }
            _headers.update(self.headers)
            _url = await self.get_url(0, duration, dtoken, 3)
            async with aiohttp.ClientSession(headers=_headers) as session:
                async with session.get(_url) as response:
                    html = await response.text()
                time_all = round(duration / 60, 2)
                time_m = duration // 60
                time_s = duration - time_m * 60
                for i in range(time_m):
                    await asyncio.sleep(59.8)
                    _url = await self.get_url(i * 60 + 59, duration, dtoken, 0)
                    async with session.get(_url) as response:
                        html = await response.text()
                    # 如果过程中返回通过直接结束
                    if json.loads(html).get("isPassed"):
                        return True
                if time_s:
                    await asyncio.sleep(time_s)
                    _url = await self.get_url(duration, duration, dtoken, 4)
                    async with session.get(_url) as response:
                        html = await response.text()
                return json.loads(html).get("isPassed")
        else:
            return False


