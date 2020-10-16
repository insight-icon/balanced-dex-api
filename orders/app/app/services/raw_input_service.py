from typing import Union

from loguru import logger

from app.crud.crud_mongodb_raw_input import CrudMongodbRawInput
from app.models import EventLog, TradeLog


class RawInputService:

    @staticmethod
    async def save_raw_event(mongodb_client, _event_or_trade: Union[EventLog, TradeLog]) -> bool:
        # key = RawInputService.__create_raw_key(_event_or_trade)
        # value = _event_or_trade.json()
        # logger.info(f"saving raw event: {key} - {value}")
        # is_saved = await CrudMongodbRawInput.set(redis_client, key, value)
        # return is_saved

        is_saved = await CrudMongodbRawInput.set(mongodb_client, _event_or_trade)
        return is_saved


