import pandas as pd
from backtesting import Backtest
from core.scripts.mexc.manager import import_mexc_kline
from core.scripts.tools.logger import ANSI_COLORS, RESET, get_logger
from tests.strategy.trend import MeanReversionTrendStrategy
from tests.tools.optimizer import optimize_mrtfs

logger = get_logger(__name__)


def test(kline: pd.DataFrame):

    bt = Backtest(kline, MeanReversionTrendStrategy, cash=100, commission=0.002)
    # optimizer, heatmap = optimize_mrtfs(bt)
    # optimizer.to_csv("mrtfs_optimizer.csv")

    stats = bt.run()
    logger.info(f"\n{stats}")
    bt.plot()


def trade():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--category", type=str, required=False, default="futures")
    parser.add_argument("--symbol", type=str, required=False, default="WIF_USDT")
    parser.add_argument("--interval", type=str, required=False, default="Min5")

    args = parser.parse_args()
    CATEGORY = args.category.lower()
    SYMBOL: str = args.symbol.upper()
    INTERVAL = args.interval

    kline = import_mexc_kline(category=CATEGORY, symbol=SYMBOL, interval=INTERVAL)

    types = {"Open": float, "High": float, "Low": float, "Close": float, "Volume": float}
    kline = kline.astype(types)
    kline = kline[["Open", "High", "Low", "Close", "Volume"]]

    logger.info(f"{ANSI_COLORS['bg']['pink']}Backtesting {SYMBOL.replace('_', '')}{RESET}")
    test(kline)


trade()
