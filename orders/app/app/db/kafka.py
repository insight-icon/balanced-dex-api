from asyncio import AbstractEventLoop

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from app.models.rwmodel import RWModel
from loguru import logger


def create_kafka_producer(loop: AbstractEventLoop,
                          client_id: str,
                          bootstrap_server: str,
                          api_version: str = "2.0.1") -> AIOKafkaProducer:
    logger.info(f"Kafka producer connecting")
    kafka_producer = AIOKafkaProducer(
        loop=loop,
        client_id=client_id,  # "event-producer",
        bootstrap_servers=bootstrap_server,  # settings.KAFKA_INTERNAL_HOST_PORT,
        api_version=api_version
    )
    # logger.info(f"created kafka producer connection {kafka_producer.__dict__}")
    logger.info(f"Kafka producer connected")
    return kafka_producer


async def close_kafka_producer(producer: AIOKafkaProducer):
    # logger.info(f"closing kafka producer connection {producer.__dict__}")
    logger.info(f"Stopping Kafka producer")
    await producer.stop()
    logger.info(f"Stopped Kafka producer")


def create_kafka_consumer(loop: AbstractEventLoop,
                          client_id: str,
                          bootstrap_server: str,
                          enable_auto_commit: bool = False,
                          api_version: str = "2.0.1") -> AIOKafkaConsumer:
    logger.info(f"Kafka consumer connecting")
    kafka_consumer = AIOKafkaConsumer(
        loop=loop,
        client_id=client_id,
        bootstrap_servers=bootstrap_server,
        metadata_max_age_ms=30000,
        enable_auto_commit=enable_auto_commit,
        api_version=api_version
    )
    # logger.info(f"created kafka consumer connection {kafka_consumer.__dict__}")
    logger.info(f"Kafka consumer connected")
    return kafka_consumer


async def close_kafka_consumer(consumer: AIOKafkaConsumer):
    # logger.info(f"closing kafka consumer connection {consumer.__dict__}")
    logger.info(f"Stopping Kafka consumer")
    await consumer.stop()
    logger.info(f"Stopped Kafka consumer")
