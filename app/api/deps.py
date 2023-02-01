from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app import crud
from app import models
from app import schemas
from app.core.security import JWTBearer
from app.db.session import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()


def get_current_employee(
    db: Session = Depends(get_db),
    token_data: schemas.TokenPayload = Depends(JWTBearer()),
) -> models.Employee:
    employee = crud.employee.get(db, id=token_data.sub)

    return employee
