import time
from datetime import datetime

import dateparser

# from dateparser import parse


def time_parser(date_time: str) -> int | None:
    date_time = dateparser.parse(
        date_time,
        # settings={'TO_TIMEZONE': 'MSK'}
    )
    timestamp = int(date_time.strftime("%s"))
    return timestamp


def timestamp_to_datetime(timestamp: int) -> str | None:
    time = datetime.fromtimestamp(timestamp)
    return time
    # .strftime('%d.%m.%Y %H:%M')
