from datetime import datetime, timedelta, timezone

import pandas as pd
from config import BYBIT_CONFIG_PATH, BYBIT_DATA_PATH
from core.scripts.bybit.api import get_kline, get_symbol_info
from core.scripts.bybit.utils import to_min_interval
from core.scripts.tools.dtt import to_unix
from core.scripts.tools.files import read_file
from core.scripts.tools.logger import ANSI_COLORS, RESET, get_logger
from core.scripts.tools.metrics import calc_change, calc_sma
from core.scripts.tools.packers import pack_data, pack_kline

logger = get_logger(__name__)
MARKET_CONFIG = read_file(f"{BYBIT_CONFIG_PATH}market.json", is_json=True)


def import_bybit_kline(
    symbol: str, interval: str, start: str = None, end: str = None, category: str = "spot"
) -> str:
    """
    Imports candle stick data from the Bybit API.

    Params:
        symbol: Symbol name. Example: BTCUSDT
        interval: Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W
        start: Datetime from which to start. Format: "YYYY-MM-DD HH:MM:SS"
        end: Datetime until which to end. Format: "YYYY-MM-DD HH:MM:SS"
        category: Product type (spot, linear, inverse).

    Returns:
        file_name: Name of the file where the data is stored.
    """
    logger.debug("BEGIN")

    kline = get_kline(category=category, symbol=symbol, interval=interval, start=start, end=end)

    config = MARKET_CONFIG["kline"]
    packed_kline = pack_kline(
        symbol=symbol, kline=kline["result"]["list"], columns=config["columns"], sort=True
    )

    file_name = config["file_name"].format(symbol=symbol, category=category, interval=interval)
    packed_kline.to_csv(f"{BYBIT_DATA_PATH}kline/{file_name}")

    logger.debug("END")
    return file_name


def import_bybit_symbol_info(symbol: str = None, category: str = "spot") -> str:
    """
    Imports symbol info from the Bybit API.

    Params:
        symbol: Symbol name. Example: BTCUSDT
        category: Product type (spot, linear, inverse).
    """
    logger.debug("BEGIN")
    data = get_symbol_info(category=category, symbol=symbol)

    config = MARKET_CONFIG["symbol_info"]
    packed_data = pack_data(data["result"]["list"], config["columns"], {"category": category})

    file_name = config["file_name"].format(symbol=symbol, category=category)
    packed_data.to_csv(f"{BYBIT_DATA_PATH}info/{file_name}", index=False)

    logger.debug("END")
    return file_name


def scan_bybit_symbol(
    symbol: str = None,
    category: str = "spot",
    interval: str = "15",
    lookback: int = 4,
    only: str = "USDT",
    min_volume: int = 2000000,
    max_symbols: int = 50,
):
    """
    Scans a symbol for potential trading opportunities.

    Params:
        symbol: Symbol name. Example: BTCUSDT
        category: Product type (spot, linear, inverse).
        interval: Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W
        lookback: Lookback in hours.
        only: Only look at symbols ending with this currency.
        min_volume: Minimum volume to consider.
        max_symbols: Maximum number of symbols to consider.
    """
    logger.debug("BEGIN")

    symbol_info = get_symbol_info(symbol=symbol, category=category)["result"]["list"]
    config = MARKET_CONFIG["kline"]

    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=lookback)

    changes, i = [], 0
    for info in symbol_info:
        symbol = info["symbol"]

        if symbol.endswith(only) and not symbol.startswith("USDC"):
            data = get_kline(
                category=category,
                symbol=symbol,
                interval=interval,
                start=to_unix(start) * 1000,
                end=to_unix(end) * 1000,
            )["result"]["list"]
            klines = pack_data(data, config["columns"])

            prices = pd.Series(float(price) for price in klines["close_price"])
            volumes = pd.Series(float(volume) for volume in klines["volume"])

            total_volume = sum(volumes)
            if total_volume >= min_volume:
                changes.append(
                    {
                        "symbol": symbol,
                        "current_price": prices.iloc[0],
                        "change": calc_change(
                            prices, interval=to_min_interval(interval), symbol=symbol, lookback=lookback
                        ),
                        "total_volume": round(total_volume),
                        "sma": calc_sma(prices, len(prices)),
                    }
                )
                i += 1

        if i >= max_symbols:
            break

    file_name = f"{category}_{interval}_scan.csv"
    scaned_symbols = pd.DataFrame(changes).sort_values(by="change", ascending=False)
    scaned_symbols.to_csv(f"{BYBIT_DATA_PATH}scan/{file_name}", index=False)

    logger.info(f"Top token: {ANSI_COLORS['bg']['pink']}{scaned_symbols['symbol'].iloc[0]}{RESET}")
    logger.debug("END")
    return file_name
