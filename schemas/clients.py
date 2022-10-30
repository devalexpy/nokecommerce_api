from pydantic import (
    BaseModel, Field, EmailStr,
)
from typing import Optional


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
    phone_number: Optional[str] = Field(None)


class ClientSingUp(ClientBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
    )


class ClientForQuery(ClientBase):
    password: str = Field(...)
    id: str = Field(...)


class ClientOut(ClientBase):
    access_token: str = Field(...)
    token_type: str = Field(...)


class ClientUpdate(BaseModel):
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
    )
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=20,
    )
    last_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=20,
    )
    email: Optional[str] = EmailStr(None)
    phone_number: Optional[str] = Field(None)


class ClientUpdatePassword(BaseModel):
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
    )
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=20,
    )
