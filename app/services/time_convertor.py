import time
import datetime

import dateparser
# from dateparser import parse


def time_parser(date_time: str) -> int | None:
    date_time = dateparser.parse(date_time, settings={'TO_TIMEZONE': 'MSK'})
    timestamp = int(date_time.strftime("%s")) + 3600 * 3
    return timestamp
