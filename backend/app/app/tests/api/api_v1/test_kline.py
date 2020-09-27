import os

import pytest
from app.utils.file_utils import FileUtils
from app.models.kline import KLine
from app.utils.test_utils import get_input_output_file_sets


PATH = 'fixtures/kline/scenarios/'
# FIXTURES_CONDITIONS = {
#     "scenario_1": True,
#     "scenario_2": False
# }

FIXTURES = get_input_output_file_sets(PATH, {})  # , FIXTURES_CONDITIONS)


# @pytest.mark.parametrize("input_file, expected_file, to_check", FIXTURES)
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
def test_kline_moving_avg(
        input_file: str,
        expected_file: str,
        # to_check: bool,

        kline: KLine,
) -> None:
    input_data = FileUtils.load_params_from_json(os.path.join(PATH, input_file))
    expected_data = FileUtils.load_params_from_json(os.path.join(PATH, expected_file))

    if len(input_data) == len(expected_data):
        for i in range(len(input_data)):
            # print(f"i: {i}, to_check: {to_check}")
            print(f"i: {i}")

            kline.avg = KLine.calculate_new_avg(
                kline.avg,
                input_data[i]["order_id"],
                input_data[i]["price"]
            )
            assert kline.avg == expected_data[i]["avg"]

