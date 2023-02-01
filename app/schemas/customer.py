from pydantic import BaseModel

from app.schemas.base import IDBase


class Customer(BaseModel):
    full_name: str


class CustomerOut(Customer, IDBase):
    class Config:
        orm_mode = True
