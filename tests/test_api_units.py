import time
import uuid
from datetime import datetime
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# 1. Тест для эндпоинта /latest
@patch("routes.price_routes.get_latest_price_service")
def test_get_latest_price_unit(mock_get_latest):
    mock_get_latest.return_value = {
        "id": uuid.uuid4(),
        "ticker": "btc",
        "price": 65000.5,
        "timestamp": time.time(),
    }

    response = client.get("/prices/latest?ticker=btc")

    assert response.status_code == 200
    assert response.json()["ticker"] == "btc"
    assert response.json()["price"] == 65000.5
    mock_get_latest.assert_called_once_with("btc")


# 2. Тест для эндпоинта /history
@patch("routes.price_routes.get_prices_by_date_service")
def test_get_history_unit(mock_get_history):
    mock_get_history.return_value = [
        {
            "id": uuid.uuid4(),
            "ticker": "btc",
            "price": 60000.1,
            "timestamp": time.time(),
        },
        {
            "id": uuid.uuid4(),
            "ticker": "btc",
            "price": 61000.1,
            "timestamp": time.time(),
        },
    ]

    params = {
        "ticker": "btc",
        "start_ts": int(time.time() - 3600),
        "end_ts": int(time.time()),
    }
    response = client.get("/prices/history", params=params)

    assert response.status_code == 200
    assert len(response.json()) == 2
    mock_get_history.assert_called_once()


# 3. Тест на ошибку (например, тикер не найден)
@patch("routes.price_routes.get_latest_price_service")
def test_get_latest_not_found(mock_get_latest):
    mock_get_latest.side_effect = HTTPException(
        status_code=404, detail="No prices inside the database"
    )

    response = client.get("/prices/latest?ticker=btc")

    assert response.status_code == 404
    assert response.json()["detail"] == "No prices inside the database"


@patch("routes.price_routes.get_all_prices_service")
def test_get_all_by_ticker_unit(mock_get_all):
    mock_get_all.return_value = [
        {
            "id": uuid.uuid4(),
            "ticker": "btc",
            "price": 60000.0,
            "timestamp": datetime(2026, 3, 1, 10, 0).timestamp(),
        },
        {
            "id": uuid.uuid4(),
            "ticker": "btc",
            "price": 60500.0,
            "timestamp": datetime(2026, 3, 1, 10, 1).timestamp(),
        },
        {
            "id": uuid.uuid4(),
            "ticker": "btc",
            "price": 61000.0,
            "timestamp": datetime(2026, 3, 1, 10, 2).timestamp(),
        },
    ]

    response = client.get("/prices/all?ticker=btc")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3
    assert response.json()[0]["ticker"] == "btc"

    mock_get_all.assert_called_once_with("btc")
