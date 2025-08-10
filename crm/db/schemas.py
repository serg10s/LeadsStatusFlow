from pydantic import BaseModel, Field, EmailStr, ConfigDict


class CreateLead(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: EmailStr
    phone: str = Field(max_length=30)
    ip: str
    landing_url: str | None = Field(max_length=40)
    password: str | None = Field(max_length=200)

    model_config = ConfigDict(extra='forbid')


class CreateAdmin(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: EmailStr
    password: str

    model_config = ConfigDict(extra='forbid')
