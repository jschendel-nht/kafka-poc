import asyncio
from datetime import datetime, timedelta
from pathlib import Path

from rust_fst import Set

from myapp.leveldb import LEVELDB_STATUS, get_sorted_keys

# min time after last leveldb write to rebuild fst
REBUILD_LAG = timedelta(minutes=1)


async def rebuilt_fst():
    while True:
        for field_name, status in LEVELDB_STATUS.items():
            if status["fst_needs_update"] and datetime.now() - status["last_write"] > REBUILD_LAG:
                print(f"Starting FST rebuild for field: {field_name}")
                status["fst_needs_update"] = False
                create_fst_set_from_leveldb(field_name)
                print(f"Completed FST rebuild for field: {field_name}")
        await asyncio.sleep(10)


def create_fst_set_from_leveldb(field_name: str) -> Set:
    it = get_sorted_keys(field_name)
    return Set.from_iter(it, path=f"/fst/{field_name}.fst")


def load_fst_set_from_disk(field_name: str) -> Set:
    fst_path = f"/fst/{field_name}.fst"
    if not Path(fst_path).exists():
        raise ValueError(f"fst does not exist for {field_name}")
    return Set(fst_path)
