import pandas as pd
from core.scripts.tools.logger import get_logger

logger = get_logger(__name__)


def calc_sr_levels(
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

    data["resistance"] = data["high_price"].rolling(window=window_size).max()
    data["support"] = data["low_price"].rolling(window=window_size).min()
    data.dropna(subset=["resistance", "support"], inplace=True)

    logger.info(f"Support and resistance levels have been calculated. Shape: {data.shape}.")
    return data


def calc_psr_levels(data: pd.DataFrame) -> pd.DataFrame:
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
