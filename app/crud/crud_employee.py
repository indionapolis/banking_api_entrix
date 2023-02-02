from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.core.security import verify_password
from app.crud import CRUDBase
from app.models import Employee
from app.schemas import EmployeeCreate
from app.schemas import InEmployee


class CRUDEmployee(CRUDBase[Employee, EmployeeCreate, InEmployee]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.email == email).first()

    def create(self, db: Session, *, obj_in: EmployeeCreate) -> Employee:
        db_obj = Employee(
            full_name=obj_in.full_name,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[Employee]:
        employee = self.get_by_email(db, email=email)
        if not employee:
            return None
        if not verify_password(password, str(employee.hashed_password)):
            return None
        return employee


employee = CRUDEmployee(Employee)
