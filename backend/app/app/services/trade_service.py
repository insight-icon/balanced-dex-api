from typing import Union

from app.crud.crud_depth import CrudDepth
from app.models.orders import EventLog, TradeLog
from pydantic import typing


class TradeService:
    # key   => <market>-<buy/sell>-<price>
    # value => summation of open orders (increment when "orderRest", decrement when "orderTrade")
    # __open_depth: typing.Dict[str, float] => model to Redis collection

    # @staticmethod
    # async def get_depth(redis_client, ):
    #     # return self.__open_depth

    @staticmethod
    async def update_depth(redis_client, _event_or_trade: Union[EventLog, TradeLog]):
        if _event_or_trade.event == "Trade":
            key_sell = TradeService.__create_key(_event_or_trade.market, 1, _event_or_trade.price)
            await CrudDepth.set_or_update_depth(redis_client, key_sell, _event_or_trade, multiplying_factor=-1)
            key_buy = TradeService.__create_key(_event_or_trade.market, 2, _event_or_trade.price)
            await CrudDepth.set_or_update_depth(redis_client, key_buy, _event_or_trade, multiplying_factor=-1)
        else:
            key = TradeService.__create_key(_event_or_trade.market, _event_or_trade.side, _event_or_trade.price)
            if _event_or_trade.event == "OrderRest":
                await CrudDepth.set_or_update_depth(redis_client, key, _event_or_trade, multiplying_factor=1)
            elif _event_or_trade.event == "OrderCancel":
                await CrudDepth.set_or_update_depth(redis_client, key, _event_or_trade, multiplying_factor=-1)

    @staticmethod
    def __create_key(_market: str, _side: int, _price: str) -> str:
        if _side == 1 or _side == 2:
            return f"{_market}-{TradeService.__is_buy_or_sell(_side)}-{_price}"
        else:
            return f"{_market}-side-{_price}"

    @staticmethod
    def __is_buy_or_sell(_side: int) -> str:
        if _side == 1:
            return "sell"
        if _side == 2:
            return "buy"
        return "-"
