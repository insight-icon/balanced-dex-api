import pytest
from app.core.file_utils import FileUtils
from app.models.kline import KLine


output_from_test_data = FileUtils.load_params_from_json('fixtures/test-data-output-kline_1.json')


def test_kline(
        kline: KLine,
        input_from_test_data: dict,
        # output_from_test_data: dict
) -> None:
    print("input_from_test_data:", input_from_test_data)
    # print("output_from_test_data:", output_from_test_data)

    kline.avg = KLine.calculate_new_avg(
        kline.avg,
        input_from_test_data["order_id"],
        input_from_test_data["price"]
    )

    count = input_from_test_data["order_id"]-1
    assert kline.avg == output_from_test_data[count]["avg"]
