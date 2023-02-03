from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi_pagination import LimitOffsetPage
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.api import deps

router = APIRouter()


@router.post("/", responses=crud.customer.not_found_resp)
def create_new_account(
    account: schemas.InAccount, db: Session = Depends(deps.get_db)
) -> schemas.AccountOut:
    crud.customer.get(db, account.customer_id)
    new_account = crud.account.create(db, obj_in=account)

    return new_account


@router.get("/all")
def get_all_accounts(
    db: Session = Depends(deps.get_db),
) -> LimitOffsetPage[schemas.AccountOut]:
    account = crud.account.get_multi(db)

    return account


@router.get("/{account_id}", responses=crud.account.not_found_resp)
def get_particular_account(
    account_id: int = Path(ge=0), db: Session = Depends(deps.get_db)
) -> schemas.AccountOut:
    account = crud.account.get(db, account_id)

    return account
