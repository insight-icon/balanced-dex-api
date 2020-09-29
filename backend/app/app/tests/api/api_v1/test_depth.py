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

    logger.info(f"get_redis_client: {get_redis_client}")
    result = await CrudRedisGeneral.get_key_value_pairs(get_redis_client, "*")
    logger.info(f"result: {result}")
    await CrudRedisGeneral.cleanup(get_redis_client, "*")
    result = await CrudRedisGeneral.get_key_value_pairs(get_redis_client,"*")
    logger.info(f"result, before start of test, redis: {result}")

    if len(input_data) == len(expected_data):
        for i in range(len(input_data)):
            logger.info(f"i::::{i}")
            data = input_data[i]
            body = json.dumps(data)
            conn = client.HTTPConnection("localhost", 80)
            conn.request("POST", "/api/v1/balanced/event", body=body)
            response = conn.getresponse()
            resp_body = response.read().decode(encoding="utf-8")
            logger.info(f"resp_body : {str(resp_body)}")
            assert response.status == 200
            assert resp_body.replace(" ", "") == json.dumps(expected_data[i]).replace(" ", "")

    get_redis_client.close()
    await get_redis_client.wait_closed()
