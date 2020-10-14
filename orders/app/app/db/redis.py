from aioredis import Redis


class RedisDataBase:
    client: Redis = None


redis = RedisDataBase()


async def get_redis_database() -> Redis:
    return redis.client
