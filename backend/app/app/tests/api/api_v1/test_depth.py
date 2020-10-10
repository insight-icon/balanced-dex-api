from http import client
import json
import os

from aioredis import Redis
from app.crud.crud_redis_general import CrudRedisGeneral
from app.utils.file_utils import FileUtils
from loguru import logger
import pytest
from app.core.config import settings
from app.utils.test_utils import get_input_output_file_sets

PATH = 'fixtures/depth/'
FIXTURES = get_input_output_file_sets(PATH)


@pytest.mark.asyncio
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
async def test_depth(
        input_file: str,
        expected_file: str,
        get_redis_client: Redis,
) -> None:
    input_data = FileUtils.load_params_from_json(os.path.join(PATH, input_file))
    expected_data = FileUtils.load_params_from_json(os.path.join(PATH, expected_file))

    await CrudRedisGeneral.cleanup(get_redis_client, "*")

    if len(input_data) == len(expected_data):
        for i in range(len(input_data)):
            logger.info(f"input line = {i}")
            depth = get_results(input_data, i)
            logger.info(f"depth : {depth}")
            for key, value in depth.items():
                logger.info(f"key, value - {key} and {value}")
                # below: get value for result key in expected results
                expected_result = expected_data[i][key]
                logger.info(f"expected_result : {expected_result}")

                assert value == expected_result

    await CrudRedisGeneral.cleanup(get_redis_client, "*")
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
    logger.info(f"resp_dict : {resp_dict}")
    assert response.status == 200
    depth = resp_dict["depth"]
    return depth
