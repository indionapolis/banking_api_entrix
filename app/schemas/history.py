from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from pydantic import Field


class HistoryOut(BaseModel):
    amount: Decimal = Field(gt=0, decimal_places=2, example=0.01)

    from_account_id: int

    to_account_id: int

    timestamp: datetime

    class Config:
        orm_mode = True
