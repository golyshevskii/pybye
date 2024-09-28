INTERVALS = {"D": 14400, "W": 100800, "M": 432000}


def to_min_interval(interval: str) -> int:
    """
    Converts a Bybit interval to a minute interval.

    Params:
        interval: Bybit interval.
    """
    try:
        return INTERVALS[interval]
    except KeyError:
        return int(interval)
