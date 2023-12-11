#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from pydantic import BaseModel
from datetime import datetime


class CourseOut(BaseModel):
    course_name: str
    course_id: str
    class_id: str
    url: str
    img_url: str
    is_open: bool
    course_teacher: str
    start_time: str
    classroom: str

    class Config:
        from_attributes = True
