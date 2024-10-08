from datetime import datetime
from typing import Any, Dict, Union

from config import BYBIT_DEMO_API_KEY, BYBIT_DEMO_API_SECRET
from core.scripts.tools.dtt import to_unix
from core.scripts.tools.logger import get_logger
from pybit.unified_trading import HTTP

logger = get_logger(__name__)

SESSION = HTTP(api_key=BYBIT_DEMO_API_KEY, api_secret=BYBIT_DEMO_API_SECRET)
DSESSION = HTTP(api_key=BYBIT_DEMO_API_KEY, api_secret=BYBIT_DEMO_API_SECRET, demo=True)


def get_kline(
    category: str,
    symbol: str,
    interval: str,
    start: Union[int, str, datetime] = None,
    end: Union[int, str, datetime] = None,
    limit: int = 1000,
) -> Dict[str, Any]:
    """
    Extracts candle stick data from the Bybit API.

    Params:
        category: Product type (spot, linear, inverse).
        symbol: Symbol name. Example: BTCUSDT
        interval: Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W
        start: Timestamp (ms) from which to start
        end: Timestamp (ms) until which to end
        limit: Number of candles to return. Max is 1000.
    """
    logger.info(f"Importing {interval} kline data for {symbol}")

    return SESSION.get_kline(
        category=category,
        symbol=symbol,
        interval=interval,
        start=to_unix(start) * 1000 if isinstance(start, (str, datetime)) else start,
        end=to_unix(end) * 1000 if isinstance(end, (str, datetime)) else end,
        limit=limit,
    )


def get_symbol_info(category: str = "spot", symbol: str = None) -> Dict[str, Any]:
    """
    Extracts symbol info from the Bybit API.

    Params:
        category: Product type (spot, linear, inverse).
        symbol: Symbol name. Example: BTCUSDT
        exclude: List of symbols to exclude.
    """
    logger.info(f"Importing {symbol or 'all'} symbol info")
    return SESSION.get_instruments_info(category=category, symbol=symbol)


def get_account_balance(account_type: str = "SPOT", coin: str = "USDT") -> Dict[str, Any]:
    """
    Extracts account balance from the Bybit API.

    Params:
        account_type: Account type (spot, linear, inverse).
        coin: Coin in which to get the balance. Example: USDT
    """
    logger.info(f"Importing {coin} balance for {account_type} account")
    return SESSION.get_wallet_balance(accountType=account_type, coin=coin)


def get_spot_asset_info(coin: str = "USDT") -> Dict[str, Any]:
    """
    Extracts spot asset info from the Bybit API.
    """
    logger.info("Importing spot asset info")
    return SESSION.get_spot_asset_info(accountType="SPOT", coin=coin)
