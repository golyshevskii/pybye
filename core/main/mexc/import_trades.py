from config import MEXC_CONFIG_PATH
from core.scripts.mexc.api import get_strades
from core.scripts.tools.files import read_file

MCONFIG = read_file(f"{MEXC_CONFIG_PATH}market.json", is_json=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="BTCUSDT")
    parser.add_argument("--limit", type=int, required=False, default=100)

    args = parser.parse_args()
    SYMBOL = args.symbol.upper()
    LIMIT = args.limit

    data = get_strades(SYMBOL, limit=LIMIT)
    print(data)
