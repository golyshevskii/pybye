from typing import Union
from scripts.bybit.api import get_kline
from scripts.tools.logger import logger
from scripts.tools.files import read_file

CONFIG = read_file("configs/bybit/config.json", is_json=True)


def import_bybit_kline(symbol: str, interval: str, start: Union[str, int], end: Union[str, int], category: str = "spot") -> None:
    """
    Imports candle stick data from the Bybit API.
    
    Params:
        symbol: Symbol name. Example: BTCUSDT
        interval: Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W
        start: Datetime from which to start. Format: "YYYY-MM-DD HH:MM:SS"
        end: Datetime until which to end. Format: "YYYY-MM-DD HH:MM:SS"
        category: Product type (spot, linear, inverse).
    """
    logger.info("BEGIN")

    data = get_kline(category=category, symbol=symbol, interval=interval, start=start, end=end)
    
    config = CONFIG["kline"]

    logger.info("END")
