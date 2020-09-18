from .rwmodel import RWModel
from pydantic import BaseModel


class Address(RWModel):
    address: str


class OrderCreate(RWModel):
    order_id: int
    market: str
    price: int
    size: int
    user: Address


class OrderRest(RWModel):
    order_id: int
    price: int
    size: int
    user: Address


class OrderCancel(RWModel):
    order_id: int
    market: str
    price: int
    size: int
    user: Address


class Trade(RWModel):
    market: str
    price: int
    size: int
    maker: Address
    maker_order: int
    taker: Address
    taker_order: int
