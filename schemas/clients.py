from pydantic import (
    BaseModel, Field, EmailStr,
)
from typing import List
from schemas.addresses import AddressesRelation
from schemas.invoices import InvoiceRelation


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


class clientOut(ClientBase):
    addresses: List[AddressesRelation] = []
    invoices: List[InvoiceRelation] = []

    class Config:
        orm_mode = True
