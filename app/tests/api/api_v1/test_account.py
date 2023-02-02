import pytest
from fastapi.testclient import TestClient

from app import crud
from app.core.config import settings
from app.models import Account


def test_post_account(
    client: TestClient, employee_token_headers, db, customer_1
) -> None:
    new_account = {"customer_id": customer_1.id, "balance": 1000}

    r = client.post(
        f"{settings.API_V1_STR}/account/",
        json=new_account,
        headers=employee_token_headers,
    )
    account_data = r.json()

    account = crud.account.get(db, account_data["id"])

    assert r.status_code == 200
    assert account_data["balance"] == new_account["balance"] == account.balance
    assert account in customer_1.accounts


@pytest.mark.parametrize(
    "balance,status", [(100000000, 422), (-1, 422), (0, 200), (99999999, 200)]
)
def test_post_account_balance(
    client: TestClient, employee_token_headers, db, balance, status, customer_1
):
    new_account = {"customer_id": customer_1.id, "balance": balance}

    r = client.post(
        f"{settings.API_V1_STR}/account/",
        json=new_account,
        headers=employee_token_headers,
    )

    assert r.status_code == status


def test_get_account(
    client: TestClient, employee_token_headers, db, account_1_1
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/account/{account_1_1.id}/",
        headers=employee_token_headers,
    )
    account_data = r.json()

    assert r.status_code == 200
    assert account_data["balance"] == account_1_1.balance
    assert "id" in account_data


def test_get_account_404(client: TestClient, employee_token_headers) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/account/{-1}/", headers=employee_token_headers
    )

    assert r.status_code == 404


def test_get_account_all(client: TestClient, employee_token_headers, db) -> None:
    count = db.query(Account).count()

    r = client.get(
        f"{settings.API_V1_STR}/account/all/", headers=employee_token_headers
    )
    customer_data = r.json()

    assert r.status_code == 200
    assert customer_data["total"] == count
