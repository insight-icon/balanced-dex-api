from typing import Optional

from .rwmodel import RWModel
from pydantic import BaseModel


class OrderCreate(RWModel):
    order_id: int
    market: str
    price: int
    size: int
    user: str


class OrderRest(RWModel):
    order_id: int
    price: int
    size: int
    user: str


class OrderCancel(RWModel):
    order_id: int
    market: str
    price: int
    size: int
    user: str


class Trade(RWModel):
    market: str
    price: int
    size: int
    maker: str
    maker_order: int
    taker: str
    taker_order: int
