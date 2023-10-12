import pickle
from typing import Iterator

import plyvel


def get_sorted_keys(table: str) -> Iterator:
    db = plyvel.DB(f"/leveldb/{table}")
    it = db.iterator(include_value=False)

    # rust-fst expects strings, but then encodes them to bytes - we could subclass and bypass this
    it = map(lambda b: b.decode("utf-8"), it)
    return it


def get_ids_for_key(table: str, key: str) -> set[str]:
    db = plyvel.DB(f"/leveldb/{table}")
    values = db.get(key.encode("utf-8"))
    return pickle.loads(values)

