from typing import Union

import pandas as pd
from config import MEXC_CONFIG_PATH, MEXC_DATA_PATH
from core.scripts.mexc.api import get_kline
from core.scripts.tools.files import read_file
from core.scripts.tools.logger import get_logger
from core.scripts.tools.packers import pack_kline

logger = get_logger(__name__)
MARKET_CONFIG = read_file(f"{MEXC_CONFIG_PATH}market.json", is_json=True)


def import_mexc_kline(
    symbol: str, interval: str, start: str = None, end: str = None, category: str = "futures", csv=False
) -> Union[str, pd.DataFrame]:
    """
    Imports candle stick data from the MEXC API.

    Params:
        symbol: Symbol name. Example: BTC_USDT
        interval: Kline interval.
        start: Datetime from which to start. Format: "YYYY-MM-DD HH:MM:SS"
        end: Datetime until which to end. Format: "YYYY-MM-DD HH:MM:SS"
        category: Product type (spot, linear, inverse).
        csv: Whether to return the data as a CSV file.

    Returns:
        file_name: Name of the file where the data is stored.
        packed_kline: Packed candle stick data.
    """
    logger.debug("BEGIN")

    kline = get_kline(category=category, symbol=symbol, interval=interval, start=start, end=end)

    config = MARKET_CONFIG["kline"]
    packed_kline = pack_kline(
        symbol=symbol, kline=kline["data"], rename_columns=config["columns"], sort=True, timeunit="s"
    )

    if csv:
        file_name = config["file_name"].format(symbol=symbol, category=category, interval=interval)
        packed_kline.to_csv(f"{MEXC_DATA_PATH}kline/{file_name}")

        logger.debug("END")
        return file_name

    logger.debug("END")
    return packed_kline
