from app import schemas


class CRUDRedis:

    @staticmethod
    def set(redis_client, redis_data: schemas.RedisData):
        return redis_client.set(redis_data.key, redis_data.value)

    @staticmethod
    def get(redis_client, redis_key):
        return redis_client.get(redis_key)


redis = CRUDRedis()
