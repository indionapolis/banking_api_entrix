from datetime import timedelta
from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app import crud
from app import models
from app import schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import JWTBearer

router = APIRouter()


@router.post(
    "/access-token",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Incorrect email or password",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect email or password"}
                }
            },
        }
    },
)
def login_access_token(
    db: Session = Depends(deps.get_db),
    email: str = Form(..., description="employee email"),
    password: str = Form(..., description="employee password"),
) -> schemas.Token:
    """
    Bearer token login, get an access token for future requests
    """
    employee = crud.employee.authenticate(db, email=email, password=password)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        employee.id, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post(
    "/test-token",
    response_model=schemas.Employee,
    responses=JWTBearer.responses | crud.employee.not_found_resp,
)
def test_token(
    current_employee: models.Employee = Depends(deps.get_current_employee),
) -> Any:
    """
    Test access token, returns employee
    """
    return current_employee
