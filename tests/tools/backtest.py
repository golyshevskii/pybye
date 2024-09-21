from backtesting import Strategy
from backtesting.test import SMA
from core.scripts.tools.logger import get_logger

logger = get_logger(__name__)


class BreakoutStrategy(Strategy):
    ATR_PERIOD = 10
    TP_PERCENTAGE = 6
    SL_PERCENTAGE = 2
    RL = None

    def init(self):
        # Initialize indicators
        self.atr = self.I(SMA, self.data.Close, self.ATR_PERIOD)

    def next(self):
        current_time = self.data.index[-1]
        resistance = self.RL[self.RL.index <= current_time].iloc[-1]

        close_price = self.data.Close[-1]
        if close_price > resistance:
            breakout_close = close_price
            entry_price = (resistance + breakout_close) / 2
            # atr_value = self.atr[-1]

            # Define a tighter stop-loss and take-profit
            sl = entry_price * (1 - self.SL_PERCENTAGE / 100)
            tp = entry_price * (1 + self.TP_PERCENTAGE / 100)

            # Place the trade
            # logger.info(f"BREAKOUT! EP: {round(entry_price, 2)}, SL: {round(sl, 2)}, TP: {round(tp, 2)}")
            self.buy(sl=sl, tp=tp)
