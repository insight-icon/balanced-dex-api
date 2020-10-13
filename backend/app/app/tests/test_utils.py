import os
from os import listdir
from os.path import isfile, join

import pytest
from app.crud.crud_redis_general import CrudRedisGeneral
from app.services.kline_service import KLineService


@pytest.mark.asyncio
async def test_init(monkeypatch, get_redis_client):
    # monkeypatch.chdir(os.path.abspath(os.path.dirname(file_path)))
    # await CrudRedisGeneral.select(get_redis_client, 9)
    await CrudRedisGeneral.cleanup(get_redis_client, "*")
    await KLineService.init_kline(get_redis_client, [60, 3600, 86400])


# def get_input_output_file_sets(dir_path: str,fixtures_condition_map: dict):
def get_input_output_file_sets(dir_path: str):
    # assumption the file naming convention is as follows =>
    # <functionality>-<scenario_name>-<input/output>.json
    # eg - kline-scenario_1-input.json
    scenarios = {}
    for f in listdir(dir_path):
        if isfile(join(dir_path, f)):
            filename_parts = f.split('-')
            if len(filename_parts) == 3:
                key = filename_parts[1]
                i_or_o = filename_parts[2]
                if key not in scenarios:
                    value = []
                    value.insert(__index_to_insert(i_or_o), f)
                    scenarios[key] = value
                else:
                    existing = scenarios.get(key)
                    existing.insert(__index_to_insert(i_or_o), f)

    fixtures = []
    for key in scenarios:
        value = scenarios[key]
        # value.append(fixtures_condition_map.get(key))
        fixtures.append(tuple(value))

    return fixtures


def __index_to_insert(i_or_o: str):
    if i_or_o == "input.json":
        return 0
    elif i_or_o == "output.json":
        return 1
