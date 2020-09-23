import aioredis
import asyncio
from app.core.config import settings

from .redis import redis
from loguru import logger


async def connect_to_redis():
    logger.info("Connecting to Redis")
    # try:
    redis.client = await asyncio.wait_for(aioredis.create_redis_pool(settings.REDIS_CONNECTION), 3)
    # except asyncio.TimeoutError:
    #     logger.error('connect_to_redis timeout!')
    logger.info("Connected to Redis")


async def close_redis_connection():
    logger.info("Closing connection to Redis")
    # try:
    redis.client.close()
    await redis.client.wait_closed()
    # except asyncio.TimeoutError:
    #     logger.error('close_redis_connection timeout!')
    logger.info("Closed connection to Redis")
