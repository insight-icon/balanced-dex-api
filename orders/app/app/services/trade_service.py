import json
from typing import Union

from aiokafka import AIOKafkaProducer
from app.crud.crud_kafka import CrudKafka
from app.crud.crud_redis_general import CrudRedisGeneral
from app.crud.crud_redis_depth import CrudRedisDepth
from loguru import logger

from app.models.eventlog import EventLog
from app.models.tradelog import TradeLog
from pydantic import typing


class TradeService:
    # key   => <market>-<buy/sell>-<price>
    # value => summation of open orders (increment when "orderRest", decrement when "orderTrade")
    # __open_depth: typing.Dict[str, float] => model to Redis collection

    @staticmethod
    async def use_db(redis_client, db: int):
        await redis_client.select(db)

    # @staticmethod
    # async def get_depth(redis_client, _key: str):
    #     return await CrudRedisGeneral.get(redis_client, _key)
    #
    # @staticmethod
    # async def get_keys(redis_client, _pattern: str):
    #     return await CrudRedisGeneral.iscan(redis_client, _pattern)
    #
    @staticmethod
    async def get_key_value_pairs(redis_client, _pattern: str):
        return await CrudRedisGeneral.get_key_value_pairs(redis_client, _pattern)

    # @staticmethod
    # async def save_raw_event(redis_client, _event_or_trade: Union[EventLog, TradeLog]) -> bool:
    #     key = TradeService.__create_raw_key(_event_or_trade)
    #     value = _event_or_trade.json()
    #     logger.info(f"saving raw event: {key} - {value}")
    #     is_saved = await CrudDepth.set(redis_client, key, value)
    #     return is_saved

    # @staticmethod
    # def __create_raw_key(_event_or_trade: Union[EventLog, TradeLog]) -> str:
    #     if _event_or_trade.event == "Trade":
    #         key = f"{_event_or_trade.event}-{_event_or_trade.maker_order}-{_event_or_trade.taker_order}"
    #     else:
    #         key = f"{_event_or_trade.event}-{_event_or_trade.order_id}"
    #     return key

    @staticmethod
    async def update_depth(redis_client, kafka_producer: AIOKafkaProducer, _event_or_trade: Union[EventLog, TradeLog]) -> dict:
        logger.info("!!!!!!!     update_depth update_depth update_depth     !!!!!!!!!")
        order_ids = await TradeService._get_order_ids(_event_or_trade)
        results = {}
        for order_id in order_ids:
            event_type = _event_or_trade.event
            is_order_exist = await CrudRedisDepth.exists_order_id(redis_client, order_id)  # 0 or 1
            if event_type == "OrderRest" and is_order_exist == 0:
                (key, value) = await TradeService._process_depth_for_new_order_rest(redis_client, order_id, _event_or_trade)
                results[key] = value
            elif event_type == "OrderRest" and is_order_exist == 1:
                (key, value) = await TradeService._process_depth_for_existing_order_rest(redis_client, order_id, _event_or_trade)
                logger.info(f"event_type == OrderRest and is_order_exist == 1, key={key}, value={value}")
                results[key] = value
            elif event_type == "OrderCancel" and is_order_exist == 1:
                (key, value) = await TradeService._process_depth_for_order_cancel(redis_client, order_id, _event_or_trade)
                results[key] = value
            elif event_type == "Trade" and is_order_exist == 1:
                (key, value) = await TradeService._process_depth_for_trade(redis_client, order_id, _event_or_trade)
                results[key] = value

        await TradeService._publish_depth_to_kafka(kafka_producer, results)
        return results

    @staticmethod
    async def _get_order_ids(_event_or_trade: Union[EventLog, TradeLog]) -> list:
        order_ids = []
        if _event_or_trade.event == "Trade":
            order_ids.append(_event_or_trade.maker_order)
            order_ids.append(_event_or_trade.taker_order)
        else:
            order_ids.append(_event_or_trade.order_id)
        logger.info(f"orders id = {order_ids}")
        return order_ids

    @staticmethod
    async def _process_depth_for_new_order_rest(redis_client, order_id: int, _event_or_trade: EventLog):
        diff = float(_event_or_trade.size)
        logger.info(f"new_value in new order of OrderRest = {diff}")
        # order
        is_saved_order = await CrudRedisDepth.set_open_order(redis_client, order_id, _event_or_trade.side,
                                                             diff)
        logger.info(f"is_saved_order={is_saved_order}")
        # depth
        old_depth_value = await CrudRedisDepth.get_depth(redis_client,
                                                         _event_or_trade.market,
                                                         _event_or_trade.side,
                                                         _event_or_trade.price)
        new_depth_value = old_depth_value + diff
        if new_depth_value == 0:
            is_deleted = await CrudRedisDepth.delete_depth(redis_client,
                                                           _event_or_trade.market,
                                                           _event_or_trade.side,
                                                           _event_or_trade.price)
            logger.info(f"new depth = 0, deleted depth = {is_deleted}")
        else:
            is_saved_depth = await CrudRedisDepth.set_depth(redis_client,
                                                            _event_or_trade.market,
                                                            _event_or_trade.side,
                                                            _event_or_trade.price,
                                                            new_depth_value)
            logger.info(f"is_saved_depth={is_saved_depth}")

        depth_key = CrudRedisDepth.create_depth_key(_event_or_trade.market, _event_or_trade.side,
                                                    _event_or_trade.price)
        return depth_key, new_depth_value

    @staticmethod
    async def _process_depth_for_existing_order_rest(redis_client, order_id: int, _event_or_trade: EventLog):
        old_order_value = await CrudRedisDepth.get_open_size_for_order_id(redis_client, order_id)
        new_order_value = float(_event_or_trade.size)
        diff = new_order_value - old_order_value
        depth_key = CrudRedisDepth.create_depth_key(_event_or_trade.market, _event_or_trade.side,
                                                    _event_or_trade.price)
        old_depth_value = await CrudRedisDepth.get_depth(redis_client,
                                                         _event_or_trade.market,
                                                         _event_or_trade.side,
                                                         _event_or_trade.price)
        logger.info(f"diff in existing order for OrderRest, old value = {old_order_value}, diff = {diff}")
        if diff != 0:
            # order
            is_saved_order = await CrudRedisDepth.set_open_order(redis_client,
                                                                 order_id,
                                                                 _event_or_trade.side,
                                                                 new_order_value)
            logger.info(f"is_saved_order={is_saved_order}")
            # depth
            new_depth_value = old_depth_value + diff
            if new_depth_value == 0:
                is_deleted = await CrudRedisDepth.delete_depth(redis_client,
                                                               _event_or_trade.market,
                                                               _event_or_trade.side,
                                                               _event_or_trade.price)
                logger.info(f"new depth = 0, deleted depth = {is_deleted}")
            else:
                is_saved_depth = await CrudRedisDepth.set_depth(redis_client,
                                                                _event_or_trade.market,
                                                                _event_or_trade.side,
                                                                _event_or_trade.price,
                                                                new_depth_value)
                logger.info(f"is_saved_depth={is_saved_depth}")
            return depth_key, new_depth_value
        return depth_key, old_depth_value

    @staticmethod
    async def _process_depth_for_order_cancel(redis_client, order_id: int, _event_or_trade: EventLog):
        old_order_value = await CrudRedisDepth.get_open_size_for_order_id(redis_client, order_id)
        diff = (-1) * old_order_value
        logger.info(f"diff in existing order for OrderCancel = {diff}")
        # order
        is_deleted = await CrudRedisDepth.cancel_order_id(redis_client, order_id)
        logger.info(f"is_deleted={is_deleted}")
        # depth
        old_depth_value = await CrudRedisDepth.get_depth(redis_client,
                                                         _event_or_trade.market,
                                                         _event_or_trade.side,
                                                         _event_or_trade.price)
        new_depth_value = old_depth_value + diff
        if new_depth_value == 0.0:
            is_deleted = await CrudRedisDepth.delete_depth(redis_client,
                                                           _event_or_trade.market,
                                                           _event_or_trade.side,
                                                           _event_or_trade.price)
            logger.info(f"new depth = 0, deleted depth = {is_deleted}")
        else:
            is_saved_depth = await CrudRedisDepth.set_depth(redis_client,
                                                            _event_or_trade.market,
                                                            _event_or_trade.side,
                                                            _event_or_trade.price,
                                                            new_depth_value)
            logger.info(f"is_saved_depth={is_saved_depth}")

        depth_key = CrudRedisDepth.create_depth_key(_event_or_trade.market, _event_or_trade.side,
                                                    _event_or_trade.price)
        return depth_key, new_depth_value

    @staticmethod
    async def _process_depth_for_trade(redis_client, order_id: int, _event_or_trade: EventLog):
        old_order_value = await CrudRedisDepth.get_open_size_for_order_id(redis_client, order_id)
        diff = (-1) * float(_event_or_trade.size)
        new_order_value = old_order_value + diff
        side = await CrudRedisDepth.get_open_side_for_order_id(redis_client, order_id)
        logger.info(f"diff in existing order for Trade = {diff}")
        # order
        if new_order_value == 0:
            deleted = await CrudRedisDepth.cancel_order_id(redis_client, order_id)
            logger.info(f"new_order_value = 0, deleting order_id - {order_id}, deleted - {deleted}")
        else:
            is_saved_order = await CrudRedisDepth.set_open_order(redis_client,
                                                                 order_id,
                                                                 side,
                                                                 new_order_value)
            logger.info(f"is_saved_order={is_saved_order}")
        # depth
        old_depth_value = await CrudRedisDepth.get_depth(redis_client,
                                                         _event_or_trade.market,
                                                         side,
                                                         _event_or_trade.price)
        new_depth_value = old_depth_value + diff
        if new_depth_value == 0:
            is_deleted = await CrudRedisDepth.delete_depth(redis_client, _event_or_trade.market, side,
                                                           _event_or_trade.price)
            logger.info(f"new depth = 0, deleted depth = {is_deleted}")
        else:
            is_saved_depth = await CrudRedisDepth.set_depth(redis_client,
                                                            _event_or_trade.market,
                                                            side,
                                                            _event_or_trade.price,
                                                            new_depth_value)
            logger.info(f"is_saved_depth={is_saved_depth}")

        depth_key = CrudRedisDepth.create_depth_key(_event_or_trade.market, side,
                                                    _event_or_trade.price)
        return depth_key, new_depth_value

    @staticmethod
    async def _publish_depth_to_kafka(kafka_producer: AIOKafkaProducer, results: dict):
        logger.info("publish to topic depth")
        for key, value in results.items():
            value_bytes = str(value).encode("utf-8")
            key_bytes = str(key).encode("utf-8")
            topics = TradeService._get_kafka_topics_from_depth_key(key)
            logger.info(f"TradeService._publish_depth_to_kafka - topics: {topics}")
            logger.info(f"TradeService._publish_depth_to_kafka - key: {key_bytes}, value: {value_bytes}")
            await CrudKafka.publish_key_value_to_topics(kafka_producer, topics, value_bytes, key_bytes)

    @staticmethod
    def _get_kafka_topics_from_depth_key(depth_key: str):
        topics = ["depth-all"]
        market = depth_key.split("-")[1]
        topic = f"depth-{market}".lower()
        topics.append(topic)
        return topics
