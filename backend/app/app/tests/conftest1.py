import os
from typing import Generator

import motor
import pytest
from aiokafka import AIOKafkaProducer
from app.db.redis import RedisDataBase

from app.models.kline import KLine
from app.models import EventLog
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

    db = get_mongodb()
    db["insight_test"]["person"].delete_one({"username": test_user["user"]["username"]})


def get_mongodb():
    mongoClient = motor.motor_asyncio.AsyncIOMotorClient("mongodb", 27017)
    return mongoClient


@pytest.fixture(scope="module")
def kline() -> KLine:
    return KLine()


@pytest.fixture(scope="function")
async def get_redis_client():
    import asyncio
    import aioredis

    redis = RedisDataBase()
    redis.client = await asyncio.wait_for(aioredis.create_redis_pool("redis://localhost:6379"), 3)
    return redis.client


# @pytest.fixture(scope="function")
# def test_init(monkeypatch):
#     def ok():
#         monkeypatch.chdir(os.path.abspath(os.path.dirname(__file__)))
#     # input_data = FileUtils.load_params_from_json(os.path.join(PATH, input_file))
#     # expected_data = FileUtils.load_params_from_json(os.path.join(PATH, expected_file))
#
#     # await CrudRedisGeneral.cleanup(get_redis_client, "*")
#     # await KLineService.init_kline(get_redis_client, [60, 3600, 86400])
#     return ok
