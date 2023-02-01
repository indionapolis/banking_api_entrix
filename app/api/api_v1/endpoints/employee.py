from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import JWTBearer
from app.schemas.employee import LoginForm

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token,
             responses={400: {"description": "Incorrect email or password", "content": {
                 "application/json": {
                     "example": {"detail": "Incorrect email or password"}
                 }}}})
def login_access_token(
        db: Session = Depends(deps.get_db), form_data: LoginForm = Depends()
) -> Any:
    """
    Bearer token login, get an access token for future requests
    """
    employee = crud.employee.authenticate(
        db, email=form_data.email, password=form_data.password
    )
    if not employee:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            employee.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


# https://testdriven.io/blog/fastapi-jwt-auth/

@router.post("/login/test-token", response_model=schemas.Employee, responses=JWTBearer.responses)
def test_token(current_employee: models.Employee = Depends(deps.get_current_employee)) -> Any:
    """
    Test access token, returns employee
    """
    return current_employee
