from decimal import Decimal

from pydantic import BaseModel
from pydantic import Field

from app.schemas.base import IDBase


class InAccount(BaseModel):
    balance: Decimal = Field(
        ge=0, lt=10**8, decimal_places=2, example=0.01, default=Decimal(0.00)
    )
    customer_id: int


class AccountOut(InAccount, IDBase):
    class Config:
        orm_mode = True
