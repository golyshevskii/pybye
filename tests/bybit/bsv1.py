import pandas as pd
from backtesting import Backtest
from config import BYBIT_DATA_PATH
from core.scripts.tools.logger import get_logger
from tests.strategy.breakout import BreakoutStrategyV1
from tests.tools.optimizer import optimize

logger = get_logger(__name__)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="BTCUSDT")

    args = parser.parse_args()
    SYMBOL = args.symbol

    D_kline = pd.read_csv(f"{BYBIT_DATA_PATH}kline/bybit_kline_{SYMBOL}_spot_D.csv")
    kline = pd.read_csv(f"{BYBIT_DATA_PATH}kline/bybit_kline_{SYMBOL}_spot_15.csv")

    # Convert start_time to datetime and set it as index for better results in the backtest
    D_kline["start_time"] = pd.to_datetime(D_kline["start_time"], utc=True)
    D_kline.set_index("start_time", inplace=True)

    kline["start_time"] = pd.to_datetime(kline["start_time"], utc=True)
    kline.set_index("start_time", inplace=True)

    # Renaming columns to match backtesting format
    kline = kline[["open_price", "high_price", "low_price", "close_price", "volume"]]
    kline.columns = ["Open", "High", "Low", "Close", "Volume"]

    # Run the backtest
    bs = BreakoutStrategyV1
    bs.RL = D_kline["resistance_2"]

    bt = Backtest(kline, bs, cash=100, commission=0.001)
    # soptimize(bt)

    stats = bt.run()
    logger.info(f"{SYMBOL}\n{stats}")
    bt.plot()
