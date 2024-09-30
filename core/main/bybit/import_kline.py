from core.scripts.bybit.manager import import_bybit_kline

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="BTCUSDT")
    parser.add_argument("--interval", type=str, required=False, default="5")

    args = parser.parse_args()
    SYMBOL = args.symbol
    INTERVAL = args.interval

    _ = import_bybit_kline(symbol=SYMBOL, interval=INTERVAL)
