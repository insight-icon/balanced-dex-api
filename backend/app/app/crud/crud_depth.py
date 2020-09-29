from typing import Union

from app.crud.crud_redis_general import CrudRedisGeneral
from loguru import logger

from app import models
from app.models.eventlog import EventLog
from app.models.tradelog import TradeLog


class CrudDepth:

    @staticmethod
    async def set_or_update_depth(redis_client, _key: str, _value: Union[EventLog, TradeLog], multiplying_factor: int):
        curr_value_in_bytes = await CrudRedisGeneral.get(redis_client, _key)
        if curr_value_in_bytes is None:
            curr_value = 0.0
        else:
            curr_value_in_str = curr_value_in_bytes.decode(encoding="utf-8")
            curr_value = float(curr_value_in_str)
        # curr_value = float((await CrudDepth.get(redis_client, _key)).decode(encoding="utf-8"))
        # if curr_value is None:
        #     curr_value = 0
        multiplying_factor = multiplying_factor / abs(multiplying_factor)
        logger.info(f"curr_value: {curr_value}")
        new_value = curr_value + float(_value.size) * multiplying_factor
        logger.info(f"set_or_update_depth: {new_value}")
        is_saved = await CrudRedisGeneral.set(redis_client, _key, max(new_value, 0))  # todo: clarify that value of depth will never go below 0
        return is_saved

    # ########## crud for redis in general ############# #
    # @staticmethod
    # async def set(redis_client, key, value):
    #     return await redis_client.set(key, value)
    #
    # @staticmethod
    # async def get(redis_client, key):
    #     return await redis_client.get(key)
    #
    # @staticmethod
    # async def iscan(redis_client, pattern):
    #     logger.info(f"crud depth in iscan func, pattern is {pattern}")
    #     result = []
    #     async for key in redis_client.iscan(match=pattern):
    #         result.append(key)
    #     return result
    #
    # @staticmethod
    # async def get_key_value_pairs(redis_client, pattern):
    #     logger.info(f"crud depth in iscan func, pattern is {pattern}")
    #     keys = await CrudDepth.iscan(redis_client, pattern)
    #     result = {}
    #     for key in keys:
    #         result[key] = await CrudDepth.get(redis_client, key)
    #     return result



