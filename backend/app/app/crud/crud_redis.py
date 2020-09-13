from app import schemas


class CRUDRedis:

    @staticmethod
    async def set(redis_client, redis_data: schemas.RedisData):
        return await redis_client.set(redis_data.key, redis_data.value)

    @staticmethod
    async def get(redis_client, redis_key):
        return await redis_client.get(redis_key)


redis = CRUDRedis()
