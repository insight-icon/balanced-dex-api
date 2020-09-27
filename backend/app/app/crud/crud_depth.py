from typing import Union

from app import models
from app.models.orders import EventLog, TradeLog


class CrudDepth:

    @staticmethod
    async def set_or_update_depth(redis_client, _key: str, _value: Union[EventLog, TradeLog], multiplying_factor: int):
        curr_value = await CrudDepth.get(redis_client, _key)
        if curr_value is None:
            curr_value = 0
        multiplying_factor = multiplying_factor / abs(multiplying_factor)
        new_value = curr_value + float(_value.size) * multiplying_factor
        await CrudDepth.set(redis_client, _key, max(new_value, 0)) # todo: clarify that value of depth will never go below 0

    @staticmethod
    async def set(redis_client, key, value):
        return await redis_client.set(key, value)

    @staticmethod
    async def get(redis_client, key):
        return await redis_client.get(key)

# crud_depth = CrudDepth()
