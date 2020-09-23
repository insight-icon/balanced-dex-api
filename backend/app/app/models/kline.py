from app.models.rwmodel import RWModel


class KLine(RWModel):
    open: float = 0
    high: float = 0
    low: float = 0
    close: float = 0
    avg: float = 0

    @staticmethod
    def calculate_new_avg(_old_avg: float, _count: int, _new_value: float):
        return ((_old_avg * (_count - 1)) + _new_value) / _count
