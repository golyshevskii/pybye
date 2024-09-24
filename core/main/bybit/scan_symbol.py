from core.scripts.bybit.manager import scan_bybit_symbol

if __name__ == "__main__":
    # from datetime import datetime, timedelta
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default=None)

    args = parser.parse_args()
    SYMBOL = args.symbol

    _ = scan_bybit_symbol(symbol=SYMBOL)
