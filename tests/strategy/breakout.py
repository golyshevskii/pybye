import numpy as np
from backtesting import Strategy
from backtesting.lib import crossover
from core.scripts.tools.logger import get_logger
from talib import ADX, ATR, SMA

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
    SL_PERCENTAGE, TP_PERCENTAGE = 1, 3.5
    RLD, RL4H, RL1H, RL15M = None, None, None, None
    SLD, SL4H, SL1H, SL15M = None, None, None, None

    def init(self):
        self.sma = self.I(SMA, self.data.Close, self.SMA_PERIOD)

    def next(self):
        timestamp = self.data.index[-1]

        resistance_d = self.RLD.asof(timestamp)
        resistance_4h = self.RL4H.asof(timestamp)
        resistance_1h = self.RL1H.asof(timestamp)
        resistance_15m = self.RL15M.asof(timestamp)

        support_d = self.SLD.asof(timestamp)
        support_4h = self.SL4H.asof(timestamp)
        support_1h = self.SL1H.asof(timestamp)
        support_15m = self.SL15M.asof(timestamp)

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

        elif cp < support_d and cp < support_4h and cp < support_1h and cp < support_15m and vol > avg_vol:
            sl = cp * (1 + self.SL_PERCENTAGE / 100)
            tp = cp * (1 - self.TP_PERCENTAGE / 100)

            if sl <= 0 or sl <= cp or tp >= cp:
                return

            try:
                self.sell(sl=sl, tp=tp)
            except ValueError:
                return


class VolatilityBreakout(Strategy):
    """Use the Average True Range (ATR) to adjust breakout levels based on market volatility"""

    ATR_PERIOD = 7
    ATR_MULTIPLIER = 0.4
    ATR_RATIO = 2
    RSI_PERIOD = 7

    def init(self):
        self.atr = self.I(self.calc_atr, self.data, self.ATR_PERIOD)
        self.rsi = self.I(self.calc_rsi, self.data, self.RSI_PERIOD)

    def next(self):
        cp = self.data.Close[-1]
        hp = self.data.High[-2]
        lp = self.data.Low[-2]
        atrv = self.atr[-1]
        rsiv = self.rsi[-1]

        if atrv < 0.3:
            self.ATR_MULTIPLIER = 0.5

        breakout_high = hp + self.ATR_MULTIPLIER * atrv
        breakout_low = lp - self.ATR_MULTIPLIER * atrv
        sl = self.ATR_RATIO * atrv

        print(
            f"Time: {self.data.index[-1]} | Close: {cp}, Breakout High: {breakout_high}, Breakout Low: {breakout_low}, ATR: {atrv}, RSI: {rsiv}"
        )

        if rsiv > 50 and cp > breakout_high:
            self.buy(sl=cp - sl)
        elif rsiv < 50 and cp < breakout_low:
            self.sell(sl=cp + sl)

    def calc_atr(self, data, period=14):
        tr = np.maximum(
            data.High - data.Low,
            np.maximum(np.abs(data.High - data.Close[-2]), np.abs(data.Low - data.Close[-2])),
        )
        atr = np.convolve(tr, np.ones((period,)) / period, mode="valid")
        return np.concatenate([np.full(period - 1, np.nan), atr])

    def calc_rsi(self, data, period=14):
        gains = np.zeros(len(data.Close))
        losses = np.zeros(len(data.Close))

        for i in range(1, len(data.Close)):
            change = data.Close[i] - data.Close[i - 1]
            if change > 0:
                gains[i] = change
            elif change < 0:
                losses[i] = -change

        avg_gain = np.zeros(len(data.Close))
        avg_loss = np.zeros(len(data.Close))

        avg_gain[period] = np.mean(gains[1 : period + 1])
        avg_loss[period] = np.mean(losses[1 : period + 1])

        for i in range(period + 1, len(data.Close)):
            avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gains[i]) / period
            avg_loss[i] = (avg_loss[i - 1] * (period - 1) + losses[i]) / period

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi


class FalseBreakoutReversal(Strategy):
    TP_PERCENTAGE = 5
    SL_PERCENTAGE = 7
    MAX_TRADE_DURATION = 12 * 60

    def init(self):
        self.sma = self.I(SMA, self.data.Close, 12)
        self.support = 0
        self.resistance = 0

    def find_sr_levels(self, data, lookback=10):
        recent_highs = data.High[-lookback:]
        recent_lows = data.Low[-lookback:]

        self.resistance = max(recent_highs)
        self.support = min(recent_lows)

    def next(self):
        # Получаем последние значения цен
        cp = self.data.Close[-1]
        hp = self.data.High[-1]
        lp = self.data.Low[-1]

        # Определяем уровни поддержки и сопротивления
        self.find_sr_levels(self.data)
        # print(f"{self.data.index[-1]} | CP={cp} > S={self.support} & LP={lp} < S={self.support} | CP={cp} < R={self.resistance} & HP={hp} > R={self.resistance}")

        sl = cp * (1 - self.SL_PERCENTAGE / 100)
        tp = cp * (1 + self.TP_PERCENTAGE / 100)
        sma_slope = self.sma[-1] - self.sma[-2]
        print(sma_slope)

        if lp <= self.support and cp >= self.support and sma_slope > 0:
            self.buy(sl=sl, tp=tp)
        elif hp >= self.resistance and cp <= self.resistance and sma_slope < 0:
            self.sell(sl=tp, tp=sl)

        for trade in self.trades:
            if (self.data.index[-1] - trade.entry_time).total_seconds() / 60 > self.MAX_TRADE_DURATION:
                trade.close()


class SMACrossoverStrategy(Strategy):
    TP_PERCENTAGE = 5
    SL_PERCENTAGE = 2
    MAX_TRADE_DURATION = 4 * 60

    def init(self):
        # Инициализируем скользящие средние, ADX и ATR
        self.sma_20 = self.I(SMA, self.data.Close, 20)
        self.sma_50 = self.I(SMA, self.data.Close, 50)
        self.adx = self.I(ADX, self.data.High, self.data.Low, self.data.Close, 14)
        self.atr = self.I(ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        cp = self.data.Close[-1]

        if crossover(self.sma_20, self.sma_50) and self.adx[-1] >= 10:
            sl = cp * (1 - self.SL_PERCENTAGE / 100)
            tp = cp * (1 + self.TP_PERCENTAGE / 100)
            self.buy(sl=sl, tp=tp)
        elif crossover(self.sma_50, self.sma_20) and self.adx[-1] >= 10:
            sl = cp * (1 + self.SL_PERCENTAGE / 100)
            tp = cp * (1 - self.TP_PERCENTAGE / 100)
            self.sell(sl=sl, tp=tp)

        for trade in self.trades:
            if (self.data.index[-1] - trade.entry_time).total_seconds() / 60 > self.MAX_TRADE_DURATION:
                trade.close()
