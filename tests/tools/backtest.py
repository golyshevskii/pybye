from backtesting import Strategy
from backtesting.test import SMA
from core.scripts.tools.logger import get_logger

logger = get_logger(__name__)


class BreakoutStrategy(Strategy):
    ATR_PERIOD = 10
    TP_PERCENTAGE = 5
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
            ep = (resistance + close_price) / 2

            # Define stop-loss and take-profit
            sl = ep * (1 - self.SL_PERCENTAGE / 100)
            tp = ep * (1 + self.TP_PERCENTAGE / 100)

            # Additional check to ensure valid sl and tp
            if sl <= 0 or sl >= ep or tp <= ep:
                return  # Skip trade

            # Proceed with valid trade setup
            # logger.info(f"BREAKOUT! EP: {round(ep, 2)}, SL: {round(sl, 2)}, TP: {round(tp, 2)}")
            try:
                # Proceed with valid trade setup
                self.buy(sl=sl, tp=tp)
            except ValueError:
                return  # Skip invalid order
