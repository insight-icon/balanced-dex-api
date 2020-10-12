import pytest
from app.utils.test_utils import get_input_output_file_sets

PATH = 'fixtures/open_orders/'
FIXTURES = get_input_output_file_sets(PATH)


@pytest.mark.asyncio
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
async def test_set_open_order(
        input_file: str,
        expected_file: str,
) -> None:
    pass


@pytest.mark.asyncio
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
async def test_get_open_order_for_order_id(
        input_file: str,
        expected_file: str,
) -> None:
    pass


@pytest.mark.asyncio
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
async def test_get_open_size_for_order_id(
        input_file: str,
        expected_file: str,
) -> None:
    pass


@pytest.mark.asyncio
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
async def test_get_open_side_for_order_id(
        input_file: str,
        expected_file: str,
) -> None:
    pass


@pytest.mark.asyncio
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
async def test_get_cancel_order_id(
        input_file: str,
        expected_file: str,
) -> None:
    pass


@pytest.mark.asyncio
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
async def test_create_order_key(
        input_file: str,
        expected_file: str,
) -> None:
    pass
