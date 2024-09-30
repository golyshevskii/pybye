from backtesting import Strategy
from backtesting.test import SMA
from core.scripts.tools.logger import get_logger

logger = get_logger(__name__)


class BreakoutStrategyV1(Strategy):
    ATR_PERIOD = 10
    TP_PERCENTAGE = 2
    SL_PERCENTAGE = 4
    RL = None

    def init(self):
        self.atr = self.I(SMA, self.data.Close, self.ATR_PERIOD)

    def next(self):
        current_time = self.data.index[-1]
        resistance = self.RL.asof(current_time)

        close_price = self.data.Close[-1]
        if close_price > resistance:
            sl = close_price * (1 - self.SL_PERCENTAGE / 100)
            tp = close_price * (1 + self.TP_PERCENTAGE / 100)

            if sl <= 0 or sl >= close_price or tp <= close_price:
                return

            try:
                self.buy(sl=sl, tp=tp)
            except ValueError:
                return


class BreakoutStrategyV2(Strategy):
    ATR_PERIOD = 10
    TP_PERCENTAGE = 5
    SL_PERCENTAGE = 2
    RL = None

    def init(self):
        self.atr = self.I(SMA, self.data.Close, self.ATR_PERIOD)

    def next(self):
        current_time = self.data.index[-1]
        resistance = self.RL.asof(current_time)

        close_price = self.data.Close[-1]

        # Проверка на пробой сопротивления и объемы
        if close_price > resistance and self.data.Volume[-1] > self.data.AvgVolume[-1]:
            sl = close_price * (1 - self.SL_PERCENTAGE / 100)
            tp = close_price * (1 + self.TP_PERCENTAGE / 100)

            if sl <= 0 or sl >= close_price or tp <= close_price:
                return

            try:
                logger.info(f"Buy at {close_price} with SL={sl} and TP={tp}")
                self.buy(sl=sl, tp=tp)
            except ValueError:
                return


class MultiframeBreakout(Strategy):
    """
    Combine breakout strategies across multiple timeframes to filter false signals and increase the accuracy of breakouts.
    """

    SMA_PERIOD = 20
    SL_PERCENTAGE, TP_PERCENTAGE = 1, 5
    RLD, RL4H, RL1H, RL15M = None, None, None, None

    def init(self):
        self.sma = self.I(SMA, self.data.Close, self.SMA_PERIOD)

    def next(self):
        timestamp = self.data.index[-1]

        resistance_d = self.RLD.asof(timestamp)
        resistance_4h = self.RL4H.asof(timestamp)
        resistance_1h = self.RL1H.asof(timestamp)
        resistance_15m = self.RL15M.asof(timestamp)

        vol = self.data.Volume[-1]
        avg_vol = self.data.AvgVolume[-1]

        cp = self.data.Close[-1]
        if (
            cp > resistance_d
            and cp > resistance_4h
            and cp > resistance_1h
            and cp > resistance_15m
            and vol > avg_vol
        ):
            sl = cp * (1 - self.SL_PERCENTAGE / 100)
            tp = cp * (1 + self.TP_PERCENTAGE / 100)

            if sl <= 0 or sl >= cp or tp <= cp:
                return

            try:
                self.buy(sl=sl, tp=tp)
            except ValueError:
                return
