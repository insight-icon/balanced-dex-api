from aioredis import Channel, create_connection
from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect
from fastapi.responses import HTMLResponse
from kafka.errors import KafkaConnectionError
from starlette.endpoints import WebSocketEndpoint
import asyncio
from typing import List
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from loguru import logger
import typing
from pydantic import BaseModel
from typing import Optional
import motor.motor_asyncio
import redis
import aioredis
# from starlette.websockets import WebSocketDisconnect
import json
from bson.json_util import dumps

from app import schemas, models, crud
from app.core.config import settings

router = APIRouter()
# app.add_middleware(CORSMiddleware, allow_origins=["*"])

# #################### create clients ####################
manager = None
mongoClient = None
redisClient = None
# pub = None
# sub = None


# @router.on_event("startup")
async def startup():
    global manager, mongoClient, redisClient
    manager = models.ConnectionManager()
    mongoClient = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_HOST, settings.MONGODB_PORT)
    redisClient = await aioredis.create_redis_pool(settings.REDIS_CONNECTION)
    # pub = await aioredis.create_redis(settings.REDIS_CONNECTION)
    # sub = await aioredis.create_redis(settings.REDIS_CONNECTION)


async def shutdown():
    global manager, mongoClient, redisClient
    redisClient.close()
    await redisClient.wait_closed()


asyncio.create_task(startup())


# # ################ web socket chat  ################
@router.get("/")
async def get():
    return HTMLResponse(html)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost/api/v1/dex/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


@router.get("/ws/connections")
async def get_connections():
    x = []
    for conn in manager.active_connections:
        x.append(conn["path"])
    return json.dumps(x)


# ################ kafka topic connected to a web socket  ################

# producer
@router.websocket("/producer/{clientid}/{topicname}")
async def publish(websocket: WebSocket, clientid: str, topicname: str):
    await websocket.accept()

    loop = asyncio.get_event_loop()
    aioproducer = AIOKafkaProducer(
        loop=loop,
        client_id="client"+clientid,
        bootstrap_servers=settings.KAFKA_INTERNAL_HOST_PORT,
        api_version="2.0.1"
    )
    logger.info("aioproducer created")

    try:
        await aioproducer.start()
        while True:
            msg = await websocket.receive_text()
            await aioproducer.send(topicname, json.dumps(msg).encode("ascii"))
            print("published:", msg)
    except WebSocketDisconnect:
        logger.error(WebSocketDisconnect)
    except KafkaConnectionError:
        logger.error(WebSocketDisconnect)
    finally:
        await aioproducer.stop()
        await websocket.close()



# consumer
async def consume(consumer, topicname):
    async for msg in consumer:
        print("for msg in consumer: ", msg)
        return msg.value.decode()


@router.websocket_route("/consumer/{clientid}/{topicname}")
class WebsocketConsumer(WebSocketEndpoint):
    """
    Consume messages from <topicname>
    This will start a Kafka Consumer for a topic
    And this path operation will:
    * return ConsumerResponse
    """

    async def on_connect(self, websocket: WebSocket) -> None:
        logger.debug("Inside on_connect for topic consumption")
        clientid = websocket["path"].split("/")[5]
        logger.debug("clientid:" + clientid)
        topicname = websocket["path"].split("/")[6]  # until I figure out an alternative
        logger.debug("topicname:" + topicname)
        logger.debug("Going to connect to websocket")
        await manager.connect(websocket)
        await manager.broadcast(f"Client connected : {clientid}")
        logger.debug("Connected to websocket")

        loop = asyncio.get_event_loop()
        # loop = asyncio.get_running_loop()
        logger.debug("get_event_loop completed")
        # todo: consumer above cannot start
        self.consumer = AIOKafkaConsumer(
            topicname,
            loop=loop,
            client_id=settings.PROJECT_NAME,
            bootstrap_servers=settings.KAFKA_INTERNAL_HOST_PORT,
            enable_auto_commit=False,
            api_version="2.0.1",  # adding this is necessary
        )
        logger.debug("self.consumer => AIOKafkaConsumer complete")
        # todo: consumer above cannot start
        await self.consumer.start()
        logger.debug("await self.consumer.start() complete")

        self.consumer_task = asyncio.create_task(
            self.send_consumer_message(websocket=websocket, topicname=topicname)
        )
        logger.info("connected")

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        clientid = websocket["path"].split("/")[2]
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{clientid} left")

        self.consumer_task.cancel()
        await self.consumer.stop()
        logger.info(f"counter: {self.counter}")
        logger.info("disconnected")
        logger.info("consumer stopped")

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        clientid = websocket["path"].split("/")[2]
        await manager.send_personal_message(f"You wrote: {data}", websocket)
        await manager.broadcast(f"Client #{clientid} says: {data}")

    async def send_consumer_message(self, websocket: WebSocket, topicname: str) -> None:
        self.counter = 0
        while True:
            data = await consume(self.consumer, topicname)
            # response = ConsumerResponse(topic=topicname, **json.loads(data))
            logger.info(f"data : {data}")
            await manager.send_personal_message(f"{data}", websocket)
            print("websocket.send_text done")
            self.counter = self.counter + 1


# # ################ mongodb  ################

@router.post("/mongo/insert")
async def post(mongo_data: schemas.MongoData):
    return await asyncio.wait_for(crud.mongo.do_insert(mongoClient, 'insight_test', 'person', mongo_data), 3.0)


@router.post("/mongo/find_one")
async def post(mongo_data: schemas.MongoData):
    result = await asyncio.wait_for(crud.mongo.do_find_one(mongoClient, 'insight_test', 'person', mongo_data), 3.0)
    # return {"name": x["name"], "phone": x["phone"]}
    return str(result)


@router.post("/mongo/find")
async def post(mongo_data: schemas.MongoData):
    results = await asyncio.wait_for(crud.mongo.do_find(mongoClient, 'insight_test', 'person', mongo_data), 3.0)
    # return {"name": x["name"], "phone": x["phone"]}
    return str(results)



# ################ redis  ################

@router.post("/redis/set")
async def post(redis_data: schemas.RedisData):
    return await crud.redis.set(redisClient, redis_data)


@router.post("/redis/get")
async def post(redis_data: schemas.RedisData):
    return await crud.redis.get(redisClient, redis_data.key)


# ################## redis pub-sub to scale websocket
@router.websocket("/pub/{clientid}/{topic}")
async def publish(websocket: WebSocket, clientid: int, topic: str):
    await websocket.accept()
    pub = await aioredis.create_redis(settings.REDIS_CONNECTION, db=2)
    try:
        while True:
            data = await websocket.receive_text()
            res = await pub.publish_json(topic, [data])
            print("published:", res)
    except WebSocketDisconnect:
        await websocket.close()
        pub.close()


@router.websocket("/sub/{clientid}/{topic}")
async def subscribe(websocket: WebSocket, clientid: int, topic: str):
    await websocket.accept()
    sub = await aioredis.create_redis(settings.REDIS_CONNECTION, db=2)
    res = await sub.subscribe(topic)
    ch = res[0]
    try:
        while await ch.wait_message():
            msg = await ch.get_json()
            logger.info(f"Got Message: {msg}")
            await websocket.send_text(msg)
    except:
        logger.info(f"WebSocketDisconnect")
        sub.unsubscribe(topic)
        sub.close()
        await websocket.close()

