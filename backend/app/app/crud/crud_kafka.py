from asyncio import AbstractEventLoop
from typing import Union

import asyncio
from aiokafka import AIOKafkaProducer
from app.core.config import settings
from kafka.errors import KafkaConnectionError
from loguru import logger


class CrudKafka:

    @staticmethod
    def create_kafka_producer(loop:  AbstractEventLoop, client_id: str, bootstrap_server: str) -> AIOKafkaProducer:
        # loop = asyncio.get_event_loop()
        producer = AIOKafkaProducer(
            loop=loop,
            client_id=client_id,  # "event-producer",
            bootstrap_servers=bootstrap_server,  # settings.KAFKA_INTERNAL_HOST_PORT,
            api_version="2.0.1"
        )
        return producer

    @staticmethod
    async def publish_message_to_topics(kafka_producer: AIOKafkaProducer, topics: list, msg: bytes):
        result = {}
        try:
            await kafka_producer.start()
            for topic in topics:
                sending_msg = await kafka_producer.send(topic, msg)
                await kafka_producer.flush()
                result[topic] = sending_msg.done()
                logger.info(f"result[topic]: {topic}:{result[topic]}")
        except KafkaConnectionError:
            logger.error("Kafka connection error")
            await kafka_producer.stop()

        return result

    @staticmethod
    async def publish_key_value_to_topics(kafka_producer: AIOKafkaProducer, topics: list, value: bytes, key: bytes):
        result = {}
        try:
            await kafka_producer.start()
            for topic in topics:
                logger.info(f"publish_key_value_to_topics - key: {key}, value: {value}")
                if key is None:
                    sending_msg = await kafka_producer.send(topic=topic, value=value)
                else:
                    sending_msg = await kafka_producer.send(topic=topic, value=value, key=key)
                await kafka_producer.flush()
                result[topic] = sending_msg.done()
                logger.info(f"result[topic]: {topic}:{result[topic]}")
        except KafkaConnectionError:
            logger.error("Kafka connection error")
            await kafka_producer.stop()

        return result
