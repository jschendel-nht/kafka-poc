import json
from functools import reduce

from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends

from publisher.dependencies import get_kafka_producer
from publisher.models import Address, Name
from publisher.fst import create_set_from_table, load_set_from_table
from publisher.leveldb import get_ids_for_key

router = APIRouter()


@router.post("/add_address")
async def add_address(data: Address, kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer)):
    try:
        topic_name = "address_raw"
        await kafka_producer.send_and_wait(topic_name, json.dumps(data.dict()).encode("ascii"))
    except Exception as e:
        await kafka_producer.stop()
        raise e
    return 'Message sent successfully'


@router.post("/add_name")
async def add_name(data: Name, kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer)):
    try:
        topic_name = "name_raw"
        await kafka_producer.send_and_wait(topic_name, json.dumps(data.dict()).encode("ascii"))
    except Exception as e:
        await kafka_producer.stop()
        raise e
    return 'Message sent successfully'


@router.post("/create_fst")
async def create_fst(table: str):
    create_set_from_table(table)
    return 'Message sent successfully'


@router.post("/search_name")
async def fuzzy_search_name(name: str):
    fst = load_set_from_table("name")
    names_matches = fst.search(name, max_dist=2)
    profile_id_matches = (get_ids_for_key("name", name) for name in names_matches)
    return list(reduce(set.union, profile_id_matches, set()))

