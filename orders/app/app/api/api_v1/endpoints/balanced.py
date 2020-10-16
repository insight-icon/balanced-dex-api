from typing import Union

from motor.motor_asyncio import AsyncIOMotorClient

from app.crud.crud_redis_general import CrudRedisGeneral

from app.db.kafka import create_kafka_producer, close_kafka_producer
from app.db.mongodb import get_mongodb_database
from app.services.kline_service import KLineService
from app.services.ws_service import WsService
from loguru import logger
import asyncio

from aiokafka import AIOKafkaProducer
from aioredis import Redis
from app.core.config import settings
from app.db.redis import get_redis_database

from app import models

from app.services.trade_service import TradeService
from fastapi import APIRouter, Depends

router = APIRouter()
kafka_producer: AIOKafkaProducer


async def init():
    global kafka_producer
    kafka_producer = get_kafka_producer()


async def shut():
    global kafka_producer
    await close_kafka_producer(kafka_producer)


def get_kafka_producer() -> AIOKafkaProducer:
    loop = asyncio.get_event_loop()
    client_id = "balanced_kafka_producer"
    bootstrap_server = settings.KAFKA_INTERNAL_HOST_PORT
    producer = create_kafka_producer(loop=loop, client_id=client_id, bootstrap_server=bootstrap_server)
    return producer


router.add_event_handler("startup", init)
router.add_event_handler("shutdown", shut)


@router.post("/event")
async def event(
        _event_or_trade: Union[models.EventLog, models.TradeLog],
        mongodb_client: AsyncIOMotorClient = Depends(get_mongodb_database),
        redis_client: Redis = Depends(get_redis_database)
):
    # save raw input in mongodb
    # logger.info(f"mongodb_client db => {mongodb_client}")
    # is_saved = await TradeService.save_raw_event(redis_client, _event_or_trade)
    # logger.info(f"TradeService.save_raw_event - is_saved ? {is_saved}")

    # 1. update "depth", then send new depth value to kafka topic
    # 2. update "kline", then send new kline(add 1min) to kafka topic
    # 3. forward event/trade to either 1 or both users

    results = {}
    # # redis_client to db = 0
    # await TradeService.use_db(redis_client, 0)
    # update depth
    depth_updates = await TradeService.update_depth(redis_client, kafka_producer, _event_or_trade)
    # logger.info(f"balanced::: depth_updates: {depth_updates}")
    results["depth"] = depth_updates
    # update kline
    kline_updates = await KLineService.update_kline(redis_client, kafka_producer, _event_or_trade)
    # logger.info(f"balanced::: kline_updates: {kline_updates}")
    results["kline"] = kline_updates
    # send event to kafka topic
    publish_to_users = await WsService.publish_to_topic(kafka_producer, _event_or_trade)
    # logger.info(f"balanced::: publish to users: {publish_to_users}")
    results["publish_to_users"] = publish_to_users

    return results


@router.post("/search")
async def search(
        _pattern: models.Msg,
        redis_client: Redis = Depends(get_redis_database)
):
    # await TradeService.use_db(redis_client, 0)
    key_value_pairs = await TradeService.get_key_value_pairs(redis_client, _pattern.msg)
    return key_value_pairs


@router.get("/events/cleanup")
async def cleanup(
        redis_client: Redis = Depends(get_redis_database)
):
    # await TradeService.use_db(redis_client, 0)
    await CrudRedisGeneral.cleanup(redis_client, "*")
    return True
