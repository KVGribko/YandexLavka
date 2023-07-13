import re
from datetime import time


def hours_validator(working_hours: list[str]):
    r = re.compile(
        "^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]-([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"
    )
    for hour in working_hours:
        if r.fullmatch(hour) is None:
            raise ValueError(f"'{hour}' not match pattern HH:MM")
        start, end = map(time.fromisoformat, hour.split("-"))
        if start >= end:
            raise ValueError(f"start: {start}, must be less than end: {end}.")
    return working_hours
