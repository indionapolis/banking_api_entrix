from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr


class InEmployee(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class EmployeeCreate(InEmployee):
    email: EmailStr
    password: str


class EmployeeInDBBase(InEmployee):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Employee(EmployeeInDBBase):
    pass
