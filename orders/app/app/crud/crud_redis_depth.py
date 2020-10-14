import json

from app.crud.crud_redis_general import CrudRedisGeneral
from app.models import OpenOrder


class CrudRedisDepth:

    @staticmethod
    async def exists_order_id(redis_client, order_id: int):
        order_id_key = CrudRedisDepth._create_order_key(order_id)
        return await CrudRedisGeneral.exists(redis_client, order_id_key)

    @staticmethod
    async def get_open_order_for_order_id(redis_client, order_id: int) -> float:
        order_id_key = CrudRedisDepth._create_order_key(order_id)
        value_bytes = await CrudRedisGeneral.get(redis_client, order_id_key)
        if value_bytes is None:
            value = {"side": 0, "size": 0}
        else:
            value_str = value_bytes.decode(encoding="utf-8")
            value = json.loads(value_str)
        return value

    @staticmethod
    async def get_open_size_for_order_id(redis_client, order_id: int) -> float:
        value = await CrudRedisDepth.get_open_order_for_order_id(redis_client, order_id)
        return value["size"]

    @staticmethod
    async def get_open_side_for_order_id(redis_client, order_id: int) -> int:
        value = await CrudRedisDepth.get_open_order_for_order_id(redis_client, order_id)
        return value["side"]

    @staticmethod
    async def set_open_order(redis_client, order_id: int, side: int, size: float):
        open_order = OpenOrder(side=side, size=size)
        open_order_json = open_order.json()
        order_id_key = CrudRedisDepth._create_order_key(order_id)
        return await CrudRedisGeneral.set(redis_client, order_id_key, open_order_json)

    @staticmethod
    async def set_depth(redis_client, market: str, side: int, price: str, value: float):
        depth_key = CrudRedisDepth._create_depth_key(market, side, price)
        return await CrudRedisGeneral.set(redis_client, depth_key, str(value))

    @staticmethod
    async def get_depth(redis_client, market: str, side: int, price: str) -> float:
        depth_key = CrudRedisDepth._create_depth_key(market, side, price)
        value_bytes = await CrudRedisGeneral.get(redis_client, depth_key)
        if value_bytes is None:
            value = 0
        else:
            value = float(value_bytes.decode(encoding="utf-8"))
        return value

    @staticmethod
    async def delete_depth(redis_client, market: str, side: int, price: str):
        depth_key = CrudRedisDepth._create_depth_key(market, side, price)
        return await CrudRedisGeneral.delete(redis_client, depth_key)

    @staticmethod
    async def cancel_order_id(redis_client, order_id: int):
        order_id_key = CrudRedisDepth._create_order_key(order_id)
        return await CrudRedisGeneral.delete(redis_client, order_id_key)

    @staticmethod
    def _create_depth_key(_market: str, _side: int, _price: str) -> str:
        if _side == 1 or _side == 2:
            return f"depth-{_market}-{CrudRedisDepth._is_buy_or_sell(_side)}-{_price}".lower()

    @staticmethod
    def create_depth_key(_market: str, _side: int, _price: str) -> str:
        if _side == 1 or _side == 2:
            return f"depth-{_market}-{CrudRedisDepth._is_buy_or_sell(_side)}-{_price}".lower()

    @staticmethod
    def _is_buy_or_sell(_side: int) -> str:
        if _side == 1:
            return "sell"
        if _side == 2:
            return "buy"
        return "-"

    @staticmethod
    def _create_order_key(_order_id: int) -> str:
        return f"order-{_order_id}".lower()

