from http import client
import json
import os

from aioredis import Redis
from app.crud.crud_redis_general import CrudRedisGeneral
from app.services.kline_service import KLineService
from app.utils.file_utils import FileUtils
from loguru import logger
import pytest
from app.tests.test_utils import get_input_output_file_sets, test_init

PATH = 'fixtures/depth/'
FIXTURES = get_input_output_file_sets(PATH)

@pytest.mark.asyncio
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
async def test_depth(
        monkeypatch,
        input_file: str,
        expected_file: str,
        get_redis_client: Redis,
) -> None:

    await test_init(monkeypatch, get_redis_client, __file__)
    input_data = FileUtils.load_params_from_json(os.path.join(PATH, input_file))
    expected_data = FileUtils.load_params_from_json(os.path.join(PATH, expected_file))

    if len(input_data) == len(expected_data):
        for i in range(len(input_data)):
            # logger.info(f"input line = {i}, and input_data[i]= {input_data[i]}")
            depth = get_results(input_data, i)
            # logger.info(f"depth : {depth}")
            for key, value in depth.items():
                # logger.info(f"key, value - {key} and {value}")
                # below: get value for result key in expected results
                expected_result = expected_data[i][key]
                logger.info(f"expected_result : {expected_result}")

                assert value == expected_result

    await CrudRedisGeneral.cleanup(get_redis_client, "*")
    await KLineService.init_kline(get_redis_client, [60, 3600, 86400])
    get_redis_client.close()
    await get_redis_client.wait_closed()


def get_results(input_data, i):
    data = input_data[i]
    # logger.info(f"in get_results, data = {data}")
    body = json.dumps(data)
    # logger.info(f"in get_results, body = {body}")
    conn = client.HTTPConnection("localhost", 80)
    conn.request("POST", "/api/v1/balanced/event", body=body)
    response = conn.getresponse()
    resp_body = str(response.read().decode(encoding="utf-8"))
    # logger.info(f"in get_results, resp_body = {resp_body}")
    resp_dict = json.loads(resp_body)
    # logger.info(f"resp_dict : {resp_dict}")
    assert response.status == 200
    depth = resp_dict["depth"]
    return depth

