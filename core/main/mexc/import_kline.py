import pandas as pd
from config import MEXC_CONFIG_PATH
from core.scripts.mexc.manager import import_mexc_kline
from core.scripts.tools.files import read_file

MCONFIG = read_file(f"{MEXC_CONFIG_PATH}market.json", is_json=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--category", type=str, required=False, default="futures")
    parser.add_argument("--symbol", type=str, required=False, default="BTC_USDT")
    parser.add_argument("--interval", type=str, required=False, default="Min5")

    args = parser.parse_args()
    CATEGORY = args.category
    SYMBOL = args.symbol.upper()
    INTERVAL = args.interval

    # Day1
    data = import_mexc_kline(category=CATEGORY, symbol=SYMBOL, interval=INTERVAL, csv=True)
