from datetime import datetime
from typing import Union


def to_unix(dtt: Union[datetime, str], format: str = "%Y-%m-%d %H:%M:%S") -> int:
    """
    Converts datetime to Unix timestamp.

    Params:
        dtt: Datetime to convert.
        format: Datetime format if dtt is a string.
    """
    if isinstance(dtt, datetime):
        return int(dtt.timestamp())
    return int(datetime.strptime(dtt, format).timestamp())


def to_format(dtt: str, format: str, new_format: str) -> str:
    """
    Returns the datetime in the specified format.

    Params:
        dtt: Datetime to convert.
        format: Datetime format.
        new_format: New datetime format.
    """
    dt = datetime.strptime(dtt, format)
    return dt.strftime(new_format)
