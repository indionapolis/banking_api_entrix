from pydantic import BaseModel

from app.schemas.base import IDBase


class InCustomer(BaseModel):
    full_name: str


class CustomerOut(InCustomer, IDBase):
    class Config:
        orm_mode = True
