from typing import Dict
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import crud
from app.api.deps import get_db
from app.core.config import settings
from app.db.base_class import Base
from app.db.init_db import init_db
from app.main import app
from app.models import Account
from app.models import Customer
from app.models import History
from app.tests.utils.utils import get_employee_token_headers

engine = create_engine(settings.TEST_DATABASE_URI, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db() -> Generator:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def client(db) -> Generator:
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    init_db(db)

    yield TestClient(app)


@pytest.fixture(scope="function")
def employee_token_headers(client: TestClient) -> Dict[str, str]:
    return get_employee_token_headers(client)


@pytest.fixture(scope="function")
def customer_1(db) -> Customer:
    yield crud.customer.create(db, obj_in={"full_name": "Pascal Niki"})


@pytest.fixture(scope="function")
def account_1_1(db, customer_1) -> Account:
    yield crud.account.create(db, obj_in={"customer_id": customer_1.id, "balance": 100})


@pytest.fixture(scope="function")
def customer_2(db) -> Customer:
    yield crud.customer.create(db, obj_in={"full_name": "John Doe"})


@pytest.fixture(scope="function")
def account_2_1(db, customer_2) -> Account:
    yield crud.account.create(db, obj_in={"customer_id": customer_2.id, "balance": 200})


@pytest.fixture(scope="function")
def account_2_2(db, customer_2) -> Account:
    yield crud.account.create(db, obj_in={"customer_id": customer_2.id, "balance": 0})


@pytest.fixture(scope="function")
def history(
    client, employee_token_headers, account_1_1, account_2_1, account_2_2, db
) -> int:
    transaction_data = {
        "from_account_id": account_1_1.id,
        "to_account_id": account_2_1.id,
        "amount": 100,
    }
    client.post(
        f"{settings.API_V1_STR}/transaction/",
        json=transaction_data,
        headers=employee_token_headers,
    )

    transaction_data = {
        "from_account_id": account_2_1.id,
        "to_account_id": account_2_2.id,
        "amount": 100,
    }
    client.post(
        f"{settings.API_V1_STR}/transaction/",
        json=transaction_data,
        headers=employee_token_headers,
    )

    transaction_data = {
        "from_account_id": account_2_2.id,
        "to_account_id": account_1_1.id,
        "amount": 100,
    }
    client.post(
        f"{settings.API_V1_STR}/transaction/",
        json=transaction_data,
        headers=employee_token_headers,
    )

    yield 3
    db.query(History).delete()
