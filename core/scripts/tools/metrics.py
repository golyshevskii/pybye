from typing import Optional

import pandas as pd
from core.scripts.tools.logger import GREEN, RED, RESET, get_logger

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
    data: pd.Series, interval: int, symbol: str = None, lookback: Optional[int] = None, round_to: int = 3
) -> float:
    """
    Calculates the % change between symbol klines.

    Params:
        data: DataFrame or list of dictionaries containing the klines data.
        interval: Interval of the klines data (in minutes).
        lookback: Lookback period for the change calculation (in hours).
        round_to: Number of decimal places to round to.
    """
    if lookback is None:
        if interval == 5:
            lookback = 1
        elif interval == 15:
            lookback = 4
        elif interval == 60:
            lookback = 16
        elif interval == 240:
            lookback = 64
        else:
            raise ValueError("Invalid interval. Required: 5, 15, 60, 240")

    idx = lookback * 60 // interval
    change = round((float(data.iloc[0]) / float(data.iloc[idx]) - 1) * 100, round_to)

    color = GREEN if change > 0 else RED
    logger.info(f"{symbol}: {color}{change}{RESET}%")
    return change


def calc_sma(data: pd.Series, window_size: int) -> Optional[float]:
    """
    Calculates the simple moving average.

    Params:
        data: DataFrame or Series containing the price data.
        window_size: Window size for the moving average.
    """
    if len(data) < window_size:
        logger.warning(f"Not enough data to calculate SMA. Required: {window_size}")
        return

    return data.rolling(window=window_size).mean().iloc[-1]
