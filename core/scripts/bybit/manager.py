import pandas as pd
from config import BYBIT_CONFIG_PATH, BYBIT_DWH_PATH
from core.scripts.bybit.api import get_kline
from core.scripts.tools.dtt import from_unix
from core.scripts.tools.files import read_file
from core.scripts.tools.logger import get_logger
from core.scripts.tools.metrics import calc_psr_levels
from core.scripts.tools.packers import pack_data

logger = get_logger(__name__)

MARKET_CONFIG = read_file(f"{BYBIT_CONFIG_PATH}market.json", is_json=True)


def import_bybit_kline(
    symbol: str, interval: str, start: str = None, end: str = None, category: str = "spot"
) -> str:
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

    file_name = config["file_name"].format(symbol=symbol, category=category, interval=interval)
    packed_data.to_csv(f"{BYBIT_DWH_PATH}kline/{file_name}", index=False)

    logger.info("END")
    return file_name


if __name__ == "__main__":
    # from datetime import datetime, timedelta

    # from_dtt = (datetime.now() - timedelta(days=14)).strftime(DTT_FORMAT)
    # to_dtt = datetime.now().strftime(DTT_FORMAT)

    from_dtt, to_dtt = None, None

    D_file = import_bybit_kline(symbol="BTCUSDT", interval="D", start=from_dtt, end=to_dtt)
    D_kline = pd.read_csv(f"{BYBIT_DWH_PATH}kline/{D_file}")

    D_kline = calc_psr_levels(D_kline)
    D_kline["dtt"] = D_kline["start_time"].apply(lambda x: from_unix(x))

    D_kline.to_csv(f"{BYBIT_DWH_PATH}kline/{D_file}", index=False)

    H_file = import_bybit_kline(symbol="BTCUSDT", interval="60", start=from_dtt, end=to_dtt)
    H_kline = pd.read_csv(f"{BYBIT_DWH_PATH}kline/{H_file}")

    H_kline = calc_psr_levels(H_kline)
    H_kline["dtt"] = H_kline["start_time"].apply(lambda x: from_unix(x))

    H_kline.to_csv(f"{BYBIT_DWH_PATH}kline/{H_file}", index=False)
