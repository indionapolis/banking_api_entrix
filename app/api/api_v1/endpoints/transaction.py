from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.api import deps
from app.models import Account
from app.models import History

router = APIRouter()


@router.post(
    "/",
    responses=crud.account.not_found_resp
    | {
        status.HTTP_200_OK: {
            "description": "Transaction completed",
            "content": {"application/json": {"example": {"msg": "success"}}},
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Insufficient funds for transfer",
            "content": {
                "application/json": {
                    "example": {"detail": "Insufficient funds for transfer"}
                }
            },
        },
    },
)
def make_new_transaction(
    transaction: schemas.Transaction, db: Session = Depends(deps.get_db)
) -> Any:
    from_account: Account = crud.account.get(db, transaction.from_account_id)
    to_account: Account = crud.account.get(db, transaction.to_account_id)

    if from_account.balance < transaction.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds for transfer",
        )

    before_sum = from_account.balance + to_account.balance

    from_account.balance -= transaction.amount
    to_account.balance += transaction.amount

    after_sum = from_account.balance + to_account.balance

    if before_sum != after_sum:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sum check mismatch",
        )

    history = History(
        amount=transaction.amount, from_account=from_account, to_account=to_account
    )

    db.add(history)
    db.add(from_account)
    db.add(to_account)
    db.commit()

    return {"msg": "success"}
