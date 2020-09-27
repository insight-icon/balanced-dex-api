import sys

from app.models.kline import KLine

# todo: calculate kline for trade (agg over 1 minute)
class KLineService:

    @staticmethod
    def calculate_kline(input_data: list) -> (float, float, float, float, float):
        _open: float = 0.0
        _high: float = 0.0
        _low: float = sys.float_info.max
        _close: float = 0.0
        _avg: float = 0.0

        if len(input_data) == 0:
            return KLine()  # every value is 0.0

        # todo: remove assumption - list is sorted in ascending order on time
        _open = input_data[0]
        _close = input_data[len(input_data) - 1]

        for i in range(len(input_data)):
            value = input_data[i]

            if value < _low:
                _low = value

            if value > _high:
                _high = value

            _avg = KLineService.__calculate_new_avg(_old_avg=_avg, _count=i + 1, _new_value=value)

        return KLine(open=_open, high=_high, low=_low, close=_close, avg=_avg)

    @staticmethod
    def __calculate_new_avg(_old_avg: float, _count: int, _new_value: float):
        return ((_old_avg * (_count - 1)) + _new_value) / _count
