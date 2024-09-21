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

    logger.info(f"Support and resistance levels have been calculated. Shape: {data.shape}.")
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

    return data
