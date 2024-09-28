import pandas as pd
from config import BYBIT_DATA_PATH
from core.scripts.bybit.manager import import_bybit_kline
from core.scripts.tools.metrics import calc_rolling_sr_levels

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="BTCUSDT")

    args = parser.parse_args()
    SYMBOL = args.symbol

    D_file = import_bybit_kline(symbol=SYMBOL, interval="D")
    D_kline = pd.read_csv(f"{BYBIT_DATA_PATH}kline/{D_file}")

    D_kline = calc_rolling_sr_levels(D_kline, window_size=2)
    D_kline["dtt"] = pd.to_datetime(D_kline["start_time"], unit="ms", utc=True)

    D_kline.to_csv(f"{BYBIT_DATA_PATH}kline/{D_file}", index=False)

    H_file = import_bybit_kline(symbol=SYMBOL, interval="60")
    H_kline = pd.read_csv(f"{BYBIT_DATA_PATH}kline/{H_file}")

    H_kline = calc_rolling_sr_levels(H_kline, window_size=48)
    H_kline["dtt"] = pd.to_datetime(H_kline["start_time"], unit="ms", utc=True)

    H_kline.to_csv(f"{BYBIT_DATA_PATH}kline/{H_file}", index=False)
