from typing import Generator
from typing import Optional

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
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db_serialized() -> Generator:
    db = SessionLocal()
    default_isolation = db.connection().default_isolation_level

    # throws exception OperationalError on concurrent update
    db.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;")
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
        # throws exception OperationalError on concurrent update
        db.execute(f"SET TRANSACTION ISOLATION LEVEL {default_isolation};")


def get_current_employee(
    db: Session = Depends(get_db),
    token_data: schemas.TokenPayload = Depends(JWTBearer()),
) -> Optional[models.Employee]:
    employee = crud.employee.get(db, id=token_data.sub)

    return employee
