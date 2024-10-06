import argparse as ap

from backtesting import Backtest
from core.scripts.bybit.manager import import_bybit_kline
from core.scripts.tools.logger import ANSI_COLORS, RESET, get_logger
from core.scripts.tools.signals import set_donchian_breakout_signal
from tests.strategy.breakout import Breakout
from tests.tools.optimizer import optimize

logger = get_logger(__name__)


def main():
    parser = ap.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="BTCUSDT")
    parser.add_argument("--interval", type=str, required=False, default="5")
    parser.add_argument("--period", type=int, required=False, default=20)

    args = parser.parse_args()
    SYMBOL = args.symbol.upper()
    INTERVAL = args.interval
    PERIOD = args.period

    pfg = ANSI_COLORS["fg"]["pink"]
    pbg = ANSI_COLORS["bg"]["pink"]

    logger.debug(f"Processing symbol {pfg}{SYMBOL}{RESET} with interval {pfg}{INTERVAL}{RESET}")

    kline = import_bybit_kline(symbol=SYMBOL, interval=INTERVAL)

    types = {"Open": float, "High": float, "Low": float, "Close": float, "Volume": float}

    kline = kline.astype(types)
    kline = kline[["Open", "High", "Low", "Close", "Volume"]]
    set_donchian_breakout_signal(kline, period=PERIOD)

    bs = Breakout
    bs.PERIOD = PERIOD

    bt = Backtest(kline, bs, cash=100, commission=0.0002)
    # optimize(bt)

    stats = bt.run()
    logger.info(f"\n{ANSI_COLORS['bg']['pink']}{SYMBOL}{RESET}\n{stats}")
    bt.plot()


main()
