import json
import os
from datetime import datetime

from aiokafka import AIOKafkaConsumer

from myapp.leveldb import LEVELDB_STATUS, write_to_leveldb

# cache for consumers so we don't rebuild them and can stop them appropriately at exit
CONSUMERS = {}

async def consume_fields():
    print("Starting Fields Consumer")
    consumer = await _make_consumer("myapp.fields")
    async for msg in consumer:
        data = json.loads(msg.value)
        # print(f"Consuming Field: {data}")
        write_to_leveldb(data["field_name"], data["field_value"], data["profile_id"])
        LEVELDB_STATUS[data["field_name"]]["last_write"] = datetime.now()
        LEVELDB_STATUS[data["field_name"]]["fst_needs_update"] = True


async def _make_consumer(*topics):
    if topics in CONSUMERS:
        return CONSUMERS[topics]

    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    consumer = AIOKafkaConsumer(*topics, group_id="myapp_core", bootstrap_servers=bootstrap_servers)

    await consumer.start()
    CONSUMERS[topics] = consumer

    return consumer
