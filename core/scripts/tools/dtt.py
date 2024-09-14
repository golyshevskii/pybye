from datetime import datetime
from typing import Union


def to_unix(dtt: Union[datetime, str]) -> int:
    """
    Converts datetime to Unix timestamp.

    Params:
        dtt: Datetime to convert. Format: "YYYY-MM-DD HH:MM:SS"
    """
    if isinstance(dtt, datetime):
        return int(dtt.timestamp())
    return int(datetime.strptime(dtt, "%Y-%m-%d %H:%M:%S").timestamp())
