import pandas as pd
from core.scripts.tools.logger import get_logger

logger = get_logger(__name__)


def calc_sr_levels(data: pd.DataFrame, window_size: int) -> pd.DataFrame:
    """
    Calculates support and resistance levels using a rolling window.

    Params:
        data: DataFrame containing the price data.
        window_size: Window size for the rolling window.
    """
    data["resistance"] = data["high_price"].rolling(window=window_size).max()
    data["support"] = data["low_price"].rolling(window=window_size).min()
    data.dropna(subset=["resistance", "support"], inplace=True)

    logger.info(f"Support and resistance levels have been calculated. Shape: {data.shape}.")
    return data
