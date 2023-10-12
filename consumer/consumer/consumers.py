import json
import os

from kafka import KafkaConsumer, KafkaProducer

from consumer.cleaning import clean_raw_value
from consumer.leveldb import write_to_leveldb

def consume_raw():
    print()
    try:
        # To consume latest messages and auto-commit offsets
        consumer = KafkaConsumer(
            "address_raw", "name_raw",
            group_id="group_1",
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
        )
        # consumer.subscribe(pattern=".*_raw$")

        producer = KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            value_serializer=lambda m: json.dumps(m).encode('ascii')
        )

        for message in consumer:
            print("CONSUMING RAW GENERIC: %s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key, message.value))
            
            cleaned_topic = message.topic.replace("_raw", "_clean")
            cleaned_value = clean_raw_value(message.topic, message.value)
            producer.send(cleaned_topic, cleaned_value)

    except Exception as e:
        print('consumer error', e)


def consume_clean():
    try:
        # To consume latest messages and auto-commit offsets
        consumer = KafkaConsumer(
            "address_clean", "name_clean",
            group_id="group_1",
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
        )
        # consumer.subscribe(pattern=".*_clean$")

        for message in consumer:
            print("CONSUMING CLEAN: %s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key, message.value))
            
            table = message.topic.removesuffix("_clean")
            key = message.value[table]
            value = message.value["profile_id"]
            write_to_leveldb(table, key, value)

    except Exception as e:
        print('consumer error', e)
