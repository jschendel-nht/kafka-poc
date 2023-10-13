def clean_address(raw_address: dict) -> str:
    address_order = ("address_line_1", "address_line_2", "city", "state", "zip_code")
    address_components = (raw_address[field].strip().lower() for field in address_order if raw_address.get(field))
    return " ".join(address_components)


def clean_name(raw_name: dict) -> str:
    return " ".join(raw_name[field].strip().lower() for field in ("first_name", "last_name"))
