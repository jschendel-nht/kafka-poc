import pickle

import plyvel

def write_to_leveldb(table: str, key: str, value: str):
    db = plyvel.DB(f"/leveldb/{table}", create_if_missing=True)

    key = key.encode()
    if existing := db.get(key):
        value_set = pickle.loads(existing)
        value_set.add(value)
    else:
        value_set = {value}

    db.put(key, pickle.dumps(value_set))
