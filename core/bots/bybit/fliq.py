from time import sleep
from typing import Any, Dict, List

from core.scripts.tools.logger import ANSI_COLORS, BLINK, RESET
from pybit.unified_trading import WebSocket

WS = WebSocket(testnet=False, channel_type="linear")

PINK = ANSI_COLORS["fg"]["pink"]
GREEN = ANSI_COLORS["bg"]["green"]
RED = ANSI_COLORS["bg"]["red"]
BLACK = ANSI_COLORS["fg"]["black"]


def sum_trades(trades: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Summarize trades

    Params:
        trades: List of trades
    """
    summary = {"buys": 0, "sells": 0}

    for trade in trades:
        vol = float(trade["v"]) * float(trade["p"])

        if trade["S"] == "Buy":
            summary["buys"] += vol
        elif trade["S"] == "Sell":
            summary["sells"] += vol

    return summary


def handle_trade(message):
    trade_summary = sum_trades(message["data"])
    buys, sells = round(trade_summary["buys"]), round(trade_summary["sells"])

    if buys > V1 and buys < V2:
        print(f"{GREEN}{BLACK}{SYMBOL} |  BUY: ${buys}{RESET}")
    if sells > V1 and sells < V2:
        print(f"{RED}{BLACK}{SYMBOL} | SELL: ${sells}{RESET}")

    if buys > V2:
        print(f"{BLINK}{GREEN}{BLACK}{SYMBOL} |  BUY: ${round(buys/1000, 1)}k{RESET}")
    if sells > V2:
        print(f"{BLINK}{RED}{BLACK}{SYMBOL} | SELL: ${round(sells/1000, 1)}k{RESET}")


def snipe(symbol: str):
    WS.trade_stream(symbol=symbol, callback=handle_trade)

    while True:
        sleep(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="WIFUSDT")
    parser.add_argument("--v1", type=int, required=False, default=1000)
    parser.add_argument("--v2", type=int, required=False, default=50000)

    args = parser.parse_args()
    SYMBOL: str = args.symbol.upper()
    V1 = args.v1
    V2 = args.v2

    try:
        snipe(SYMBOL)
    except KeyboardInterrupt:
        print(f"{PINK}bye-bye!{RESET}")
