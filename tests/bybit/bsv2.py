import pandas as pd
from backtesting import Backtest
from config import BYBIT_CONFIG_PATH
from core.scripts.bybit.api import get_kline
from core.scripts.tools.files import read_file
from core.scripts.tools.logger import get_logger
from tests.strategy.breakout import BreakoutStrategyV2
from tests.tools.optimizer import optimize

MARKET_CONFIG = read_file(f"{BYBIT_CONFIG_PATH}market.json", is_json=True)

logger = get_logger(__name__)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="BTCUSDT")
    parser.add_argument("--interval", type=str, required=False, default="5")

    args = parser.parse_args()
    SYMBOL = args.symbol
    INTERVAL = args.interval

    kline = get_kline(category="spot", symbol=SYMBOL, interval=INTERVAL)["result"]["list"]
    kline = pd.DataFrame(kline, columns=MARKET_CONFIG["kline"]["columns"])

    kline["start_time"] = pd.to_datetime(kline["start_time"], unit="ms", utc=True)
    kline.set_index("start_time", inplace=True)
    kline.sort_index(inplace=True, ascending=True)

    kline = kline.astype(
        {
            "open_price": "float",
            "high_price": "float",
            "low_price": "float",
            "close_price": "float",
            "volume": "float",
        }
    )
    kline["resistance"] = kline["high_price"].rolling(window=12, min_periods=1).max().shift(1)
    kline["avg_volume"] = kline["volume"].rolling(window=12, min_periods=1).mean().shift(1)

    kline = kline[
        ["open_price", "high_price", "low_price", "close_price", "volume", "avg_volume", "resistance"]
    ]
    kline.columns = ["Open", "High", "Low", "Close", "Volume", "AvgVolume", "Resistance"]

    # Run the backtest
    bs = BreakoutStrategyV2
    bs.RL = kline["Resistance"]

    bt = Backtest(kline, bs, cash=100, commission=0.001)
    # optimize(bt)

    stats = bt.run()
    logger.info(f"{SYMBOL}\n{stats}")
    bt.plot()
