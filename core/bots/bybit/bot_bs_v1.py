import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterator, Union

import pandas as pd
from config import BYBIT_CONFIG_PATH, BYBIT_DATA_PATH
from core.scripts.bybit.api import get_kline, get_symbol_info
from core.scripts.tools.files import read_file
from core.scripts.tools.logger import ANSI_COLORS, RESET, get_logger
from core.scripts.tools.metrics import calc_change

logger = get_logger(__name__)

MARKET_CONFIG = read_file(f"{BYBIT_CONFIG_PATH}market.json", is_json=True)
SYMBOLS_LIKE = r"^[A-Z]+USDT$"
MIN_VOLUME, MIN_CHANGE = 2000000, 2
SL_PERCENTAGE, TP_PERCENTAGE = 2, 5


def get_tradeable_symbols(
    interval: str, lookback: int, min_volume: int, min_change: int, config: Dict[str, Any]
) -> Iterator[pd.DataFrame]:
    """
    Get the tradeable symbols.

    Params:
        interval: Interval of the klines.
        lookback: Lookback period in hours.
    """
    symbols = {
        symbol["symbol"]
        for symbol in get_symbol_info()["result"]["list"]
        if re.match(SYMBOLS_LIKE, symbol["symbol"])
    }

    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=lookback)

    i = 0
    for symbol in symbols:
        kline = get_kline(category="spot", symbol=symbol, interval=interval, start=start, end=end)["result"][
            "list"
        ]
        kline_df = pd.DataFrame(kline, columns=config["columns"])
        kline_df["symbol"] = symbol

        change = calc_change(
            kline_df["close_price"].astype(float), int(interval), symbol=symbol, lookback=lookback
        )
        total_volume = sum(kline_df["volume"].astype(float))

        if total_volume >= min_volume and change > min_change:
            i += 1
            yield kline_df

        if i > 10:
            break


def get_daily_resistance_level(symbol: str, start: datetime, end: datetime, config: Dict[str, Any]) -> float:
    """
    Get the daily resistance level.

    Params:
        symbol: Symbol to get the daily resistance level for.
        start: Start date.
        end: End date.
        config: Config.
    """
    daily_kline = get_kline(category="spot", symbol=symbol, interval="D", start=start, end=end)
    daily_kline_df = pd.DataFrame(daily_kline["result"]["list"], columns=config["columns"])

    return daily_kline_df["high_price"].max()


def check_breakout(symbol: str, resistance: float, data: pd.DataFrame) -> Union[Dict[str, Any], None]:
    """
    Check if the resistance level is broken.

    Params:
        symbol: Symbol to check.
        resistance: Resistance level.
        data: Kline data of the symbol.
    """
    cp = data["close_price"].iloc[-1]
    if cp > resistance:
        ep = cp
        sl = ep * (1 - SL_PERCENTAGE / 100)
        tp = ep + (1 + TP_PERCENTAGE / 100)

        logger.info(
            f"{ANSI_COLORS['bg']['green']}BREAKOUT | {symbol}: EP={round(ep, 5)}, SL={round(sl, 5)}, TP={round(tp, 5)}{RESET}"
        )
        return {"symbol": symbol, "ep": ep, "sl": sl, "tp": tp}


def main():
    config = MARKET_CONFIG["kline"]

    tradeable_symbols = get_tradeable_symbols(
        interval=INTERVAL, lookback=LOOKBACK, min_volume=MIN_VOLUME, min_change=MIN_CHANGE, config=config
    )

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=DAILY_RESISTANCE_LOOKBACK)

    breakouts = []
    for symbol_data in tradeable_symbols:
        symbol = symbol_data["symbol"].iloc[0]
        resistance = get_daily_resistance_level(symbol=symbol, start=start, end=end, config=config)
        logger.info(f"{ANSI_COLORS['bg']['yellow']}RESISTANCE | {symbol}: {resistance}{RESET}")

        trade = check_breakout(symbol=symbol, resistance=resistance, data=symbol_data)
        if trade:
            breakouts.append(trade)

    pd.DataFrame(breakouts).to_csv(f"{BYBIT_DATA_PATH}breakout/breakouts.csv")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--i", type=str, required=False, default="15")
    parser.add_argument("--lb", type=int, required=False, default=1)
    parser.add_argument("--drlb", type=int, required=False, default=10)

    args = parser.parse_args()

    INTERVAL = args.i
    LOOKBACK = args.lb
    DAILY_RESISTANCE_LOOKBACK = args.drlb

    main()
# NOTUSDT: 0.010561
