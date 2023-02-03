from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi_pagination import LimitOffsetPage
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.api import deps

router = APIRouter()


@router.post("/")
def create_new_customer(
    customer: schemas.InCustomer, db: Session = Depends(deps.get_db)
) -> schemas.CustomerOut:
    new_customer = crud.customer.create(db, obj_in=customer)

    return new_customer


@router.get("/all")
def get_all_customers(
    db: Session = Depends(deps.get_db),
) -> LimitOffsetPage[schemas.CustomerOut]:
    customers = crud.customer.get_multi(db)

    return customers


@router.get("/{customer_id}", responses=crud.customer.not_found_resp)
def get_particular_customer(
    customer_id: int = Path(ge=0), db: Session = Depends(deps.get_db)
) -> schemas.CustomerOut:
    customer = crud.customer.get(db, customer_id)

    return customer


@router.put("/{customer_id}", responses=crud.customer.not_found_resp)
def update_customer(
    customer: schemas.InCustomer,
    customer_id: int = Path(ge=0),
    db: Session = Depends(deps.get_db),
) -> schemas.CustomerOut:
    old_customer = crud.customer.get(db, customer_id)

    new_customer = crud.customer.update(db, db_obj=old_customer, obj_in=customer)

    return new_customer
