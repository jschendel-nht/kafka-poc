import json
import os

from kafka import KafkaConsumer, KafkaProducer

from myapp_etl.cleaning import clean_address, clean_name


def consume_address():
    print("Running Address Consumer")
    consumer = _make_kafka_consumer("postgres.member.address")
    producer = _make_kafka_producer()
    for message in consumer:
        raw_address = message.value['payload']['after']
        # print(f"Consuming Address: {raw_address}")
        cleaned_address = clean_address(raw_address)
        value = {"profile_id": raw_address["profile_id"], "field_name": "address", "field_value":cleaned_address}
        producer.send("myapp.fields", value)


def consume_name():
    print("Running Name Consumer")
    consumer = _make_kafka_consumer("postgres.member.name")
    producer = _make_kafka_producer()
    for message in consumer:
        raw_name = message.value['payload']['after']
        # print(f"Consuming Name: {raw_name}")
        cleaned_name = clean_name(raw_name)
        value = {"profile_id": raw_name["profile_id"], "field_name": "name", "field_value": cleaned_name}
        producer.send("myapp.fields", value)


def _make_kafka_consumer(*topics: str) -> KafkaConsumer:
        consumer = KafkaConsumer(
            *topics,
            group_id="myapp_etl",
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
        )
        return consumer

def _make_kafka_producer() -> KafkaProducer:
        producer = KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            value_serializer=lambda m: json.dumps(m).encode('ascii')
        )
        return producer
