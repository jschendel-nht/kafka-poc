import asyncio
import os
from functools import cache

from aiokafka import AIOKafkaProducer


@cache
def get_kafka_producer():
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    loop = asyncio.get_event_loop()
    return AIOKafkaProducer(loop=loop, bootstrap_servers=bootstrap_servers)
