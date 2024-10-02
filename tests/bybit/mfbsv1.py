import pandas as pd
from backtesting import Backtest
from core.scripts.bybit.manager import import_bybit_kline
from core.scripts.tools.metrics import calc_rolling_sr_levels
from tests.strategy.breakout import MultiframeBreakout
from tests.tools.optimizer import optimize

WD = 20
W4H = 14
W1H = 50
W15M = 30
W5M = 24


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="BTCUSDT")

    args = parser.parse_args()
    SYMBOL = args.symbol

    kline_d = import_bybit_kline(symbol=SYMBOL, interval="D")
    kline_4h = import_bybit_kline(symbol=SYMBOL, interval="240")
    kline_1h = import_bybit_kline(symbol=SYMBOL, interval="60")
    kline_15m = import_bybit_kline(symbol=SYMBOL, interval="15")
    kline_5m = import_bybit_kline(symbol=SYMBOL, interval="5")

    types = {
        "open_price": float,
        "high_price": float,
        "low_price": float,
        "close_price": float,
        "volume": float,
    }

    kline_d = kline_d.astype(types)
    kline_4h = kline_4h.astype(types)
    kline_1h = kline_1h.astype(types)
    kline_15m = kline_15m.astype(types)
    kline_5m = kline_5m.astype(types)

    kline_d = calc_rolling_sr_levels(kline_d, window=WD)
    kline_4h = calc_rolling_sr_levels(kline_4h, window=W4H)
    kline_1h = calc_rolling_sr_levels(kline_1h, window=W1H)
    kline_15m = calc_rolling_sr_levels(kline_15m, window=W15M)

    kline_5m["avg_volume"] = kline_5m["volume"].rolling(window=W5M, min_periods=1).mean().shift(1)
    kline_5m = kline_5m[["open_price", "high_price", "low_price", "close_price", "volume", "avg_volume"]]
    kline_5m.columns = ["Open", "High", "Low", "Close", "Volume", "AvgVolume"]

    mfbs = MultiframeBreakout
    mfbs.RLD = kline_d["resistance"]
    mfbs.RL4H = kline_4h["resistance"]
    mfbs.RL1H = kline_1h["resistance"]
    mfbs.RL15M = kline_15m["resistance"]

    bt = Backtest(kline_5m, mfbs, cash=100, commission=0.001)
    # optimize(bt)

    stats = bt.run()
    print(f"{SYMBOL}\n{stats}")
    bt.plot()
