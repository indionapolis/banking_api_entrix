from fastapi import APIRouter
from fastapi import Depends
from fastapi_pagination import LimitOffsetPage
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.api import deps

router = APIRouter()


@router.get("/")
def get_all_history(
    db: Session = Depends(deps.get_db),
) -> LimitOffsetPage[schemas.HistoryOut]:
    history = crud.history.get_multi(db)

    return history


@router.get("/customer/{customer_id}")
def get_customer_history(
    customer_id: int, db: Session = Depends(deps.get_db)
) -> LimitOffsetPage[schemas.HistoryOut]:
    return crud.history.filter_customer(db, customer_id)


@router.get("/account/{account_id}")
def get_account_history(
    account_id: int, db: Session = Depends(deps.get_db)
) -> LimitOffsetPage[schemas.HistoryOut]:
    return crud.history.filter_account(db, account_id)
