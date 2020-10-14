import asyncio
from loguru import logger
from app.db.mongodb_utils import connect_to_mongodb, close_mongodb_connection
from app.db.redis_utils import connect_to_redis, close_redis_connection


async def db_init():
    try:
        await asyncio.wait_for(connect_to_mongodb(), timeout=3)
        await asyncio.wait_for(connect_to_redis(), timeout=3)

    except asyncio.TimeoutError:
        logger.error('db_init timeout!')


async def db_close():
    try:
        await asyncio.wait_for(close_mongodb_connection(), timeout=3)
        await asyncio.wait_for(close_redis_connection(), timeout=3)

    except asyncio.TimeoutError:
        logger.error('db_close timeout!')
