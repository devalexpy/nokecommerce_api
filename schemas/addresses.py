from pydantic import BaseModel, UUID4, Field
from uuid import UUID
from typing import List


class AddressBase(BaseModel):
    address: str = Field(...)


class AddressOut(AddressBase):
    is_default: bool = Field(...)
    id: UUID4 = Field(...)


class AddressesOut(BaseModel):
    addresses: List[AddressOut] = Field(...)


class AddressUpdate(BaseModel):
    new_address: str = Field(...)
