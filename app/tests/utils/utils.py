import random
import string
from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_employee_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "email": settings.FIRST_EMPLOYEE_EMAIL,
        "password": settings.FIRST_EMPLOYEE_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/employee/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
