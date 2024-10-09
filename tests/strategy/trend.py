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


class EMATrend(Strategy):
    RP = 1.0
    TPP = 10
    SLP = 3
    EMA_PERIOD = 50
    LOOKBACK = 5

    def init(self):
        self.ema = self.I(talib.EMA, self.data.Close, timeperiod=self.EMA_PERIOD)

    def set_stop_loss(self, direction):
        if direction == 1:
            low_swing = self.data.Close[-self.LOOKBACK :].min()
            sl = low_swing * (1 - self.SLP / 100)
        elif direction == -1:
            high_swing = self.data.Close[-self.LOOKBACK :].max()
            sl = high_swing * (1 + self.SLP / 100)
        return sl

    def risk_vol(self):
        return self.equity * (self.RP / 100)

    def next(self):
        cp = self.data.Close[-1]

        for trade in self.trades:
            if trade.is_long:
                nsl = self.set_stop_loss(1)
                trade.sl = nsl if nsl > trade.sl else trade.sl
            else:
                nsl = self.set_stop_loss(-1)
                trade.sl = nsl if nsl < trade.sl else trade.sl

        if crossover(self.data.Close, self.ema):
            # LONG
            sl = self.set_stop_loss(1)
            tp = cp * (1 + self.TPP / 100)

            qty = round(float(self.risk_vol() / (cp - sl)))
            qty = max(1, qty)
            print(
                f"{self.data.index[-1]}| LONG - Risk Vol: {self.risk_vol()}, SL: {sl}, TP: {tp}, Qty: {qty}"
            )
            self.buy(sl=sl, tp=tp)

        elif crossover(self.ema, self.data.Close):
            # SHORT
            sl = self.set_stop_loss(-1)
            tp = cp * (1 - self.TPP / 100)

            qty = round(float(self.risk_vol() / (sl - cp)))
            qty = max(1, qty)
            print(
                f"{self.data.index[-1]}| SHORT - Risk Vol: {self.risk_vol()}, SL: {sl}, TP: {tp}, Qty: {qty}"
            )
            self.sell(sl=sl, tp=tp)


class BBMA(Strategy):
    TPP = 10
    SLP = 3
    MAP = 3
    LOOKBACK = 3

    def init(self):
        self.ma = self.I(talib.MA, self.data.Close, timeperiod=self.MAP)

    def set_stop_loss(self, direction):
        if direction == 1:
            low_swing = self.data.Close[-self.LOOKBACK :].min()
            sl = low_swing * (1 - self.SLP / 100)
        elif direction == -1:
            high_swing = self.data.Close[-self.LOOKBACK :].max()
            sl = high_swing * (1 + self.SLP / 100)
        return sl

    def next(self):
        cp1, cp2 = self.data.Close[-1], self.data.Close[-2]
        cma = self.ma[-1]
        bbu1, bbu2 = self.bbu[-1], self.bbu[-2]
        bbl1, bbl2 = self.bbl[-1], self.bbl[-2]

        if cp2 < bbu2 and cp1 > bbu1:
            # SHORT
            sl = self.set_stop_loss(-1)
            tp = cp1 * (1 - self.TPP / 100)

            qty = round(float(self.risk_vol() / (sl - cp1)))
            qty = max(1, qty)
            print(
                f"{self.data.index[-1]}| SHORT - Risk Vol: {self.risk_vol()}, SL: {sl}, TP: {tp}, Qty: {qty}"
            )
            self.sell(sl=sl, tp=tp)

        elif cp2 > bbl2 and cp1 < bbl1:
            # LONG
            sl = self.set_stop_loss(1)
            tp = cp1 * (1 + self.TPP / 100)

            qty = round(float(self.risk_vol() / (cp1 - sl)))
            qty = max(1, qty)
            print(
                f"{self.data.index[-1]}| LONG - Risk Vol: {self.risk_vol()}, SL: {sl}, TP: {tp}, Qty: {qty}"
            )
            self.buy(sl=sl, tp=tp)
