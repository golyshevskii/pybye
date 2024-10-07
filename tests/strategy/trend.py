import talib
from backtesting import Strategy
from backtesting.lib import crossover


class MeanReversionTrendStrategy(Strategy):
    SL_PERCENTAGE = 2
    TP_PERCENTAGE = 6
    RSI_PERIOD = 21
    SEMA_PERIOD = 5
    LEMA_PERIOD = 20
    LRSI_THRESHOLD = 50
    SRSI_THRESHOLD = 50

    def init(self):
        # Инициализация индикаторов
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.RSI_PERIOD)
        self.sema = self.I(talib.EMA, self.data.Close, timeperiod=self.SEMA_PERIOD)
        self.lema = self.I(talib.EMA, self.data.Close, timeperiod=self.LEMA_PERIOD)

    def next(self):
        cp = self.data.Close[-1]

        for trade in self.trades:
            sema = self.sema[-1]
            lema = self.lema[-1]
            diff_percent = abs(sema - lema) / lema * 100

            if trade.is_long:
                reverse_cross = crossover(self.lema, self.sema)
            else:
                reverse_cross = crossover(self.sema, self.lema)

            if diff_percent > 10 or reverse_cross:
                trade.close()

        if crossover(self.sema, self.lema):
            # LONG
            if self.rsi[-1] < self.LRSI_THRESHOLD:
                sl = cp * (1 - self.SL_PERCENTAGE / 100)
                tp = cp * (1 + self.TP_PERCENTAGE / 100)
                self.buy(sl=sl, tp=tp)
        elif crossover(self.lema, self.sema):
            # SHORT
            if self.rsi[-1] > self.SRSI_THRESHOLD:
                sl = cp * (1 + self.SL_PERCENTAGE / 100)
                tp = cp * (1 - self.TP_PERCENTAGE / 100)
                self.sell(sl=sl, tp=tp)
