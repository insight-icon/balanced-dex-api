# import json
# from app.models.orders import OrderCreate
# from app.models.schema_registry import new_schema_registry
# from pydantic import BaseModel
# from app.core.config import settings
# from fastapi.testclient import TestClient
# import http.client
#
#
# def test_get_mode() -> None:
#     conn = http.client.HTTPConnection("127.0.0.1", 8081)
#     conn.request("GET", "/mode")
#     response = conn.getresponse()
#     assert response.status == 200
#
#
# def test_register_schema_registry() -> None:
#     _schema_id = "scv"
#     _id = "scv_id"
#     _description = "Sample schema to help you get started."
#     _key_or_value = "value"
#     _topic = "test7"  # OrderCreate.__name__
#     _cls = OrderCreate
#
#     schema_registry = new_schema_registry(
#         _schema_id=_schema_id,
#         _id=_id,
#         _description=_description,
#         _key_or_value=_key_or_value,
#         _topic=_topic,
#         _cls=_cls
#     )
#
#     req_body = json.dumps(schema_registry)
#
#     conn = http.client.HTTPConnection("127.0.0.1", 8081)
#     conn.request("POST", f"/subjects/{_topic}-{_key_or_value}/versions", req_body)
#     response = conn.getresponse()
#     print(response.read().decode())
#     assert response.status == 200
#
#
# def test_delete_schema_registry_by_subject() -> None:
#     _key_or_value = "value"
#     _topic = "test7"
#
#     conn = http.client.HTTPConnection("127.0.0.1", 8081)
#     conn.request("DELETE", f"/subjects/{_topic}-{_key_or_value}")
#     response = conn.getresponse()
#     response_dict = json.loads(response.read().decode())
#
#     print(f" status:{response.status}")
#     assert response.status == 200 or 404
#     if response.status == 404:
#         # 40404 = for soft deleted subject, 40401 = subject not present
#         error = response_dict["error_code"]
#         print(f"error_code:{error}")
#         assert error == 40404 or 40401
#
