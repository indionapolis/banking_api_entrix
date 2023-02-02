import pytest
from fastapi.testclient import TestClient

from app.core.config import settings


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "email": settings.FIRST_EMPLOYEE,
        "password": settings.FIRST_EMPLOYEE_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/employee/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_incorrect_creds(client: TestClient) -> None:
    login_data = {
        "email": "test@mail.com",
        "password": "123",
    }
    r = client.post(f"{settings.API_V1_STR}/employee/access-token", data=login_data)

    assert r.status_code == 400


@pytest.mark.parametrize(
    "token_sub,status_code", [(None, 200), ({"Authorization": "Bearer 123"}, 403)]
)
def test_post_token(
    client: TestClient, employee_token_headers, token_sub, status_code
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/employee/test-token",
        headers=token_sub or employee_token_headers,
    )

    assert r.status_code == status_code
