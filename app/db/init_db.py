from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app.core.config import settings
from app.db import base  # noqa: F401


def init_db(db: Session) -> None:
    employee = crud.employee.get_by_email(db, email=settings.FIRST_EMPLOYEE)
    if not employee:
        employee_in = schemas.EmployeeCreate(
            email=settings.FIRST_EMPLOYEE,
            password=settings.FIRST_EMPLOYEE_PASSWORD,
            is_superuser=True,
        )
        employee = crud.employee.create(db, obj_in=employee_in)  # noqa: F841
