import pandas as pd
from backtesting import Backtest
from core.scripts.bybit.manager import import_bybit_kline
from core.scripts.tools.packers import setup_scalp_kline
from tests.strategy.scalp import Scalp
from tests.tools.optimizer import optimize


def plot_scalp_kline(pkline):
    from datetime import datetime

    import numpy as np
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    def pointpos(x):
        if x["signal"] == 2:
            return x["Low"] - 1e-3
        elif x["signal"] == 1:
            return x["High"] + 1e-3
        else:
            return np.nan

    pkline["pointpos"] = pkline.apply(lambda row: pointpos(row), axis=1)

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=pkline.index,
                open=pkline["Open"],
                high=pkline["High"],
                low=pkline["Low"],
                close=pkline["Close"],
            ),
            go.Scatter(x=pkline.index, y=pkline["BBL_20_2"], line=dict(color="green", width=1), name="BBL"),
            go.Scatter(x=pkline.index, y=pkline["BBU_20_2"], line=dict(color="green", width=1), name="BBU"),
            go.Scatter(x=pkline.index, y=pkline["FEMA"], line=dict(color="black", width=1), name="FEMA"),
            go.Scatter(x=pkline.index, y=pkline["SEMA"], line=dict(color="blue", width=1), name="SEMA"),
        ]
    )

    fig.add_scatter(
        x=pkline.index,
        y=pkline["pointpos"],
        mode="markers",
        marker=dict(size=5, color="MediumPurple"),
        name="entry",
    )
    fig.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="BTCUSDT")
    parser.add_argument("--interval", type=str, required=False, default="5")

    args = parser.parse_args()
    SYMBOL = args.symbol
    INTERVAL = args.interval

    kline = import_bybit_kline(symbol=SYMBOL, interval=INTERVAL)
    kline.reset_index(inplace=True)

    types = {
        "open_price": float,
        "high_price": float,
        "low_price": float,
        "close_price": float,
        "volume": float,
    }
    kline = kline.astype(types)

    kline = kline[["start_time", "open_price", "high_price", "low_price", "close_price", "volume"]]
    kline.columns = ["Time", "Open", "High", "Low", "Close", "Volume"]

    kwargs = {
        "lookback": 14,
        "sema_len": 50,
        "fema_len": 20,
        "rsi_len": 14,
        "bbands_len": 20,
        "bbands_std": 2,
        "atr_len": 14,
    }

    pkline = setup_scalp_kline(kline, **kwargs)
    pkline.set_index("Time", inplace=True)

    print(pkline.tail(3))

    bt = Backtest(pkline, Scalp, commission=0.001, cash=100)
    # optimize(bt)

    stats = bt.run()
    print(f"{SYMBOL}\n{stats}")
    bt.plot()
    # plot_scalp_kline(pkline)
