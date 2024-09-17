import pandas as pd
from config import BYBIT_CONFIG_PATH, BYBIT_DWH_PATH
from core.scripts.bybit.api import get_kline
from core.scripts.tools.dtt import CSV_DTT_FORMAT, DTT_FORMAT, to_format
from core.scripts.tools.files import read_file
from core.scripts.tools.logger import get_logger
from core.scripts.tools.metrics import calc_sr_levels
from core.scripts.tools.packers import pack_data

logger = get_logger(__name__)

MARKET_CONFIG = read_file(f"{BYBIT_CONFIG_PATH}market.json", is_json=True)


def import_bybit_kline(symbol: str, interval: str, start: str, end: str, category: str = "spot") -> str:
    """
    Imports candle stick data from the Bybit API.

    Params:
        symbol: Symbol name. Example: BTCUSDT
        interval: Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W
        start: Datetime from which to start. Format: "YYYY-MM-DD HH:MM:SS"
        end: Datetime until which to end. Format: "YYYY-MM-DD HH:MM:SS"
        category: Product type (spot, linear, inverse).

    Returns:
        file_name: Name of the file where the data is stored.
    """
    logger.info("BEGIN")

    data = get_kline(category=category, symbol=symbol, interval=interval, start=start, end=end)

    config = MARKET_CONFIG["kline"]
    packed_data = pack_data(
        data["result"]["list"],
        config["columns"],
        {"category": category, "symbol": symbol, "interval": interval},
    )

    file_name = config["file_name"].format(
        symbol=symbol,
        category=category,
        interval=interval,
        start=to_format(start, DTT_FORMAT, CSV_DTT_FORMAT),
        end=to_format(end, DTT_FORMAT, CSV_DTT_FORMAT),
    )
    packed_data.to_csv(f"{BYBIT_DWH_PATH}kline/{file_name}", index=False)

    logger.info("END")
    return file_name


if __name__ == "__main__":
    from_dtt = "2024-09-01 00:00:00"
    to_dtt = "2024-09-14 00:00:00"

    D_file = import_bybit_kline(symbol="BTCUSDT", interval="D", start=from_dtt, end=to_dtt)
    D_kline = pd.read_csv(f"{BYBIT_DWH_PATH}kline/{D_file}")
    D_kline = calc_sr_levels(D_kline, window_size=5)
    D_kline.to_csv(f"{BYBIT_DWH_PATH}kline/{D_file}", index=False)

    H_file = import_bybit_kline(symbol="BTCUSDT", interval="60", start=from_dtt, end=to_dtt)
    H_kline = pd.read_csv(f"{BYBIT_DWH_PATH}kline/{H_file}")
    H_kline = calc_sr_levels(H_kline, window_size=48)
    H_kline.to_csv(f"{BYBIT_DWH_PATH}kline/{H_file}", index=False)
