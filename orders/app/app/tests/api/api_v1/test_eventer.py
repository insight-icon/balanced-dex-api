# import json
#
# import pytest
# from aiokafka import AIOKafkaProducer
# from app.core.config import settings
# from app.models import EventLog
# from starlette.testclient import TestClient
# from app.main import app
#
#
# def test_eventer_start(
#         client: TestClient,
#         order_create: EventLog,
# ) -> None:
#     response = client.get(f"{settings.API_V1_STR}/eventer/start")
#     assert response.status_code == 200
#
#
# @pytest.mark.asyncio
# async def test_eventer(
#         # client: TestClient,
#         order_create: EventLog,
#         kafka_producer: AIOKafkaProducer
# ) -> None:
#     import asyncio
#     try:
#         await kafka_producer.start()
#         x = order_create.schema_json()
#         await kafka_producer.send(
#             "orders",
#             value=json.dumps(order_create.dict()).encode("utf-8")
#         )
#     finally:
#         await kafka_producer.stop()
#     assert 1 == 1
#
# # @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 44)])
# # def test_eval(test_input, expected):
# #     assert eval(test_input) == expected
#
#
# # def test_test(
# #         client: TestClient
# # ) -> None:
# #     response = client.get(f"{settings.API_V1_STR}/dex/")
# #     assert response.status_code == 200
