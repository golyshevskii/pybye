import pandas as pd
from backtesting import Backtest
from core.scripts.mexc.manager import import_mexc_kline
from core.scripts.tools.logger import ANSI_COLORS, RESET, get_logger
from tests.strategy.trend import BBMA
from tests.tools.optimizer import optimize

logger = get_logger(__name__)


def test(kline: pd.DataFrame):
    bbma = BBMA
    bt = Backtest(kline, bbma, cash=100, commission=0.002)

    params = {
        "RP": range(1, 4, 1),
        "TPP": range(5, 11, 1),
        "SLP": range(3, 6, 1),
        "EMA_PERIOD": range(20, 51, 10),
        "LOOKBACK": range(5, 21, 5),
    }
    # optimize(bt, maximize="Equity Final [$]", params=params)

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
