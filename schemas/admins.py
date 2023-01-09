from pydantic import BaseModel, Field


class AdminBase(BaseModel):
    name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    phone_number: str = Field(None)
    company_name: str = Field(...)


class AdminOut(AdminBase):
    access_token: str = Field(...)
    token_type: str = Field(...)


class AdminForQuery(AdminBase):
    id: str = Field(...)
    password: str = Field(...)
