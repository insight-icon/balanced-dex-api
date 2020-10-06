import json
from typing import Union

from aiokafka import AIOKafkaProducer
from app.crud.crud_kafka import CrudKafka
from app.models import EventLog, TradeLog
from kafka.errors import KafkaConnectionError
from loguru import logger


class WsService:

    @staticmethod
    async def publish_to_topic(kafka_producer: AIOKafkaProducer, _event_or_trade: Union[EventLog, TradeLog]) -> dict:
        logger.info("!!! WS service !!!")
        topics = []
        if type(_event_or_trade) == EventLog:
            topics.append(_event_or_trade.user)
        elif type(_event_or_trade) == TradeLog:
            topics.append(_event_or_trade.maker)
            topics.append(_event_or_trade.taker)

        msg = json.dumps(_event_or_trade.dict()).encode("ascii")
        key = str(_event_or_trade.timestamp).encode("utf-8")
        result = await CrudKafka.publish_message_to_topics(kafka_producer, topics, msg)
        return result

