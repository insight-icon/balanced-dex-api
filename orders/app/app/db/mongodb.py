from motor.motor_asyncio import AsyncIOMotorClient


class MongodbDataBase:
    client: AsyncIOMotorClient = None


mongodb = MongodbDataBase()


async def get_mongodb_database() -> AsyncIOMotorClient:
    return mongodb.client
