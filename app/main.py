from fastapi import FastAPI
from fastapi_pagination import add_pagination
from sqlalchemy.exc import OperationalError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.api_v1.api_router import api_router
from app.core.config import settings
from app.db.init_db import init

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Basic HTTP API for imaginary bank",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="v1",
    on_startup=[init],
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
add_pagination(app)


@app.exception_handler(OperationalError)
def db_exception_handler(request, exc):
    return JSONResponse(
        status_code=423,
        content={"detail": "Try again later."},
    )
