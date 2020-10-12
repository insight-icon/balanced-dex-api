import pytest
from app.utils.test_utils import get_input_output_file_sets

PATH = 'fixtures/kline/'
FIXTURES = get_input_output_file_sets(PATH)


@pytest.mark.asyncio
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
async def test_set_kline(
        input_file: str,
        expected_file: str,
) -> None:
    pass


@pytest.mark.asyncio
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
async def test_get_kline(
        input_file: str,
        expected_file: str,
) -> None:
    pass


@pytest.mark.asyncio
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
async def test_create_kline(
        input_file: str,
        expected_file: str,
) -> None:
    pass


@pytest.mark.asyncio
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
async def test_get_interval_from_kline(
        input_file: str,
        expected_file: str,
) -> None:
    pass


@pytest.mark.asyncio
@pytest.mark.parametrize("input_file, expected_file", FIXTURES)
async def test_latest_key(
        input_file: str,
        expected_file: str,
) -> None:
    pass
