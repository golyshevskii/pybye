from typing import Any, Dict

from config import BYBIT_DEMO_API_KEY, BYBIT_DEMO_API_SECRET
from core.scripts.tools.dtt import to_unix
from core.scripts.tools.logger import get_logger
from pybit.unified_trading import HTTP

logger = get_logger(__name__)
session = HTTP(api_key=BYBIT_DEMO_API_KEY, api_secret=BYBIT_DEMO_API_SECRET)


def get_kline(
    category: str, symbol: str, interval: str, start: str = None, end: str = None, limit: int = 1000
) -> Dict[str, Any]:
    """
    Extracts candle stick data from the Bybit API.

    Params:
        category: Product type (spot, linear, inverse).
        symbol: Symbol name. Example: BTCUSDT
        interval: Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W
        start: Datetime from which to start. Format: "YYYY-MM-DD HH:MM:SS"
        end: Datetime until which to end. Format: "YYYY-MM-DD HH:MM:SS"
        limit: Number of candles to return. Max is 1000.
    """
    logger.info(f"Importing {interval} kline data for {symbol} between {start} and {end}...")

    return session.get_kline(
        category=category,
        symbol=symbol,
        interval=interval,
        start=to_unix(start) * 1000 if start else None,
        end=to_unix(end) * 1000 if end else None,
        limit=limit,
    )
