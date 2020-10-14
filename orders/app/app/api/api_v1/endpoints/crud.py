from aioredis import Redis
from app import models
from app.db.mongodb import get_mongodb_database
from app.db.redis import get_redis_database
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()


@router.post("/mongodb/insert")
async def post(
    mongo_data: models.MongoData,
    db: AsyncIOMotorClient = Depends(get_mongodb_database),
):
    collection = db["database_name"]["collection_name"]
    result = await collection.collection.insert_one(mongo_data.dict())
    return repr(result.inserted_id)


@router.post("/mongodb/findone")
async def post(
    mongo_data: models.MongoData,
    db: AsyncIOMotorClient = Depends(get_mongodb_database),
):
    collection = db["database_name"]["collection_name"]
    result = await collection.collection.find_one({"name": mongo_data.name})
    return repr(result)


# @router.get("/redis/properties")
# async def redis_properties(
#     redis_client: Redis = Depends(get_redis_database),
# ):
#     str = f"initial db - {redis_client.db}"
#     x = await redis_client.select(1)
#     str1 = str + f"changed db  - {x}, now it is {redis_client.db}"
#     return repr(str1)


@router.post("/redis/set")
async def post(
    redis_data: models.RedisData,
    db: Redis = Depends(get_redis_database),
):
    result = await db.set(redis_data.key, redis_data.value)
    return repr(result)


@router.post("/redis/get")
async def post(
    redis_data: models.RedisData,
    db: Redis = Depends(get_redis_database),
):
    result = await db.get(redis_data.key)
    return repr(result)
