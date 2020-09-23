import json
from typing import Dict, Generator

import motor
import pytest
from aiokafka import AIOKafkaProducer
from app.core.config import settings
from app.models.kline import KLine
from app.models.orders import OrderCreate
from app.core.file_utils import FileUtils
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def kafka_producer() -> AIOKafkaProducer:
    import asyncio

    loop = asyncio.get_event_loop()
    producer = AIOKafkaProducer(
        loop=loop,
        client_id="eventer-01",
        bootstrap_servers="kafka://kafka:19092",
        api_version="2.0.1"
    )
    asyncio.wait_for(producer.start, 10)
    return producer


@pytest.fixture(scope="module")
def order_create() -> OrderCreate:
    return OrderCreate(
        order_id=1,
        market="ICX",
        price=90,
        size=17,
        user="asdasdas",
    )


@pytest.fixture(scope="session")
def test_user():
    return {
        "user": {
            "email": "user1@example.com",
            "password": "string1",
            "username": "string1"
        }
    }


@pytest.fixture(scope="session")
def test_client(test_user):
    from app.main import app
    with TestClient(app) as test_client:
        yield test_client

    db = get_database()
    db["insight_test"]["person"].delete_one({"username": test_user["user"]["username"]})


def get_database():
    mongoClient = motor.motor_asyncio.AsyncIOMotorClient("mongodb", 27017)
    return mongoClient


@pytest.fixture(scope="module", params=FileUtils.load_params_from_json('fixtures/test-data-input-kline_1.json'))
def input_from_test_data(request):
    a = request.param
    return request.param


@pytest.fixture(scope="module", params=FileUtils.load_params_from_json('fixtures/test-data-output-kline_1.json'))
def output_from_test_data(request):
    a = request.param
    return request.param


@pytest.fixture(scope="module")
def kline() -> KLine:
    return KLine()
