from fastapi import APIRouter
from fastapi import Depends

from app.api.api_v1.endpoints import account
from app.api.api_v1.endpoints import customer
from app.api.api_v1.endpoints import employee
from app.api.api_v1.endpoints import history
from app.api.api_v1.endpoints import transaction
from app.core.security import JWTBearer

api_router = APIRouter()

general_api_router = APIRouter()
secure_api_router = APIRouter()

general_api_router.include_router(
    employee.router, prefix="/employee", tags=["Employee"], dependencies=None
)

secure_api_router.include_router(customer.router, prefix="/customer", tags=["Customer"])
secure_api_router.include_router(account.router, prefix="/account", tags=["Account"])
secure_api_router.include_router(
    transaction.router, prefix="/transaction", tags=["Transaction"]
)
secure_api_router.include_router(history.router, prefix="/history", tags=["History"])

# add routers to central API gateway
api_router.include_router(general_api_router)
api_router.include_router(
    secure_api_router,
    dependencies=[Depends(JWTBearer())],
    responses=JWTBearer.responses,
)
