from pydantic import BaseModel
from pydantic import Field

from app.schemas.base import IDBase


class InCustomer(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=100)


class CustomerOut(InCustomer, IDBase):
    class Config:
        orm_mode = True
