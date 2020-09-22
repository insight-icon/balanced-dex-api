from app import models


# # implement other CRUD - # https://motor.readthedocs.io/en/stable/tutorial-asyncio.html
class CRUDMongo:

    @staticmethod
    async def do_insert(mongo_client, database_name: str, collection_name: str, mongodata: models.MongoData):
        db = mongo_client[database_name]
        collection = db[collection_name]
        result = await collection.insert_one(mongodata.dict())
        return repr(result.inserted_id)

    @staticmethod
    async def do_find_one(mongo_client, database_name: str, collection_name: str, mongodata: models.MongoData):
        db = mongo_client[database_name]
        collection = db[collection_name]
        document = await collection.find_one({"name": mongodata.name})
        return document

    @staticmethod
    async def do_find(mongo_client, database_name: str, collection_name: str, mongodata: models.MongoData):
        db = mongo_client[database_name]
        collection = db[collection_name]
        cursor = collection.find({"name": mongodata.name})
        cursor.limit(10)
        result = []
        async for document in cursor:
            result.append(document)
        return result


mongo = CRUDMongo()
