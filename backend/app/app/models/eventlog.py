from app.models.rwmodel import RWModel


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
    price: str
    size: str
    user: str

    timestamp: float
