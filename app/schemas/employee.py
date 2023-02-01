from typing import Optional

from fastapi import Form
from pydantic import BaseModel, EmailStr


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


class LoginForm:
    """
    username: employee email string.
    password: password string.
    """

    def __init__(
            self,
            email: str = Form(..., description="employee email"),
            password: str = Form(..., description="employee password")
    ):
        self.email = email
        self.password = password
