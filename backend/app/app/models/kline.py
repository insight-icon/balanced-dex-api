from app.models.rwmodel import RWModel


class KLine(RWModel):
    open: float = 0
    high: float = 0
    low: float = 0
    close: float = 0
    avg: float = 0
