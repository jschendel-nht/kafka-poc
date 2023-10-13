from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel
from pydantic.types import PositiveInt

from myapp.fst import load_fst_set_from_disk
from myapp.leveldb import get_ids_for_key

router = APIRouter()


class FuzzySearch(BaseModel):
    field_name: Literal["address", "name"]
    search_target: str
    max_distance: PositiveInt


@router.post("/fuzzy_search")
async def fuzzy_search(data: FuzzySearch):
    data = data.dict()
    fst = load_fst_set_from_disk(data["field_name"])
    matches = fst.search(data["search_target"].lower(), max_dist=data["max_distance"])

    result = []
    for candidate in matches:
        for profile_id in get_ids_for_key(data["field_name"], candidate):
            result.append({"target": data["search_target"], "candidate": candidate, "profile_id": profile_id})

    return result

