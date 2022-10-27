from pydantic import BaseModel, UUID4, Field
from uuid import UUID


class InvoiceRelation(BaseModel):
    id: UUID4 = Field(default_factory=UUID4)
