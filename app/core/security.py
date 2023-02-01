from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Optional
from typing import Union

from fastapi import HTTPException
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from jose import jwt
from passlib.context import CryptContext

from app import schemas
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class JWTBearer(HTTPBearer):
    """
    sdfsdf
    """

    responses = {
        403: {
            "description": "Authentication error",
            "content": {"application/json": {"example": {"detail": "<reason>"}}},
        }
    }

    def __init__(self, auto_error: bool = True):
        """
        keke
        :param auto_error:
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> schemas.TokenPayload:
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            token_data = self.decode_jwt(credentials.credentials)
            if token_data is None:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return token_data
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def decode_jwt(token: str) -> Optional[schemas.TokenPayload]:

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            token_data = schemas.TokenPayload(**payload)
        except Exception:
            token_data = None

        return token_data
