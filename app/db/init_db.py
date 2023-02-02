import logging

from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.core.config import settings
from app.db import base  # noqa: F401
from app.db.session import SessionLocal
from app.schemas import InCustomer

logger = logging.getLogger(__name__)

ini_customers = [
    {"id": 1, "name": "Arisha Barron"},
    {"id": 2, "name": "Branden Gibson"},
    {"id": 3, "name": "Rhonda Church"},
    {"id": 4, "name": "Georgina Hazel"},
]


def init_db(db: Session) -> None:
    employee = crud.employee.get_by_email(db, email=settings.FIRST_EMPLOYEE)
    if not employee:
        employee_in = schemas.EmployeeCreate(
            email=settings.FIRST_EMPLOYEE,
            password=settings.FIRST_EMPLOYEE_PASSWORD,
            full_name="Tom",
            is_superuser=True,
        )
        employee = crud.employee.create(db, obj_in=employee_in)  # noqa: F841

        for customer in ini_customers:
            crud.customer.create(db, obj_in=InCustomer(full_name=customer["name"]))

        logger.info("Database populated with initial data.")


def init() -> None:
    db = SessionLocal()
    init_db(db)
