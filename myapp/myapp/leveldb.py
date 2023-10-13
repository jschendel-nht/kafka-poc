import pickle
from collections import defaultdict
from functools import cache
from typing import Iterator

import plyvel

# tracker for leveldb status used to determine when to build a new FST
LEVELDB_STATUS = defaultdict(dict)


@cache
def get_db(field_name: str) -> plyvel.DB:
    return plyvel.DB(f"/leveldb/{field_name}", create_if_missing=True)


def write_to_leveldb(field_name: str, key: str, value: str):
    db = get_db(field_name)
    key = key.encode()
    if existing := db.get(key):
        value_set = pickle.loads(existing)
        value_set.add(value)
    else:
        value_set = {value}

    db.put(key, pickle.dumps(value_set))


def get_sorted_keys(field_name: str) -> Iterator:
    db = get_db(field_name)
    it = db.iterator(include_value=False)

    # rust-fst expects strings, but then encodes them to bytes - we could subclass and bypass this
    it = map(lambda b: b.decode("utf-8"), it)
    return it


def get_ids_for_key(field_name: str, key: str) -> set[str]:
    db = get_db(field_name)
    values = db.get(key.encode("utf-8"))
    return pickle.loads(values)

