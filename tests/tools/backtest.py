import numpy as np
from backtesting import Strategy
from backtesting.test import SMA
from core.scripts.tools.logger import get_logger

logger = get_logger(__name__)


class BreakoutStrategy(Strategy):
    atr_period = 10
    resistance_levels = None
    risk_percentage = 0.01  # 1% risk per trade
    sma_long_period = 50
    sma_short_period = 20
    atr_multiple_sl = 0.5  # Use 0.5x ATR for SL
    risk_reward_ratio = 3  # 1:3 risk-reward ratio

    def init(self):
        # Initialize indicators
        self.atr = self.I(SMA, self.data.Close, self.atr_period)
        self.sma_long = self.I(SMA, self.data.Close, self.sma_long_period)
        self.sma_short = self.I(SMA, self.data.Close, self.sma_short_period)

    def next(self):
        current_time = self.data.index[-1]

        # Get the resistance level
        try:
            resistance = self.resistance_levels[self.resistance_levels.index <= current_time].iloc[-1]
        except IndexError:
            return

        close_price = self.data.Close[-1]

        # Ensure breakout above resistance and price above both SMAs
        if close_price > resistance and close_price > self.sma_long[-1] and not self.position:
            # Enter trade with tighter SL and fixed 1:3 risk-reward ratio
            breakout_close = close_price
            entry_price = (resistance + breakout_close) / 2
            atr_value = self.atr[-1]

            # Define a tighter stop-loss and take-profit with a 1:3 ratio
            sl = max(entry_price - self.atr_multiple_sl * atr_value, 0.001)
            tp = entry_price + self.risk_reward_ratio * (entry_price - sl)

            # Position size based on risk
            risk_per_trade = self.equity * self.risk_percentage
            position_size = risk_per_trade / (entry_price - sl)

            # Ensure valid position size
            if position_size > 0:
                position_size = max(1, int(position_size))  # Ensure at least 1 unit

                # Place the trade
                self.buy(size=position_size, sl=sl, tp=tp)
                logger.info(f"Entry at {entry_price}, SL: {sl}, TP: {tp}, Size: {position_size}")

        # Exit condition based on SMA crossover
        if self.position and close_price < self.sma_short[-1]:
            logger.info(f"Exiting position at {close_price}, SMA: {self.sma_short[-1]}")
            self.sell()  # Exit the trade if the short SMA is crossed
