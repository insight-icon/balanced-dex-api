import pytest
from app.core.config import settings
from fastapi.testclient import TestClient
from typing import Dict, Generator
from app.main import app


def test_test1(
        input_value: int
) -> None:
    response = TestClient(app).get(f"{settings.API_V1_STR}/dex/")
    assert response.status_code == 200
    assert input_value == 39


def test_test(
        client: TestClient,
        input_value: int
) -> None:
    response = client.get(f"{settings.API_V1_STR}/dex/")
    assert response.status_code == 200
    assert input_value == 39