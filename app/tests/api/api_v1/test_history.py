from fastapi.testclient import TestClient

from app.core.config import settings


def test_get_history(client: TestClient, employee_token_headers, history):
    r = client.get(f"{settings.API_V1_STR}/history/", headers=employee_token_headers)
    history_data = r.json()

    assert r.status_code == 200
    assert history_data["total"] == history


def test_get_history_customer_1(
    client: TestClient, employee_token_headers, history, customer_1
):
    r = client.get(
        f"{settings.API_V1_STR}/history/customer/{customer_1.id}",
        headers=employee_token_headers,
    )
    history_data = r.json()

    assert r.status_code == 200
    assert history_data["total"] == 2


def test_get_history_customer_2(
    client: TestClient, employee_token_headers, history, customer_2
):
    r = client.get(
        f"{settings.API_V1_STR}/history/customer/{customer_2.id}",
        headers=employee_token_headers,
    )
    history_data = r.json()

    assert r.status_code == 200
    assert history_data["total"] == 3


def test_get_history_account_1_1(
    client: TestClient, employee_token_headers, history, account_1_1
):
    r = client.get(
        f"{settings.API_V1_STR}/history/account/{account_1_1.id}",
        headers=employee_token_headers,
    )
    history_data = r.json()

    assert r.status_code == 200
    assert history_data["total"] == 2


def test_get_history_account_2_1(
    client: TestClient, employee_token_headers, history, account_2_1
):
    r = client.get(
        f"{settings.API_V1_STR}/history/account/{account_2_1.id}",
        headers=employee_token_headers,
    )
    history_data = r.json()

    assert r.status_code == 200
    assert history_data["total"] == 2
