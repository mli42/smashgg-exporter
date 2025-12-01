import datetime


def get_date_timestamp(date: str) -> int:
    return int(
        datetime.datetime
        .strptime(date, "%d/%m/%Y")
        .replace(tzinfo=datetime.timezone.utc)
        .timestamp()
    )
