import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterator, Union

import pandas as pd
from config import BYBIT_CONFIG_PATH, BYBIT_DATA_PATH
from core.scripts.bybit.api import get_kline, get_symbol_info
from core.scripts.tools.files import read_file
from core.scripts.tools.logger import ANSI_COLORS, RESET, get_logger
from core.scripts.tools.metrics import calc_change
from core.scripts.tools.packers import pack_kline

logger = get_logger(__name__)

MARKET_CONFIG = read_file(f"{BYBIT_CONFIG_PATH}market.json", is_json=True)
SYMBOLS_LIKE = r"^[A-Z]+USDT$"
MIN_VOLUME, MIN_CHANGE = 1000000, 0.1
SL_PERCENTAGE, TP_PERCENTAGE = 2, 5
ROUND_TO = 10


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

    for symbol in symbols:
        kline = get_kline(category="spot", symbol=symbol, interval=interval, start=start, end=end)
        kline_df = pack_kline(
            symbol=symbol, kline=kline["result"]["list"], columns=config["columns"], sort=True
        )

        change = calc_change(
            kline_df["close_price"].astype(float), int(interval), symbol=symbol, lookback=lookback
        )
        total_volume = sum(kline_df["volume"].astype(float))

        if total_volume >= min_volume and change > min_change:
            yield kline_df


def get_daily_resistance_level(
    symbol: str, window: int, start: datetime, end: datetime, config: Dict[str, Any]
) -> float:
    """
    Get the daily resistance level.

    Params:
        symbol: Symbol to get the daily resistance level for.
        window: Rolling window to calculate the resistance level.
        start: Start date.
        end: End date.
        config: Config.
    """
    daily_kline = get_kline(category="spot", symbol=symbol, interval="D", start=start, end=end)
    daily_kline_df = pd.DataFrame(daily_kline["result"]["list"], columns=config["columns"])

    mean_high = daily_kline_df["high_price"].rolling(window=window).mean()
    std_high = daily_kline_df["high_price"].rolling(window=window).std()

    return mean_high.iloc[-1] + std_high.iloc[-1]


def check_breakout(symbol: str, resistance: float, data: pd.DataFrame) -> Union[Dict[str, Any], None]:
    """
    Check if the resistance level is broken.

    Params:
        symbol: Symbol to check.
        resistance: Resistance level.
        data: Kline data of the symbol.
    """
    cp = float(data["close_price"].iloc[-1])
    if cp > resistance:
        sl = cp * (1 - SL_PERCENTAGE / 100)
        tp = cp * (1 + TP_PERCENTAGE / 100)

        logger.info(
            f"{ANSI_COLORS['bg']['green']}BREAKOUT | {symbol}: "
            f"EP={round(cp, ROUND_TO)}, SL={round(sl, ROUND_TO)}, TP={round(tp, ROUND_TO)}{RESET}"
        )
        return {"symbol": symbol, "ep": cp, "sl": sl, "tp": tp}


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

        resistance = get_daily_resistance_level(
            symbol=symbol, window=DAILY_RESISTANCE_LOOKBACK, start=start, end=end, config=config
        )
        logger.info(
            f"{ANSI_COLORS['bg']['yellow']}RESISTANCE | {symbol}: {round(resistance, ROUND_TO)}{RESET}"
        )

        trade = check_breakout(symbol=symbol, resistance=resistance, data=symbol_data)
        if trade:
            breakouts.append(trade)

    pd.DataFrame(breakouts).to_csv(f"{BYBIT_DATA_PATH}breakout/breakouts.csv", index=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=str, required=False, default="15")
    parser.add_argument("--lookback", type=int, required=False, default=1)
    parser.add_argument("--drlookback", type=int, required=False, default=16)

    args = parser.parse_args()

    INTERVAL = args.interval
    LOOKBACK = args.lookback
    DAILY_RESISTANCE_LOOKBACK = args.drlookback

    main()
