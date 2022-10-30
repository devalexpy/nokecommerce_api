from pydantic import BaseModel, Field


class AdminBase(BaseModel):
    name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    phone_number: str = Field(...)
    company_name: str = Field(...)


class AdminOut(AdminBase):
    access_token: str = Field(...)
    token_type: str = Field(...)


class AdminForQuery(AdminBase):
    id: int = Field(...)
    password: str = Field(...)
