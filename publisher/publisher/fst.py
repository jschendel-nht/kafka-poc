from pathlib import Path

from rust_fst import Set

from publisher.leveldb import get_sorted_keys


def create_set_from_table(table: str) -> Set:
    it = get_sorted_keys(table)
    return Set.from_iter(it, path=f"/fst/{table}.fst")


def load_set_from_table(table: str) -> Set:
    fst_path = f"/fst/{table}.fst"
    if not Path(fst_path).exists():
        raise ValueError(f"fst does not exist for {table}")
    return Set(fst_path)
