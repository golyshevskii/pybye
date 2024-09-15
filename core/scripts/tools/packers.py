from typing import Any, Dict, List

import pandas as pd
from core.scripts.tools.logger import get_logger

logger = get_logger(__name__)


def pack_data(
    data: List[List[str]], data_columns: List[str], additional_data: Dict[str, Any]
) -> pd.DataFrame:
    """
    Packs data into the DataFrame.

    Params:
        data: List of data.
        data_columns: List of column names.
        additional: Additional columns to pass to the DataFrame.
    """
    df = pd.DataFrame(data, columns=data_columns)

    for column, value in additional_data.items():
        df[column] = value

    logger.info(f"Data has been packed. Shape: {df.shape}.")
    return df
