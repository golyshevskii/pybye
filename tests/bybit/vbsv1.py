import pandas as pd
from backtesting import Backtest
from core.scripts.bybit.manager import import_bybit_kline
from tests.strategy.breakout import VolatilityBreakout
from tests.tools.optimizer import optimize

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="BTCUSDT")
    parser.add_argument("--interval", type=str, required=False, default="5")

    args = parser.parse_args()
    SYMBOL = args.symbol
    INTERVAL = args.interval

    kline = import_bybit_kline(symbol=SYMBOL, interval=INTERVAL)

    types = {
        "open_price": float,
        "high_price": float,
        "low_price": float,
        "close_price": float,
        "volume": float,
    }

    kline = kline.astype(types)

    kline = kline[["open_price", "high_price", "low_price", "close_price", "volume"]]
    kline.columns = ["Open", "High", "Low", "Close", "Volume"]

    bt = Backtest(kline, VolatilityBreakout, cash=100, commission=0.001)
    # optimize(bt)

    stats = bt.run()
    print(f"{SYMBOL}\n{stats}")
    bt.plot()
