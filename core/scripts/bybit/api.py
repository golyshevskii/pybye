from typing import Any, Dict

from config import BYBIT_API_KEY, BYBIT_API_SECRET
from pybit.unified_trading import HTTP
from scripts.tools.dtt import to_unix
from scripts.tools.logger import logger

session = HTTP(api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET)


def get_kline(category: str, symbol: str, interval: str, start: int, end: int, limit: int = 200) -> Dict[str, Any]:
    """
    Extracts candle stick data from the Bybit API.

    Params:
        category: Product type (spot, linear, inverse).
        symbol: Symbol name. Example: BTCUSDT
        interval: Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W
        start: Datetime from which to start. Format: "YYYY-MM-DD HH:MM:SS"
        end: Datetime until which to end. Format: "YYYY-MM-DD HH:MM:SS"
        limit: Number of klines to return. Default: 200
    """
    logger.info(f"Importing kline data for {symbol} between {start} and {end}...")

    return session.get_kline(
        category=category,
        symbol=symbol,
        interval=interval,
        start_time=to_unix(start) * 1000,
        end_time=to_unix(end) * 1000,
        limit=limit,
    )
