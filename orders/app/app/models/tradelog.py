from app.models.rwmodel import RWModel


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

    timestamp: float
