from typing import Any, Dict, List, Union

import pandas as pd
from tqdm import tqdm

tqdm.pandas()

from core.scripts.tools.logger import get_logger
from core.scripts.tools.metrics import calc_scalp_metrics
from core.scripts.tools.signals import set_scalp_signal

logger = get_logger(__name__)


def pack_data(
    data: List[List[str]], data_columns: List[str], additional_data: Dict[str, Any] = None
) -> pd.DataFrame:
    """
    Packs data into the DataFrame.

    Params:
        data: List of data.
        data_columns: List of column names.
        additional: Additional columns to pass to the DataFrame.
    """
    df = pd.DataFrame(data, columns=data_columns)

    if additional_data is not None:
        for column, value in additional_data.items():
            df[column] = value

    logger.info(f"Data has been packed. Shape: {df.shape}.")
    return df


def pack_kline(
    symbol: str,
    kline: List[Union[Dict[str, Any], List[str]]],
    columns: List[str],
    index_column: str = "Time",
    sort: bool = False,
    asc: bool = True,
) -> pd.DataFrame:
    """
    Packs kline data into the DataFrame with the symbol and start_time index.

    Params:
        symbol: Symbol of the kline.
        kline: List of kline data.
        columns: List of column names.
        sort: Whether to sort the data.
        asc: Whether to sort in ascending order.
    """
    data = pd.DataFrame(kline, columns=columns)

    data["symbol"] = symbol
    data[index_column] = pd.to_numeric(data[index_column], errors="coerce")
    data[index_column] = pd.to_datetime(data[index_column], unit="ms", utc=True)
    data.set_index(index_column, inplace=True)

    if sort:
        data.sort_index(inplace=True, ascending=asc)

    logger.info(f"Kline has been packed. Shape: {data.shape}.")
    return data


def setup_scalp_kline(kline: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Packs kline data with scalping metrics and order points.

    Params:
        kline: DataFrame containing the kline data.
    """
    df = kline.copy()

    df = calc_scalp_metrics(df, **kwargs)
    df["signal"] = df.progress_apply(lambda row: set_scalp_signal(df, row.name, **kwargs), axis=1)

    logger.info(f"Kline has been packed. Shape: {df.shape}.")
    return df
