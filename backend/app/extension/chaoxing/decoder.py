#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import base64
import pickle
import re
from hashlib import sha1, md5
from io import BytesIO

from fontTools.ttLib import TTFont

with open("app/extension/chaoxing/asset/font-1.pkl", "rb") as f:
    hashed = pickle.load(f)[0]

with open("app/extension/chaoxing/asset/font-2.pkl", "rb") as f:
    cmap = pickle.load(f)

hashed_dict = {j: i for i, j in hashed}
cmap = list(filter(lambda x: 0x4e00 <= x[0] <= 0x9fa5, cmap))
cmap = {j: i for i, j in cmap}


class Decoder:

    def __init__(self, html: str):
        self.html = html
        self.font: bytes = None
        self.table: dict = {}
        self.get_font()
        self.get_dict()

    def get_font(self) -> None:
        pattern = r"base64,([^']+)'"
        match = re.search(pattern, self.html)
        base64_string = match.group(1)
        self.font = base64.b64decode(base64_string)

    def get_dict(self) -> None:
        aa = TTFont(BytesIO(self.font))
        aa_glyphs = aa["glyf"].glyphs
        aa_cmap = aa.getBestCmap()
        aa_cmap = {j: i for i, j in zip(aa_cmap.keys(), aa_cmap.values())}
        for i, j in zip(aa_glyphs.keys(), aa_glyphs.values()):
            try:
                hashed = (sha1(j.data).digest(), md5(j.data).digest())
                self.table[chr(aa_cmap[i])] = chr(cmap[hashed_dict[hashed]])
            except KeyError:
                continue

    def translate(self, raw: str) -> str:
        return "".join([self.table.get(word, word) for word in raw])
