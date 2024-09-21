import pandas as pd
from backtesting import Backtest
from config import BYBIT_DWH_PATH
from tests.tools.backtest import BreakoutStrategy

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="BTCUSDT")

    args = parser.parse_args()
    SYMBOL = args.symbol

    D_kline = pd.read_csv(f"{BYBIT_DWH_PATH}kline/bybit_kline_{SYMBOL}_spot_D.csv")
    H_kline = pd.read_csv(f"{BYBIT_DWH_PATH}kline/bybit_kline_{SYMBOL}_spot_60.csv")

    # Convert start_time to datetime and set it as index for better results in the backtest
    D_kline["start_time"] = pd.to_datetime(D_kline["start_time"], unit="ms", utc=True)
    D_kline.set_index("start_time", inplace=True)
    D_kline.sort_index(inplace=True, ascending=True)

    H_kline["start_time"] = pd.to_datetime(H_kline["start_time"], unit="ms", utc=True)
    H_kline.set_index("start_time", inplace=True)
    H_kline.sort_index(inplace=True, ascending=True)

    # Renaming columns to match backtesting format
    H_kline = H_kline[["open_price", "high_price", "low_price", "close_price", "volume"]]
    H_kline.columns = ["Open", "High", "Low", "Close", "Volume"]

    # Run the backtest
    bs = BreakoutStrategy
    bs.RL = D_kline["resistance"]

    bt = Backtest(H_kline, bs, cash=100000, commission=0.002)
    stats = bt.run()

    optimizer = bt.optimize(TP_PERCENTAGE=range(10, 31, 1), maximize="Equity Final [$]")

    print(stats, optimizer, sep="\n\n")
    bt.plot()
