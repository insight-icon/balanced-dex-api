from app.models.rwmodel import RWModel


class OpenOrder(RWModel):
    side: int
    size: float

