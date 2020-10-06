from asyncio import AbstractEventLoop

from aiokafka import AIOKafkaProducer
from app.models.rwmodel import RWModel
from loguru import logger


def create_kafka_producer(loop: AbstractEventLoop,
                                client_id: str,
                                bootstrap_server: str,
                                api_version: str = "2.0.1") -> AIOKafkaProducer:
    kafka_producer = AIOKafkaProducer(
        loop=loop,
        client_id=client_id,  # "event-producer",
        bootstrap_servers=bootstrap_server,  # settings.KAFKA_INTERNAL_HOST_PORT,
        api_version=api_version
    )
    logger.info(f"created kafka producer connection {kafka_producer.__dict__}")
    return kafka_producer


async def close_kafka_producer(producer: AIOKafkaProducer) -> AIOKafkaProducer:
    logger.info(f"closing kafka producer connection {producer.__dict__}")
    return await producer.stop()
