from backtesting import Strategy
from backtesting.test import SMA


class BreakoutStrategy(Strategy):
    atr_period = 14
    resistance_levels = None

    def init(self):
        # Initialize ATR indicator
        self.atr = self.I(SMA, self.data.Close, self.atr_period)

    def next(self):
        current_time = self.data.index[-1]
        resistance = self.resistance_levels[self.resistance_levels.index <= current_time].iloc[-1]

        if self.data.Close[-1] > resistance:
            breakout_close = self.data.Close[-1]
            entry_price = (resistance + breakout_close) / 2

            sl = entry_price - self.atr[-1]
            self.buy(sl=sl)
