from typing import Any, Dict, List, Union

import pandas as pd
from core.scripts.tools.logger import get_logger

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
    index_column: str = "start_time",
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
