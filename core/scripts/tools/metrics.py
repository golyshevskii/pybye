from typing import Any, Dict, List, Optional, Union

import pandas as pd
from core.scripts.tools.logger import get_logger

logger = get_logger(__name__)


def calc_rolling_sr_levels(
    data: pd.DataFrame, window_size: int, sort_by: str = "start_time", ascending: bool = True
) -> pd.DataFrame:
    """
    Calculates support and resistance levels using a rolling window.

    Params:
        data: DataFrame containing the price data.
        window_size: Window size for the rolling window.
        sort_by: Column to sort by.
        ascending: Whether to sort in ascending order.
    """
    data = data.sort_values(by=sort_by, ascending=ascending)

    data["resistance"] = data["close_price"].rolling(window=window_size, min_periods=1).max().shift(1)
    data["support"] = data["close_price"].rolling(window=window_size, min_periods=1).min().shift(1)

    logger.info("Rolling support and resistance levels have been calculated")
    return data


def calc_pivot_sr_levels(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates pivot, support and resistance levels.

    Params:
        data: DataFrame containing the candle data.
    """
    data["pivot"] = (data["high_price"] + data["low_price"] + data["close_price"]) / 3
    data["support"] = (2 * data["pivot"]) - data["high_price"]
    data["support_2"] = data["pivot"] - (data["high_price"] - data["low_price"])
    data["resistance"] = (2 * data["pivot"]) - data["low_price"]
    data["resistance_2"] = data["pivot"] + (data["high_price"] - data["low_price"])

    logger.info("Pivot, support and resistance levels have been calculated")
    return data


def calc_change(
    data: Union[pd.DataFrame, List[Dict[str, Any]]],
    interval: int,
    period: Optional[int] = None,
    round_to: int = 2,
) -> float:
    """
    Calculates the % change between symbol klines.

    Params:
        data: DataFrame or list of dictionaries containing the klines data.
        interval: Interval of the klines data (in minutes).
        period: Lookback period for the change calculation (in minutes).
        round_to: Number of decimal places to round to.
    """
    if period is None:
        if interval == 5:
            period = 60  # 1 hour
        elif interval == 15:
            period = 240  # 4 hours
        elif interval == 60:
            period = 720  # 12 hours
        elif interval == 240:
            period = 5760  # 4 days
        elif interval == 1440:
            period = 10080  # 1 week
        else:
            raise ValueError("Invalid interval. Required: 5, 15, 60, 240, 1440")

    idx = period * 60 // interval

    if isinstance(data, pd.DataFrame):
        return round(
            (float(data["close_price"].iloc[-1]) / float(data["close_price"].iloc[-idx]) - 1) * 100, round_to
        )

    return round((float(data[-1]["close_price"]) / float(data[-idx]["close_price"]) - 1) * 100, round_to)
