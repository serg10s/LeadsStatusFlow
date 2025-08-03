from pydantic import BaseModel


class CreateLead(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    ip: str
    landing_url: str
