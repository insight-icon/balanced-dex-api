from app import schemas

# # implement other CRUD - # https://motor.readthedocs.io/en/stable/tutorial-asyncio.html
class CRUDMongo:

    @staticmethod
    async def do_insert(mongo_client, mongodata: schemas.MongoData):
        result = await mongo_client.insight_test.person.insert_one(mongodata.dict())
        return repr(result.inserted_id)

    @staticmethod
    async def do_find_one(mongo_client, mongodata: schemas.MongoData):
        document = await mongo_client.insight_test.person.find_one({"name": mongodata.name})
        return document


mongo = CRUDMongo()
