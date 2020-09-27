from typing import Union

import asyncio

from aiokafka import AIOKafkaProducer
from aioredis import Redis
from app.core.config import settings
from app.db.redis import get_redis_database
from app.models.orders import EventLog, TradeLog
from app.services.trade_service import TradeService
from fastapi import APIRouter, Depends

router = APIRouter()
event_producer: AIOKafkaProducer = None


def init():
    global event_producer
    event_producer = get_kafka_producer()


def get_kafka_producer() -> AIOKafkaProducer:
    loop = asyncio.get_event_loop()
    producer = AIOKafkaProducer(
        loop=loop,
        client_id="event-producer",
        bootstrap_servers=settings.KAFKA_INTERNAL_HOST_PORT,
        api_version="2.0.1"
    )
    return producer


router.add_event_handler("startup", init)


@router.post("/event")
async def event(
        _event: Union[EventLog, TradeLog],
        redis_client: Redis = Depends(get_redis_database)
):
    # if _event is "EventLog" then:
    #   a. update "depth"
    #   b. forward event to user for "order rest" and "order cancel"
    # if _event is "TradeLog" then update "depth" and kline
    #   a. update "depth"
    #   b. update "kline"
    #   c. forward event to both users for "trade"

    await TradeService.update_depth(redis_client, _event)
