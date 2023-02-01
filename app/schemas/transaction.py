from decimal import Decimal

from pydantic import BaseModel
from pydantic import Field


class Transaction(BaseModel):
    from_account_id: int
    to_account_id: int

    amount: Decimal = Field(gt=0, decimal_places=2, example=0.01, default=0.01)
