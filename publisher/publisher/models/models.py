from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    profile_id: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state: str
    zip: str

class Name(BaseModel):
    profile_id: str
    first_name: str
    last_name: str
