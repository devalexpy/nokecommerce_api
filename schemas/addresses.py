from pydantic import BaseModel, UUID4, Field
from uuid import UUID
from typing import Optional


class AddressesRelation(BaseModel):
    id: UUID4 = Field(default_factory=UUID4)


class AddressesBase(BaseModel):
    address: str = Field(...)
    is_default: Optional[bool] = Field(default=False)
