import pandas as pd
from config import BYBIT_DATA_PATH
from core.scripts.bybit.manager import import_bybit_kline
from core.scripts.tools.metrics import calc_rolling_sr_levels

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="BTCUSDT")
    parser.add_argument("--interval", type=str, required=False, default="15")

    args = parser.parse_args()
    SYMBOL = args.symbol
    INTERVAL = args.interval

    D_file = import_bybit_kline(symbol=SYMBOL, interval="D")
    D_kline = pd.read_csv(f"{BYBIT_DATA_PATH}kline/{D_file}")

    D_kline = calc_rolling_sr_levels(D_kline, window=16)
    D_kline.to_csv(f"{BYBIT_DATA_PATH}kline/{D_file}", index=False)

    file = import_bybit_kline(symbol=SYMBOL, interval=INTERVAL)
    kline = pd.read_csv(f"{BYBIT_DATA_PATH}kline/{file}")

    kline = calc_rolling_sr_levels(kline, window=4)
    kline.to_csv(f"{BYBIT_DATA_PATH}kline/{file}", index=False)
