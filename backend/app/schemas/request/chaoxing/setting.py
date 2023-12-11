from typing import Annotated
from pydantic import BaseModel, Field


class ChaoxingSettingIn(BaseModel):
    work: Annotated[dict, Field(title="work setting")]
    exam: Annotated[dict, Field(title="work setting")]
    task: Annotated[dict, Field(title="work setting")]
    sign: Annotated[dict, Field(title="work setting")]
    searcher: Annotated[dict, Field(title="work setting")]
