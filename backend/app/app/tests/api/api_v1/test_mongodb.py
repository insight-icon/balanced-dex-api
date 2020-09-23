from app.core.config import settings


# def test_mongodb_insert(test_client, test_user):
#     response = test_client.post(f"{settings.API_V1_STR}/dex/mongo/insert", json="test_user")
#     assert response.status_code == 201
#     assert response.json()["user"]["username"] == test_user["user"]["username"]
