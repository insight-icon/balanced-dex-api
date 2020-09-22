import json
import time

import asyncio
from typing import Dict

from aiokafka import AIOKafkaProducer
from app.models.orders import OrderCreate, Address
from app.models.rwmodel import RWModel
from fastapi import APIRouter
from loguru import logger
from pydantic.main import BaseModel
from starlette.background import BackgroundTasks

# from ....models.orders import OrderCreate, Address
from ....core.config import settings

router = APIRouter()
eventer: AIOKafkaProducer = None
run: bool = False


def init():
    global eventer, run
    eventer = get_kafka_producer()
    run = False


def get_kafka_producer() -> AIOKafkaProducer:
    loop = asyncio.get_event_loop()
    producer = AIOKafkaProducer(
        loop=loop,
        client_id="eventer-01",
        bootstrap_servers=settings.KAFKA_INTERNAL_HOST_PORT,
        api_version="2.0.1"
    )
    return producer


router.add_event_handler("startup", init)


@router.get("/")
async def index():
    options = dict()
    options["/start"] = "start producing mock events"
    options["/run_once"] = "produce 1 mock event"
    options["/run"] = "produce mock events at regular interval"
    options["/stop"] = "stop producing mock events"
    return options


def create_OrderCreate() -> OrderCreate:
    return OrderCreate(
        order_id=1,
        market="ICX",
        price=90,
        size=17,
        user=Address(address="asdasdas"),
    )

@router.get("/start")
async def start_eventer():
    global eventer
    await eventer.start()
    return "eventer started"


@router.get("/run_once")
async def run_once_eventer():
    global eventer, run
    o = create_OrderCreate()
    sent = await eventer.send(
        "orders",
        value=json.dumps(o.dict()).encode("utf-8")
    )
    result = await sent
    return result


class Item(BaseModel):
    amount: int


@router.post("/run")
async def run_eventer(
        item: Item, background_tasks: BackgroundTasks
) -> Dict[str, str]:
    background_tasks.add_task(background_async, item.amount)
    return {"message": f"producing event every {item.amount} sec"}


@router.get("/stop")
async def stop_eventer():
    global eventer, run
    run = False
    await eventer.stop()
    return "eventer stopped"


async def background_async(amount: int) -> None:
    global eventer, run
    run = True
    try:
        while run:
            o = create_OrderCreate()
            await eventer.send(
                "orders",
                value=json.dumps(o.dict()).encode("utf-8")
            )
            logger.info(f"EVENTER sent :: {o.schema_json()}")

            logger.debug(f"sleeping {amount}s")
            await asyncio.sleep(amount)
            logger.debug(f"slept {amount}s")
    except:
        await stop_eventer()
