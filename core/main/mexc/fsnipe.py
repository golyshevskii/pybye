import time

from core.scripts.mexc.api import get_depth, get_fticker, get_ftrades
from core.scripts.tools.logger import ANSI_COLORS, RESET

DEPTH_LIMIT = 100


def snipe_symbol(symbol: str):
    order_book = get_depth(symbol, limit=DEPTH_LIMIT)["data"]
    trades = get_ftrades(symbol=symbol, limit=DEPTH_LIMIT)["data"]
    ticker = get_fticker(symbol=symbol)["data"]

    asks = order_book["asks"]
    bids = order_book["bids"]

    total_ask_volume = sum([ask[1] for ask in asks])
    total_bid_volume = sum([bid[1] for bid in bids])

    order_book_imbalance = total_bid_volume - total_ask_volume

    total_buy_volume, total_sell_volume = 0, 0
    for trade in trades:
        if trade["T"] == 1:
            total_buy_volume += trade["v"]
        elif trade["T"] == 2:
            total_sell_volume += trade["v"]

    rise_fall_rate = ticker["riseFallRate"]
    last_price = ticker["lastPrice"]

    signal = None
    if order_book_imbalance > 0 and total_buy_volume > total_sell_volume and rise_fall_rate > 0:
        signal = f"LONG | PRICE: {last_price} B.VOL: {total_buy_volume} IMB: {order_book_imbalance} RF-RATE: {rise_fall_rate}"
        print(f"{ANSI_COLORS['bg']['green']}{signal}{RESET}")

    elif order_book_imbalance < 0 and total_sell_volume > total_buy_volume and rise_fall_rate < 0:
        signal = f"SHORT | PRICE: {last_price} S.VOL: {total_sell_volume} IMB: {order_book_imbalance} RF-RATE: {rise_fall_rate}"
        print(f"{ANSI_COLORS['bg']['red']}{signal}{RESET}")

    else:
        signal = f"NONE | PRICE: {last_price} S.VOL: {total_sell_volume} B.VOL: {total_buy_volume} IMB: {order_book_imbalance} RF.RATE: {rise_fall_rate}"
        print(f"{ANSI_COLORS['bg']['yellow']}{signal}{RESET}")

    return signal


def snipe():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="WIF_USDT")

    args = parser.parse_args()
    SYMBOL: str = args.symbol.upper()

    print(f"SNIPING: {ANSI_COLORS['fg']['pink']}{SYMBOL.replace('_', '')}{RESET}")

    while True:
        snipe_symbol(SYMBOL)
        time.sleep(1)


snipe()
