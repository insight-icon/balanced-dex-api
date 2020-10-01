import json
import sys
import time
from typing import Union

from app.crud.crud_redis_general import CrudRedisGeneral
from app.crud.crud_redis_kline import CrudRedisKLine
from loguru import logger

from app.models import EventLog, TradeLog
from app.models.kline import KLine


# todo: calculate kline for trade (agg over 1 minute)
class KLineService:

    @staticmethod
    async def init_kline(redis_client, interval_seconds: int):
        kline_key_latest = CrudRedisKLine.create_kline_key(interval_seconds, "latest")
        await CrudRedisGeneral.set(redis_client, kline_key_latest, "")

    @staticmethod
    async def update_kline(redis_client, _event_or_trade: Union[EventLog, TradeLog]) -> dict:
        if type(_event_or_trade) == TradeLog:
            logger.info("!! === update kline === !!")
            await KLineService._update_kline_for_trade(redis_client, _event_or_trade)

        return {}

    @staticmethod
    async def _update_kline_for_trade(redis_client, _trade: TradeLog):
        results = await CrudRedisGeneral.get_key_value_pairs(redis_client, "kline*latest")
        for key, value in results.items():
            # current_time_micro_secs = (time.time()) * (10**6)
            # logger.info(f"current time is - {current_time_micro_secs}")
            kline_latest_key = key.decode("utf-8")
            kline_latest_key_interval_seconds = CrudRedisKLine.get_interval_from_kline_latest_key(kline_latest_key)
            kline_latest_value = value.decode("utf-8")
            logger.info(f"result is {kline_latest_key}, {kline_latest_value} and interval is {kline_latest_key_interval_seconds}")

            if kline_latest_value == "":
                logger.info(f"kline_latest_value == ")
                kline = await KLineService._create_new_kline(kline_latest_key_interval_seconds, _trade)
                await CrudRedisKLine.set_kline(redis_client, key, kline.dict())
            else:
                logger.info(f"else of kline_latest_value == ")
                kline = json.loads(kline_latest_value)
                kline_start_timestamp = kline["start_timestamp"]
                trade_timestamp = _trade.timestamp

                logger.info(f"{(trade_timestamp - kline_start_timestamp)} <= {kline_latest_key_interval_seconds * (10 ** 6)} : "
                            f"{(trade_timestamp - kline_start_timestamp) <= kline_latest_key_interval_seconds * (10 ** 6)}")

                if (trade_timestamp - kline_start_timestamp) <= kline_latest_key_interval_seconds * (10 ** 6):
                    # continue kline
                    logger.info("# continue kline")
                    await KLineService._update_kline(kline, _trade)
                    await CrudRedisKLine.set_kline(redis_client, key, kline)
                else:
                    logger.info("# store existing kline and create new kline")
                    kline_key = CrudRedisKLine.create_kline_key(kline_latest_key_interval_seconds, int(kline_start_timestamp))
                    logger.info(f"kline_start_timestamp: {kline_start_timestamp}, kline_key: {kline_key}, and kline: {kline}")
                    await CrudRedisKLine.set_kline(redis_client, kline_key, kline)

                    new_kline = await KLineService._create_new_kline(kline_latest_key_interval_seconds, _trade)
                    await CrudRedisKLine.set_kline(redis_client, key, new_kline.dict())

    @staticmethod
    async def _create_new_kline(interval_seconds: float, trade: TradeLog) -> KLine:
        return KLine(
            open=trade.price,
            high=trade.price,
            low=trade.price,
            close=trade.price,
            volume=trade.size,
            interval_seconds=interval_seconds,
            start_timestamp=trade.timestamp,
            end_timestamp=trade.timestamp
        )

    @staticmethod
    async def _update_kline(kline: dict, trade: TradeLog):
        # open
        # high
        price = float(trade.price)
        size = float(trade.size)
        if price > kline["high"]:
            kline["high"] = price
        # low
        if price < kline["low"]:
            kline["low"] = price
        # close
        kline["close"] = price
        # vol
        kline["volume"] = kline["volume"] + size
        # interval
        # start_timestamp
        # end_timestamp
        kline["end_timestamp"] = trade.timestamp


