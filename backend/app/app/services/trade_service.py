import json
from typing import Union

from app.crud.crud_redis_general import CrudRedisGeneral
from app.crud.crud_redis_orders import CrudRedisOrders
from loguru import logger

from app.crud.crud_depth import CrudDepth
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
    # async def update_depth(redis_client, _event_or_trade: Union[EventLog, TradeLog]) -> dict:
    #     if _event_or_trade.event == "Trade":
    #         updates = await TradeService.__update_depth_for_trade(redis_client, _event_or_trade)
    #     else:
    #         updates = await TradeService.__update_depth_for_event(redis_client, _event_or_trade)
    #     return updates
    #
    # @staticmethod
    # async def __update_depth_for_trade(redis_client, _event_or_trade: TradeLog) -> dict:
    #     updates = {}
    #     key_sell = TradeService.__create_depth_key(_event_or_trade.market, 1, _event_or_trade.price)
    #     logger.info(f"key_sell: {key_sell}")
    #     updates["sell"] = \
    #         await CrudDepth.set_or_update_depth(redis_client, key_sell, _event_or_trade, multiplying_factor=-1)
    #     key_buy = TradeService.__create_depth_key(_event_or_trade.market, 2, _event_or_trade.price)
    #     logger.info(f"key_buy: {key_buy}")
    #     updates["buy"] = \
    #         await CrudDepth.set_or_update_depth(redis_client, key_buy, _event_or_trade, multiplying_factor=-1)
    #     return updates
    #
    # @staticmethod
    # async def __update_depth_for_event(redis_client, _event_or_trade: EventLog) -> dict:
    #     updates = {}
    #     if _event_or_trade.event == "OrderRest":
    #         updates = await TradeService.__update_depth_for_event_order_rest(redis_client, _event_or_trade)
    #     elif _event_or_trade.event == "OrderCancel":
    #         updates = await TradeService.__update_depth_for_event_order_cancel(redis_client, _event_or_trade)
    #     return updates
    #
    #     # updates = {}
    #     # depth_key = TradeService.__create_depth_key(_event_or_trade.market, _event_or_trade.side, _event_or_trade.price)
    #     # logger.info(f"key: {depth_key}")
    #     # if _event_or_trade.event == "OrderRest":
    #     #     updates[str(_event_or_trade.side)] = \
    #     #         await CrudDepth.set_or_update_depth(redis_client, depth_key, _event_or_trade, multiplying_factor=1)
    #     # elif _event_or_trade.event == "OrderCancel":
    #     #     updates[str(_event_or_trade.side)] = \
    #     #         await CrudDepth.set_or_update_depth(redis_client, depth_key, _event_or_trade, multiplying_factor=-1)
    #     # return updates
    #
    # @staticmethod
    # async def __update_depth_for_event_order_rest(redis_client, _event_or_trade: EventLog) -> dict:
    #     order_key = TradeService.__create_order_key()
    #     return {}
    #
    # @staticmethod
    # async def __update_depth_for_event_order_cancel(redis_client, _event_or_trade: EventLog) -> dict:
    #     return {}

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
    async def update_depth(redis_client, _event_or_trade: Union[EventLog, TradeLog]) -> dict:
        logger.info("!!!!!!!     update_depth update_depth update_depth     !!!!!!!!!")
        order_ids = []
        if _event_or_trade.event == "Trade":
            order_ids.append(_event_or_trade.maker_order)
            order_ids.append(_event_or_trade.taker_order)
        else:
            order_ids.append(_event_or_trade.order_id)
        logger.info(f"orders id = {order_ids}")

        for order_id in order_ids:
            event_type = _event_or_trade.event
            is_order_exist = await CrudRedisOrders.exists_order_id(redis_client, order_id)  # 0 or 1
            if event_type == "OrderRest" and is_order_exist == 0:
                diff = float(_event_or_trade.size)
                logger.info(f"new_value in new order of OrderRest = {diff}")
                # order
                is_saved_order = await CrudRedisOrders.set_open_order(redis_client, order_id, _event_or_trade.side,
                                                                      diff)
                logger.info(f"is_saved_order={is_saved_order}")
                # depth
                old_depth_value = await CrudRedisOrders.get_depth(redis_client,
                                                                  _event_or_trade.market,
                                                                  _event_or_trade.side,
                                                                  _event_or_trade.price)
                new_depth_value = old_depth_value + diff
                is_saved_depth = await CrudRedisOrders.set_depth(redis_client,
                                                                 _event_or_trade.market,
                                                                 _event_or_trade.side,
                                                                 _event_or_trade.price,
                                                                 new_depth_value)
                logger.info(f"is_saved_depth={is_saved_depth}")
                pass
            elif event_type == "OrderRest" and is_order_exist == 1:
                old_order_value = await CrudRedisOrders.get_open_size_for_order_id(redis_client, order_id)
                new_order_value = float(_event_or_trade.size)
                diff = new_order_value - old_order_value
                logger.info(f"diff in existing order for OrderRest, old value = {old_order_value}, diff = {diff}")
                if diff != 0:
                    # order
                    is_saved_order = await CrudRedisOrders.set_open_order(redis_client,
                                                                          order_id,
                                                                          _event_or_trade.side,
                                                                          new_order_value)
                    logger.info(f"is_saved_order={is_saved_order}")
                    # depth
                    old_depth_value = await CrudRedisOrders.get_depth(redis_client,
                                                                      _event_or_trade.market,
                                                                      _event_or_trade.side,
                                                                      _event_or_trade.price)
                    is_saved_depth = await CrudRedisOrders.set_depth(redis_client,
                                                                     _event_or_trade.market,
                                                                     _event_or_trade.side,
                                                                     _event_or_trade.price,
                                                                     old_depth_value + diff)
                    logger.info(f"is_saved_depth={is_saved_depth}")
                pass
            elif event_type == "OrderCancel" and is_order_exist == 1:
                old_order_value = await CrudRedisOrders.get_open_size_for_order_id(redis_client, order_id)
                diff = (-1) * old_order_value
                logger.info(f"diff in existing order for OrderCancel = {diff}")
                # order
                is_deleted = await CrudRedisOrders.cancel_order_id(redis_client, order_id)
                logger.info(f"is_deleted={is_deleted}")
                # depth
                old_depth_value = await CrudRedisOrders.get_depth(redis_client,
                                                                  _event_or_trade.market,
                                                                  _event_or_trade.side,
                                                                  _event_or_trade.price)
                is_saved_depth = await CrudRedisOrders.set_depth(redis_client,
                                                                 _event_or_trade.market,
                                                                 _event_or_trade.side,
                                                                 _event_or_trade.price,
                                                                 old_depth_value + diff)
                logger.info(f"is_saved_depth={is_saved_depth}")
                pass
            elif event_type == "Trade" and is_order_exist == 1:
                old_order_value = await CrudRedisOrders.get_open_size_for_order_id(redis_client, order_id)
                diff = (-1) * float(_event_or_trade.size)
                new_order_value = old_order_value + diff
                side = await CrudRedisOrders.get_open_side_for_order_id(redis_client, order_id)
                logger.info(f"diff in existing order for Trade = {diff}")
                # order
                if new_order_value == 0:
                    deleted = await CrudRedisOrders.cancel_order_id(redis_client, order_id)
                    logger.info(f"new_order_value = 0, deleting order_id - {order_id}, deleted - {deleted}")
                else:
                    is_saved_order = await CrudRedisOrders.set_open_order(redis_client,
                                                                          order_id,
                                                                          _event_or_trade.side,
                                                                          new_order_value)
                    logger.info(f"is_saved_order={is_saved_order}")
                # depth
                old_depth_value = await CrudRedisOrders.get_depth(redis_client,
                                                                  _event_or_trade.market,
                                                                  side,
                                                                  _event_or_trade.price)
                is_saved_depth = await CrudRedisOrders.set_depth(redis_client,
                                                                 _event_or_trade.market,
                                                                 side,
                                                                 _event_or_trade.price,
                                                                 old_depth_value + diff)
                logger.info(f"is_saved_depth={is_saved_depth}")
                pass

            # if diff == 0:
            #     deleted = await CrudRedisOrders.cancel_order_id(redis_client, order_id)
            #     logger.info(f"diff = 0, deleting order_id - {order_id}, deleted - {deleted}")

    # @staticmethod
    # def __create_depth_key(_market: str, _side: int, _price: str) -> str:
    #     if _side == 1 or _side == 2:
    #         return f"depth-{_market}-{TradeService.__is_buy_or_sell(_side)}-{_price}"
    #
    # @staticmethod
    # def __is_buy_or_sell(_side: int) -> str:
    #     if _side == 1:
    #         return "sell"
    #     if _side == 2:
    #         return "buy"
    #     return "-"
    #
    # @staticmethod
    # def __create_order_key(order_id: int):
    #     return f"order-{order_id}"
