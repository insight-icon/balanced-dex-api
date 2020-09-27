from typing import Generator

import motor
import pytest
from aiokafka import AIOKafkaProducer
from app.models.kline import KLine
from app.models.orders import EventLog
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
def order_create() -> EventLog:
    return EventLog(
        event="OrderRest",
        order_id=1,
        side=1,
        market="BALICD",
        price="0.0034",
        size="1.223",
        user="hxcd6f04b2a5184715ca89e523b6c823ceef2f9c3d",
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


@pytest.fixture(scope="module")
def kline() -> KLine:
    return KLine()



