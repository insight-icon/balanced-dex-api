# import pytest
# from app.tests.test_utils import get_input_output_file_sets
#
# PATH = 'fixtures/redis/'
# FIXTURES = get_input_output_file_sets(PATH)
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("input_file, expected_file", FIXTURES)
# async def test_set(
#         input_file: str,
#         expected_file: str,
# ) -> None:
#     pass
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("input_file, expected_file", FIXTURES)
# async def test_get(
#         input_file: str,
#         expected_file: str,
# ) -> None:
#     pass
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("input_file, expected_file", FIXTURES)
# async def test_delete(
#         input_file: str,
#         expected_file: str,
# ) -> None:
#     pass
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("input_file, expected_file", FIXTURES)
# async def test_iscan(
#         input_file: str,
#         expected_file: str,
# ) -> None:
#     pass
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("input_file, expected_file", FIXTURES)
# async def test_get_key_value_pairs(
#         input_file: str,
#         expected_file: str,
# ) -> None:
#     pass
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("input_file, expected_file", FIXTURES)
# async def test_exists(
#         input_file: str,
#         expected_file: str,
# ) -> None:
#     pass
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize("input_file, expected_file", FIXTURES)
# async def test_cleanup(
#         input_file: str,
#         expected_file: str,
# ) -> None:
#     pass
