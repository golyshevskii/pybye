from backtesting import Strategy


class Scalp(Strategy):
    slcoef = 1.1
    TPSLRatio = 1.5
    rsi_length = 16

    def init(self):
        super().init()
        self.signal = self.I(self.SIGNAL)
        self.rsi = self.I(self.RSI)  # Assuming RSI is part of your data
        self.bbu = self.I(self.BBU)  # Upper Bollinger Band
        self.bbm = self.I(self.BBM)  # Middle Bollinger Band
        self.bbl = self.I(self.BBL)  # Lower Bollinger Band

    def next(self):
        super().next()
        slatr = self.slcoef * self.data.ATR[-1]
        TPSLRatio = self.TPSLRatio

        if len(self.trades) > 0:
            if self.trades[-1].is_long and self.data.RSI[-1] >= 90:
                self.trades[-1].close()
            elif self.trades[-1].is_short and self.data.RSI[-1] <= 10:
                self.trades[-1].close()

        if self.signal == 2 and len(self.trades) == 0:
            sl = self.data.Close[-1] - slatr
            tp = self.data.Close[-1] + slatr * TPSLRatio
            self.buy(sl=sl, tp=tp)

        elif self.signal == 1 and len(self.trades) == 0:
            sl = self.data.Close[-1] + slatr
            tp = self.data.Close[-1] - slatr * TPSLRatio
            self.sell(sl=sl, tp=tp)

    def SIGNAL(self):
        return self.data.signal

    def BBU(self):
        return self.data["BBU_20_2"]

    def BBM(self):
        return self.data["BBM_20_2"]

    def BBL(self):
        return self.data["BBL_20_2"]

    def RSI(self):
        return self.data["RSI"]
