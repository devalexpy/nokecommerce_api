from pydantic import (
    BaseModel, Field, EmailStr,
    UUID4
)
from typing import Optional
from uuid import UUID


class ClientBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=20,
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=20,
    )
    email: str = EmailStr(...)
    phone_number: str = Field(...)


class ClientSingUp(ClientBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
    )


class clientLogin(BaseModel):
    email: str = EmailStr(...)
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
    )
