import json
from typing import Dict

import asyncio
from fastapi import FastAPI
from aiokafka import AIOKafkaProducer

app = FastAPI()


loop = asyncio.get_event_loop()
producer = AIOKafkaProducer(
    loop=loop, bootstrap_servers="localhost:9092"
)


@app.on_event("startup")
async def startup_event():
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()


@app.post("/payment")
async def perform_payment(payment_parameters: Dict[str, str]):
    topicname = "payments"

    await producer.send(topicname, json.dumps(payment_parameters).encode("ascii"))

    response = {"message": "payment event created"}

    return response
