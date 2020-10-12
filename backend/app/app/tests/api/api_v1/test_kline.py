from http import client
import json
import os

import pytest
from aioredis import Redis
from app.crud.crud_redis_general import CrudRedisGeneral
from app.services.kline_service import KLineService
from app.utils.file_utils import FileUtils
from app.models.kline import KLine
from app.utils.test_utils import get_input_output_file_sets
from loguru import logger

PATH = 'fixtures/kline/'
FIXTURES = get_input_output_file_sets(PATH)


@pytest.mark.asyncio
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
async def test_kline(
        input_file: str,
        expected_file: str,
        get_redis_client: Redis,
) -> None:
    input_data = FileUtils.load_params_from_json(os.path.join(PATH, input_file))
    expected_data = FileUtils.load_params_from_json(os.path.join(PATH, expected_file))

    await CrudRedisGeneral.cleanup(get_redis_client, "*")
    await KLineService.init_kline(get_redis_client, 60)
    await KLineService.init_kline(get_redis_client, 3600)
    await KLineService.init_kline(get_redis_client, 86400)

    if len(input_data) == len(expected_data):
        for i in range(len(input_data)):
            logger.info(f"input line = {i}")
            logger.info(input_data[i])
            klines = get_results(input_data, i)
            # logger.info(f"klines : {klines}")
            for key, value in klines.items():
                # logger.info(f"KLINE :: key: value is {key}:{value}")
                # below: get value for result key in expected results
                expected_result = expected_data[i][key]
                # logger.info(f"expected_result : {expected_result}")

                for key, value in value.items():
                    logger.info(f"individual kline, key: value is {key}:{value}")
                    if key == "start_timestamp" or "end_timestamp":
                        assert float(value) / float(expected_result[key]) == 1
                    else:
                        assert value == expected_result[key]

    await CrudRedisGeneral.cleanup(get_redis_client, "*")
    await KLineService.init_kline(get_redis_client, 60)
    await KLineService.init_kline(get_redis_client, 3600)
    await KLineService.init_kline(get_redis_client, 86400)

    get_redis_client.close()
    await get_redis_client.wait_closed()


def get_results(input_data, i):
    data = input_data[i]
    body = json.dumps(data)
    conn = client.HTTPConnection("localhost", 80)
    conn.request("POST", "/api/v1/balanced/event", body=body)
    response = conn.getresponse()
    resp_body = str(response.read().decode(encoding="utf-8"))
    resp_dict = json.loads(resp_body)
    # logger.info(f"resp_dict : {resp_dict}")
    assert response.status == 200
    klines = resp_dict["kline"]
    return klines
