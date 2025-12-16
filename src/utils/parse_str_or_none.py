def parse_str_or_none(value: str) -> str | None:
    return value if value != "None" else None
