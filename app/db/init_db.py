from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    employee = crud.employee.get_by_email(db, email=settings.FIRST_EMPLOYEE)
    if not employee:
        employee_in = schemas.EmployeeCreate(
            email=settings.FIRST_EMPLOYEE,
            password=settings.FIRST_EMPLOYEE_PASSWORD,
            is_superuser=True,
        )
        employee = crud.employee.create(db, obj_in=employee_in)  # noqa: F841
