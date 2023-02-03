from decimal import Decimal

from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator


class Transaction(BaseModel):
    from_account_id: int
    to_account_id: int

    amount: Decimal = Field(gt=0, decimal_places=2, example=0.01, default=Decimal(0.01))

    @root_validator(pre=True)
    def check_self_transaction(cls, v):
        assert (
            v["from_account_id"] != v["to_account_id"]
        ), "Can't transfer within same account"
        return v
