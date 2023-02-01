from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr


class EmployeeBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    email: EmailStr
    password: str


class EmployeeInDBBase(EmployeeBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Employee(EmployeeInDBBase):
    pass
