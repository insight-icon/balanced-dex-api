###############################################################################################################
############################################ To read and implement ############################################

# Background tasks are run after the response is sent (https://fastapi.tiangolo.com/tutorial/background-tasks/)

# motor for async connection to MongoDB (https://motor.readthedocs.io/en/stable/tutorial-asyncio.html

###############################################################################################################
###############################################################################################################

from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


import asyncio
# import json
import typing

from aiokafka import AIOKafkaConsumer
# # from app.core.config import KAFKA_INSTANCE
# # from app.core.config import PROJECT_NAME
# # from app.core.models.model import ConsumerResponse
from fastapi import FastAPI
from fastapi import WebSocket
from loguru import logger
from starlette.endpoints import WebSocketEndpoint
from starlette.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import Optional
# from pydantic import confloat
# from pydantic import StrictStr

KAFKA_INSTANCE = "kafka:9092"
PROJECT_NAME = "insight_tester"
app = FastAPI(title=PROJECT_NAME)
app.add_middleware(CORSMiddleware, allow_origins=["*"])


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
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
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


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        print("send_personal_message: "+ message)
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        print("broadcast:", message)
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/ping")
def get():
    return {"ping": "pong"}

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/connections")
async def get():
    return len(manager.active_connections)

@app.websocket("/ws/{client_id}")
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

# ################ kafka topic consumption ################


async def consume(consumer, topicname):
    async for msg in consumer:
        print("for msg in consumer: ", msg)
        return msg.value.decode()

@app.websocket_route("/consumer/{clientid}/{topicname}")
class WebsocketConsumer(WebSocketEndpoint):
    """
    Consume messages from <topicname>
    This will start a Kafka Consumer for a topic
    And this path operation will:
    * return ConsumerResponse
    """

    async def on_connect(self, websocket: WebSocket) -> None:
        topicname = websocket["path"].split("/")[3]  # until I figure out an alternative
        clientid = websocket["path"].split("/")[2]
        
        await manager.connect(websocket)
        await manager.broadcast(f"Client connected : {clientid}")

        loop = asyncio.get_event_loop()
        self.consumer = AIOKafkaConsumer(
            topicname,
            loop=loop,
            client_id=PROJECT_NAME,
            bootstrap_servers=KAFKA_INSTANCE,
            enable_auto_commit=False,
        )

        await self.consumer.start()

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

# ######################## end of kafka topic consumption ########################

# ################ mongo db  ################
import motor.motor_asyncio
import pymongo 
import urllib.parse 
import json

# mongo_uri = "mongodb+srv://anuragjha:" + urllib.parse.quote("Blue@0520") + "@cluster0.7ogsb.mongodb.net/insight_test?retryWrites=true&w=majority"
# client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb', 27017)


class Person(BaseModel):
    name: str
    phone: Optional[str] = None

# https://motor.readthedocs.io/en/stable/tutorial-asyncio.html
async def do_insert(person: Person):
    document = {
        "name": person.name,
        "phone": person.phone
    }
    result = await client.insight_test.person.insert_one(document)
    return("result",repr(result.inserted_id))
    
@app.post("/mongo/insert")
async def post(person: Person):
    return await asyncio.wait_for(do_insert(person), 3.0)

async def do_find_one(person: Person):
    document = await client.insight_test.person.find_one({"name":person.name})
    return document

@app.post("/mongo/find_one")
async def post(person: Person): 
    x = await asyncio.wait_for(do_find_one(person), 3.0)
    return {"name":x["name"], "phone":x["phone"]}

@app.post("/mongo/find")
async def post(person: Person):
    return await do_insert(person)
    # x = asyncio.create_task(await do_insert(person))    

# # implement orther CRUD - # https://motor.readthedocs.io/en/stable/tutorial-asyncio.html
# ######################## end of mongo db ########################

# ################ redis connection ################
import redis

class RedisData(BaseModel):
    key: str
    value: Optional[str] = None

# redisClient = redis.Redis(host='default', port=6379, db=0)

redisClient = redis.Redis(host='redis', port=6379, db=0)
@app.post("/redis/set")
async def post(redis_data: RedisData):
    return redisClient.set(redis_data.key, redis_data.value)


@app.post("/redis/get")
async def post(redis_data: RedisData):
    return redisClient.get(redis_data.key)