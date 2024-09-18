from datetime import datetime, timezone
from typing import Union

DTT_FORMAT = "%Y-%m-%d %H:%M:%S"
CSV_DTT_FORMAT = "%Y-%m-%dT%H-%M-%S"


def to_unix(dtt: Union[datetime, str], format: str = DTT_FORMAT, tz: timezone = timezone.utc) -> int:
    """
    Converts datetime to Unix timestamp.

    Params:
        dtt: Datetime to convert.
        format: Datetime format if dtt is a string.
        tz: Timezone. Default is UTC.
    """
    if isinstance(dtt, datetime):
        return int(dtt.astimezone(tz).timestamp())
    return int(datetime.strptime(dtt, format).astimezone(tz).timestamp())


def from_unix(unix: int, format: str = DTT_FORMAT, tz: timezone = timezone.utc, unit: str = "ms") -> datetime:
    """
    Converts Unix timestamp to datetime.

    Params:
        unix: Unix timestamp.
        format: Datetime format.
        tz: Timezone. Default is UTC.
        unit: Timestamp unit. Default is seconds.
    """
    dev = 1000 if unit == "ms" else 1
    return datetime.fromtimestamp(unix / dev, tz=tz).strftime(format)


def to_new_format(dtt: str, format: str, new_format: str) -> str:
    """
    Returns the datetime in the specified format.

    Params:
        dtt: Datetime to convert.
        format: Datetime format.
        new_format: New datetime format.
    """
    dt = datetime.strptime(dtt, format)
    return dt.strftime(new_format)
