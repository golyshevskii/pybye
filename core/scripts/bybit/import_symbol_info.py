from core.scripts.bybit.manager import import_bybit_symbol_info

if __name__ == "__main__":
    # from datetime import datetime, timedelta
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default=None)

    args = parser.parse_args()
    SYMBOL = args.symbol

    _ = import_bybit_symbol_info(symbol=SYMBOL)
