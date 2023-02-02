from fastapi.testclient import TestClient

from app.core.config import settings


def test_post_transaction_two_customers(
    client: TestClient, employee_token_headers, db, account_1_1, account_2_1
) -> None:
    amount = 100
    account_balance_before = account_1_1.balance
    account2_balance_before = account_2_1.balance
    sum_before = account_1_1.balance + account_2_1.balance

    transaction_data = {
        "from_account_id": account_1_1.id,
        "to_account_id": account_2_1.id,
        "amount": amount,
    }
    r = client.post(
        f"{settings.API_V1_STR}/transaction/",
        json=transaction_data,
        headers=employee_token_headers,
    )
    result = r.json()

    sum_after = account_1_1.balance + account_2_1.balance
    account_balance_after = account_1_1.balance
    account2_balance_after = account_2_1.balance

    assert r.status_code == 200
    assert result["msg"] == "success"
    assert sum_after == sum_before
    assert account_balance_after == account_balance_before - amount
    assert account2_balance_after == account2_balance_before + amount


def test_post_transaction_one_customers(
    client: TestClient, employee_token_headers, db, account_2_1, account_2_2
) -> None:
    amount = 100
    account_balance_before = account_2_1.balance
    account2_balance_before = account_2_2.balance
    sum_before = account_2_1.balance + account_2_2.balance

    transaction_data = {
        "from_account_id": account_2_1.id,
        "to_account_id": account_2_2.id,
        "amount": amount,
    }
    r = client.post(
        f"{settings.API_V1_STR}/transaction/",
        json=transaction_data,
        headers=employee_token_headers,
    )
    result = r.json()

    sum_after = account_2_1.balance + account_2_2.balance
    account_balance_after = account_2_1.balance
    account2_balance_after = account_2_2.balance

    assert r.status_code == 200
    assert result["msg"] == "success"
    assert sum_after == sum_before
    assert account_balance_after == account_balance_before - amount
    assert account2_balance_after == account2_balance_before + amount


def test_post_transaction_two_customers_not_enough_money(
    client: TestClient, employee_token_headers, db, account_1_1, account_2_2
) -> None:
    transaction_data = {
        "from_account_id": account_2_2.id,
        "to_account_id": account_1_1.id,
        "amount": 100,
    }
    r = client.post(
        f"{settings.API_V1_STR}/transaction/",
        json=transaction_data,
        headers=employee_token_headers,
    )
    result = r.json()

    assert r.status_code == 400
    assert result["detail"] == "Insufficient funds for transfer"
