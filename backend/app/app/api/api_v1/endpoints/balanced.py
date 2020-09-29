from typing import Union

from app.services.kline_service import KLineService
from loguru import logger
import asyncio

from aiokafka import AIOKafkaProducer
from aioredis import Redis
from app.core.config import settings
from app.db.redis import get_redis_database

# from app.models import RedisData
# from app.models import Msg
# from app.models.orders import EventLog, TradeLog
from app import models

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
        _event_or_trade: Union[models.EventLog, models.TradeLog],
        redis_client: Redis = Depends(get_redis_database)
):
    # # save raw event/trade in redis collection
    # # save raw _event in db 1
    # await TradeService.use_db(redis_client, 1)
    # logger.info(f"redis db => {redis_client.db}")
    # is_saved = await TradeService.save_raw_event(redis_client, _event_or_trade)
    # logger.info(f"TradeService.save_raw_event - is_saved ? {is_saved}")

    # 1. update "depth", then send new depth value to kafka topic
    # 2. update "kline", then send new kline(add 1min) to kafka topic
    # 3. forward event/trade to either 1 or both users

    # redis_client to db = 0
    await TradeService.use_db(redis_client, 0)
    # update depth
    depth_updates = await TradeService.update_depth(redis_client, _event_or_trade)
    # update kline
    kline_updates = await KLineService.update_kline(redis_client, _event_or_trade)
    # send event to kafka topic
    # todo here: send event to topic "user" or "maker"/"taker"



    return depth_updates


# @router.post("/event/keys/pattern")
# async def event(
#         _pattern: models.Msg,
#         redis_client: Redis = Depends(get_redis_database)
# ):
#     await TradeService.use_db(redis_client, 0)
#     keys = await TradeService.get_keys(redis_client, _pattern.msg)
#     return keys


@router.post("/depth/pattern")
async def event(
        _pattern: models.Msg,
        redis_client: Redis = Depends(get_redis_database)
):
    await TradeService.use_db(redis_client, 0)
    key_value_pairs = await TradeService.get_key_value_pairs(redis_client, _pattern.msg)
    return key_value_pairs


@router.get("/events")
async def events(
        redis_client: Redis = Depends(get_redis_database)
):
    await TradeService.use_db(redis_client, 1)
    key_value_pairs = await TradeService.get_key_value_pairs(redis_client, "*")
    return key_value_pairs
