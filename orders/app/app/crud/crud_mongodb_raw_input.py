from typing import Union

from app.models import EventLog, TradeLog


class CrudMongodbRawInput:

    @staticmethod
    async def set(mongodb_client, _event_or_trade: Union[EventLog, TradeLog]):
        pass


    # @staticmethod
    # def __create_raw_key(_event_or_trade: Union[EventLog, TradeLog]) -> str:
    #     if _event_or_trade.event == "Trade":
    #         key = f"{_event_or_trade.event}-{_event_or_trade.maker_order}-{_event_or_trade.taker_order}"
    #     else:
    #         key = f"{_event_or_trade.event}-{_event_or_trade.order_id}"
    #     return key