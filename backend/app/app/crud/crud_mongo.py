from app import schemas

# # implement other CRUD - # https://motor.readthedocs.io/en/stable/tutorial-asyncio.html
class CRUDMongo:

    @staticmethod
    async def do_insert(mongo_client, person: schemas.MongoData):
        document = {
            "name": person.name,
            "phone": person.phone
        }
        result = await mongo_client.insight_test.person.insert_one(document)
        return "result", repr(result.inserted_id)

    @staticmethod
    async def do_find_one(mongo_client, person: schemas.MongoData):
        document = await mongo_client.insight_test.person.find_one({"name": person.name})
        return document


mongo = CRUDMongo()
