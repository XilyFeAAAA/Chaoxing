from typing import Annotated
from pydantic import BaseModel, Field

course_id_field = Field(title="course_id")
do_homework_field = Field(title="do_homework")


class CourseOrderIn(BaseModel):
    course_id: Annotated[str, course_id_field]
    do_homework: Annotated[bool, do_homework_field]