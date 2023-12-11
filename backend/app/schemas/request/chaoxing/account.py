from typing import Annotated
from pydantic import BaseModel, Field

phone_field = Field(title="phone number ", pattern='^1[3456789]\d{9}$')
password_field = Field(title="password")
account_id_field = Field(title="account_id")


class AccountIn(BaseModel):
    phone: Annotated[str, phone_field]
    password: Annotated[str, password_field]


class AccountRefreshIn(BaseModel):
    account_id: Annotated[str, account_id_field]
    password: Annotated[str, password_field]
