from core.scripts.bybit.manager import scan_bybit_symbol

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default=None)
    parser.add_argument("--interval", type=str, required=False, default="15")
    parser.add_argument("--lookback", type=int, required=False, default=4)
    parser.add_argument("--max_symbols", type=int, required=False, default=50)

    args = parser.parse_args()
    SYMBOL = args.symbol
    INTERVAL = args.interval
    LOOKBACK = args.lookback
    MAX_SYMBOLS = args.max_symbols

    _ = scan_bybit_symbol(symbol=SYMBOL, interval=INTERVAL, lookback=LOOKBACK, max_symbols=MAX_SYMBOLS)
