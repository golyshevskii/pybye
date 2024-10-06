import pandas as pd
from config import MEXC_CONFIG_PATH, MEXC_DATA_PATH
from core.scripts.mexc.api import get_ticker_24h
from core.scripts.tools.files import read_file

MCONFIG = read_file(f"{MEXC_CONFIG_PATH}market.json", is_json=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="BTCUSDT")

    args = parser.parse_args()
    SYMBOL = args.symbol.upper()

    data = get_ticker_24h(SYMBOL)

    file_name = MCONFIG["ticker24h"]["file_name"].format(symbol=SYMBOL)
    pd.DataFrame([data] if isinstance(data, dict) else data).to_csv(
        f"{MEXC_DATA_PATH}24h/{file_name}", index=False
    )
