from loguru import logger


class CrudRedisGeneral:
    @staticmethod
    async def set(redis_client, key, value):
        return await redis_client.set(key, value)

    @staticmethod
    async def get(redis_client, key):
        return await redis_client.get(key)

    @staticmethod
    async def delete(redis_client, key):
        return await redis_client.delete(key)

    @staticmethod
    async def iscan(redis_client, pattern):
        logger.info(f"crud depth in iscan func, pattern is {pattern}")
        result = []
        async for key in redis_client.iscan(match=pattern):
            result.append(key)
        return result

    @staticmethod
    async def get_key_value_pairs(redis_client, pattern):
        logger.info(f"get_key_value_pairs, pattern is {pattern}")
        keys = await CrudRedisGeneral.iscan(redis_client, pattern)
        result = {}
        if keys is None:
            return result
        for key in keys:
            result[key] = await CrudRedisGeneral.get(redis_client, key)
        return result

    @staticmethod
    async def mget_key_value_pairs(redis_client, keys: list):
        logger.info(f"mget_key_value_pairs func, keys: {keys}")
        result = {}
        if keys is None or len(keys) == 0:
            return result
        for key in keys:
            result[key] = await CrudRedisGeneral.get(redis_client, key)
        return result

    @staticmethod
    async def exists(redis_client, key):
        return await redis_client.exists(key)

    @staticmethod  # todo: remove for prod
    async def cleanup(redis_client, pattern: str):
        keys = await CrudRedisGeneral.iscan(redis_client, pattern)
        for key in keys:
            await CrudRedisGeneral.delete(redis_client, key)
