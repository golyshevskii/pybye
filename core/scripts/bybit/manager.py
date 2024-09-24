from datetime import datetime, timedelta, timezone

import pandas as pd
from config import BYBIT_CONFIG_PATH, BYBIT_DATA_PATH
from core.scripts.bybit.api import get_kline, get_symbol_info
from core.scripts.bybit.utils import to_min_interval
from core.scripts.tools.dtt import to_unix
from core.scripts.tools.files import read_file
from core.scripts.tools.logger import get_logger
from core.scripts.tools.metrics import calc_change, calc_sma
from core.scripts.tools.packers import pack_data

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

    data = get_kline(category=category, symbol=symbol, interval=interval, start=start, end=end)

    config = MARKET_CONFIG["kline"]
    packed_data = pack_data(
        data["result"]["list"],
        config["columns"],
        {"category": category, "symbol": symbol, "interval": interval},
    )

    file_name = config["file_name"].format(symbol=symbol, category=category, interval=interval)
    packed_data.to_csv(f"{BYBIT_DATA_PATH}kline/{file_name}", index=False)

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
    interval: str = "60",
    lookback: int = 4,
    only: str = "USDT",
    min_volume: int = 2000000,
):
    """
    Scans a symbol for potential trading opportunities.

    Params:
        symbol: Symbol name. Example: BTCUSDT
        category: Product type (spot, linear, inverse).
        interval: Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W
        lookback: Lookback in hours.
        only: Only look at symbols ending with this currency.
    """
    logger.debug("BEGIN")

    symbol_info = get_symbol_info(symbol=symbol, category=category)["result"]["list"]
    config = MARKET_CONFIG["kline"]

    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=lookback)

    changes = []
    i = 0
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

            close_prices = klines["close_price"]
            prices = pd.Series(float(price) for price in close_prices)
            volumes = pd.Series(float(volume) for volume in klines["volume"])

            total_volume = volumes.sum()
            if total_volume >= min_volume:
                changes.append(
                    {
                        "symbol": symbol,
                        "current_price": prices.iloc[-1],
                        "change": calc_change(
                            close_prices, interval=to_min_interval(interval), symbol=symbol, lookback=lookback
                        ),
                        "total_volume": round(total_volume),
                        "sma": calc_sma(prices, len(prices)),
                    }
                )
                i += 1

        if i > 5:
            break

    file_name = f"{category}_{interval}_scan.csv"
    pd.DataFrame(changes).to_csv(f"{BYBIT_DATA_PATH}scan/{file_name}", index=False)

    logger.debug("END")
