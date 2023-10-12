def clean_raw_value(topic: str, raw_value: dict) -> str:
    cleaning_lookup = {"address_raw": clean_address, "name_raw": clean_name}
    if topic not in cleaning_lookup:
        raise ValueError(f"Unknown raw topic: {topic}")
    return cleaning_lookup[topic](raw_value)


def clean_address(raw_address: dict) -> str:
    address_order = ("address_line_1", "address_line_2", "city", "state", "zip")
    address_components = (raw_address[field].strip().lower() for field in address_order if raw_address.get(field))
    cleaned_address = " ".join(address_components)
    return {"profile_id": raw_address["profile_id"], "address": cleaned_address}

def clean_name(raw_name: dict) -> str:
    cleaned_name = " ".join(raw_name[field].strip().lower() for field in ("first_name", "last_name"))
    return {"profile_id": raw_name["profile_id"], "name": cleaned_name}
