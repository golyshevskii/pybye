import random
from typing import List

import pandas as pd
import pandas_ta as ta
from backtesting import Backtest
from core.scripts.mexc.manager import import_mexc_kline
from core.scripts.tools.logger import ANSI_COLORS, RESET
from deap import algorithms, base, creator, tools
from tests.strategy.breakout import BreakoutGE

# INDIVIDUALS PARAMS
GRAMMAR = {
    "rsi_period": [10, 14, 20, 25],
    "rsi_overbought": [60, 70, 80],
    "rsi_oversold": [20, 30, 40],
    "macd_fast": [10, 12, 15],
    "macd_slow": [26, 30, 35],
    "macd_signal": [9, 10, 12],
    "lookback_period": [10, 20, 30],
}


def get_kline(symbol: str, interval: str) -> pd.DataFrame:
    kline = import_mexc_kline(symbol=symbol, interval=interval)

    types = {"Open": float, "High": float, "Low": float, "Close": float, "Volume": float}
    kline = kline.astype(types)

    return kline


def create_individual() -> List[int]:
    return [
        random.choice(GRAMMAR["rsi_period"]),
        random.choice(GRAMMAR["rsi_overbought"]),
        random.choice(GRAMMAR["rsi_oversold"]),
        random.choice(GRAMMAR["macd_fast"]),
        random.choice(GRAMMAR["macd_slow"]),
        random.choice(GRAMMAR["macd_signal"]),
        random.choice(GRAMMAR["lookback_period"]),
    ]


def evaluate(individual) -> float:
    global KLINE

    rsi_period, rsi_overbought, rsi_oversold, macd_fast, macd_slow, macd_signal, lookback_period = individual

    if macd_fast <= 0 or macd_slow <= 0 or macd_signal <= 0:
        return (0,)

    geb = BreakoutGE
    geb.rsi_period = rsi_period
    geb.rsi_overbought = rsi_overbought
    geb.rsi_oversold = rsi_oversold
    geb.macd_fast = macd_fast
    geb.macd_slow = macd_slow
    geb.macd_signal = macd_signal
    geb.lookback_period = lookback_period

    KLINE["RSI"] = ta.rsi(KLINE["Close"], length=rsi_period)
    macd = ta.macd(KLINE["Close"], fast=macd_fast, slow=macd_slow, signal=macd_signal)

    KLINE["MACD_line"] = macd[f"MACD_{macd_fast}_{macd_slow}_{macd_signal}"]
    KLINE["MACD_signal"] = macd[f"MACDs_{macd_fast}_{macd_slow}_{macd_signal}"]
    KLINE = KLINE.dropna(subset=["Close"])

    bt = Backtest(KLINE, geb, cash=100, commission=0.002, trade_on_close=True)
    stats = bt.run()
    return (stats["Equity Final [$]"],)


def run():

    # SETUP toolbox
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # GENERATE INITIAL POPULATION
    population = toolbox.population(n=50)

    # RUN GE
    algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=10, verbose=True)

    # SELECT BEST INDIVIDUAL
    best_individual = tools.selBest(population, 1)[0]
    print(f"{ANSI_COLORS['bg']['pp']}BEST INDIVIDUAL: {best_individual}{RESET}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="BTC_USDT")
    parser.add_argument("--interval", type=str, required=False, default="Min15")

    args = parser.parse_args()
    SYMBOL = args.symbol.upper()
    INTERVAL = args.interval
    KLINE = get_kline(symbol=SYMBOL, interval=INTERVAL)

    # BEST INDIVIDUAL: [10, 80, 20, 15, 35, 10, 30]
    run()
