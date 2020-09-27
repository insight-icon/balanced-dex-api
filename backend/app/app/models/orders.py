from typing import Optional

from .rwmodel import RWModel
from pydantic import BaseModel


class EventLog(RWModel):
    """
    {
        "event":"OrderCreate",
        "order_id": 1,
        "side": 1,
        "market":"BALICD",
        "price":"0.0034",
        "size":"1.223",
        "user":"hxcd6f04b2a5184715ca89e523b6c823ceef2f9c3d"
    }
    """
    event: str
    order_id: int
    side: int
    market: str
    price: str  # todo: confirm datatype is str
    size: str  # todo: confirm datatype is str
    user: str


class TradeLog(RWModel):
    """
    {
        "event":"Trade",
        "market":"BALICD",
        "price":"0.003",
        "size":"1.223",
        "maker": "hxcd6f04b2a5184715ca89e523b6c823ceef2f9c3d",
        "maker_order": 3,
        "taker": "hx562dc1e2c7897432c298115bc7fbcc3b9d5df294",
        "taker_order": 4,
        "user":"hx562dc1e2c7897432c298115bc7fbcc3b9d5df294"
    }
    """
    event: str
    market: str
    price: str
    size: str
    maker: str
    maker_order: int
    taker: str
    taker_order: int
    user: str


# class OrderCreate(RWModel):
#     order_id: int
#     market: str
#     price: int
#     size: int
#     user: str
#
#
# class OrderRest(RWModel):
#     order_id: int
#     price: int
#     size: int
#     user: str
#
#
# class OrderCancel(RWModel):
#     order_id: int
#     market: str
#     price: int
#     size: int
#     user: str
