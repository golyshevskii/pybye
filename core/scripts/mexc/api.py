import logging
from datetime import datetime
from typing import Any, Dict, List, Union

from config import MEXC_API_KEY, MEXC_API_SECRET
from core.scripts.tools.dtt import to_unix
from core.scripts.tools.logger import ANSI_COLORS, RESET, get_logger
from pymexc import futures, spot

logger = get_logger(__name__, level=logging.INFO)

SCLIENT = spot.HTTP(api_key=MEXC_API_KEY, api_secret=MEXC_API_SECRET)
FCLIENT = futures.HTTP(api_key=MEXC_API_KEY, api_secret=MEXC_API_SECRET)
SWEB_SOCKET = spot.WebSocket(api_key=MEXC_API_KEY, api_secret=MEXC_API_SECRET)
FWEB_SOCKET = futures.WebSocket(api_key=MEXC_API_KEY, api_secret=MEXC_API_SECRET)

PFG = ANSI_COLORS["fg"]["pink"]


def get_kline(
    category: str,
    symbol: str,
    interval: str,
    start: Union[int, str, datetime] = None,
    end: Union[int, str, datetime] = None,
) -> Dict[str, Any]:
    """
    Extracts candle stick data from the MEXC API.

    Params:
        category: Product type (spot, futures).
        symbol: Symbol name. Example: BTC_USDT
        interval: Kline interval.
            futures! ['Min1', 'Min5', 'Min15', 'Min30', 'Min60', 'Hour4', 'Hour8', 'Day1', 'Week1', 'Month1']
            spot! ['1m', '5m', '15m', '30m', '60m', '4h', '1d', '1M']
        start: Timestamp (s) from which to start
        end: Timestamp (s) until which to end
    """
    logger.debug(f"Extracting {PFG}{interval}{RESET} kline data for {PFG}{symbol}{RESET}")

    if category == "futures":
        return FCLIENT.kline(
            symbol=symbol,
            interval=interval,
            start=to_unix(start) if isinstance(start, (str, datetime)) else start,
            end=to_unix(end) if isinstance(end, (str, datetime)) else end,
        )

    if category == "spot":
        return SCLIENT.klines(
            symbol=symbol.replace("_", ""),
            interval=interval,
            start=to_unix(start) if isinstance(start, (str, datetime)) else start,
            end=to_unix(end) if isinstance(end, (str, datetime)) else end,
        )


def get_ticker_24h(symbol: Union[str, None] = "BTCUSDT") -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Gets 24h price stats for a specific symbol.

    Params
        symbol: Symbol name. Example: BTCUSDT
        WARNING: if symbol is None, all symbols will be returned
    """
    logger.debug(f"Extracting 24h price ticker for {PFG}{symbol}{RESET}")
    return SCLIENT.ticker_24h(symbol=symbol)


def get_depth(symbol: str = "BTC_USDT", limit: int = None) -> Dict[str, Any]:
    """
    Gets futures order book for a specific symbol.

    Params
        symbol: Symbol name. Example: BTC_USDT
        limit: Number of bids and asks to return.
    """
    logger.debug(f"Extracting futures order book for {PFG}{symbol}{RESET}")
    return FCLIENT.get_depth(symbol=symbol, limit=limit)


def get_ndepth(symbol: str = "BTC_USDT", limit: int = None) -> Dict[str, Any]:
    """
    Gets futures order book for a specific symbol.

    Params
        symbol: Symbol name. Example: BTC_USDT
        limit: Number of bids and asks to return.
    """
    logger.debug(f"Extracting futures order book for {PFG}{symbol}{RESET}")
    return FCLIENT.depth_commits(symbol=symbol, limit=limit)


def get_ftrades(symbol: str = "BTC_USDT", limit: int = 100) -> Dict[str, Any]:
    """
    Gets spot recent trades for a specific symbol.

    Params
        symbol: Symbol name. Example: BTC_USDT
        limit: Number of bids and asks to return.
    """
    logger.debug(f"Extracting futures recent trades for {PFG}{symbol}{RESET}")
    return FCLIENT.deals(symbol=symbol, limit=limit)


def get_fticker(symbol: str = "BTC_USDT") -> Dict[str, Any]:
    """
    Gets futures trand ticker for a specific symbol.

    Params
        symbol: Symbol name. Example: BTC_USDT
    """
    logger.debug(f"Extracting futures trand ticker for {PFG}{symbol}{RESET}")
    return FCLIENT.ticker(symbol)


def get_strades(symbol: str = "BTCUSDT", limit: int = 100) -> List[Dict[str, Any]]:
    """
    Gets spot recent trades for a specific symbol.

    Params
        symbol: Symbol name. Example: BTCUSDT
        limit: Number of trades to return.
    """
    logger.debug(f"Extracting spot recent trades for {PFG}{symbol}{RESET}")
    return SCLIENT.trades(symbol=symbol, limit=limit)
