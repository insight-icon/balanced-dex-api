from datetime import datetime

from app.models.rwmodel import RWModel
from pydantic.schema import time


class KLine(RWModel):
    open: float = 0
    high: float = 0
    low: float = 0
    close: float = 0
    volume: float = 0

    interval_seconds: int
    start_timestamp: float
    end_timestamp: float = 0.0
