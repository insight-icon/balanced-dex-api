from loguru import logger

from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings
from .mongodb import mongodb


async def connect_to_mongodb():
    logger.info("Connecting to Mongodb")
    mongodb.client = AsyncIOMotorClient(f"{settings.MONGODB_HOST}:{settings.MONGODB_PORT}",
                                        maxPoolSize=5,
                                        minPoolSize=1)
    logger.info("Connected to Mongodb")


async def close_mongodb_connection():
    logger.info("Closing connection to Mongodb")
    mongodb.client.close()
    logger.info("Closed connection to Mongodb")
