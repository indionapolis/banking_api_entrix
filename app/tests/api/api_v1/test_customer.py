from fastapi.testclient import TestClient

from app import crud
from app.core.config import settings
from app.models import Customer


def test_create_customer(client: TestClient, employee_token_headers, db) -> None:
    customer = {"full_name": "Pavel Nikulin"}

    r = client.post(
        f"{settings.API_V1_STR}/customer/",
        json=customer,
        headers=employee_token_headers,
    )
    customer_data = r.json()

    assert r.status_code == 200
    assert customer_data["full_name"] == "Pavel Nikulin"
    assert crud.customer.get(db, customer_data["id"])


def test_get_customer(client: TestClient, employee_token_headers, db) -> None:
    customer = db.query(Customer).first()

    r = client.get(
        f"{settings.API_V1_STR}/customer/{customer.id}", headers=employee_token_headers
    )
    customer_data = r.json()

    assert r.status_code == 200
    assert customer_data["full_name"] == customer.full_name
    assert "id" in customer_data


def test_get_customer_404(client: TestClient, employee_token_headers) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/customer/{1000000}", headers=employee_token_headers
    )

    assert r.status_code == 404


def test_get_customer_all(client: TestClient, employee_token_headers, db) -> None:
    count = db.query(Customer).count()

    r = client.get(
        f"{settings.API_V1_STR}/customer/all/", headers=employee_token_headers
    )
    customer_data = r.json()

    assert r.status_code == 200
    assert customer_data["total"] == count


def test_update_customer(
    client: TestClient, employee_token_headers, db, customer_1
) -> None:
    new_data = {"full_name": "Pedro Pascal"}
    r = client.put(
        f"{settings.API_V1_STR}/customer/{customer_1.id}/",
        json=new_data,
        headers=employee_token_headers,
    )
    customer_data = r.json()

    assert r.status_code == 200
    assert new_data["full_name"] == customer_data["full_name"] == customer_1.full_name
    assert "id" in customer_data
