from config import BYBIT_CONFIG_PATH, BYBIT_DWH_PATH
from core.scripts.bybit.api import get_kline
from core.scripts.tools.dtt import to_format
from core.scripts.tools.files import read_file
from core.scripts.tools.logger import get_logger
from core.scripts.tools.packers import pack_data

logger = get_logger(__name__)

MARKET_CONFIG = read_file(f"{BYBIT_CONFIG_PATH}market.json", is_json=True)

DTT_FORMAT = "%Y-%m-%d %H:%M:%S"
CSV_DTT_FORMAT = "%Y-%m-%dT%H-%M-%S"


def import_bybit_kline(symbol: str, interval: str, start: str, end: str, category: str = "spot") -> None:
    """
    Imports candle stick data from the Bybit API.

    Params:
        symbol: Symbol name. Example: BTCUSDT
        interval: Kline interval. 1,3,5,15,30,60,120,240,360,720,D,M,W
        start: Datetime from which to start. Format: "YYYY-MM-DD HH:MM:SS"
        end: Datetime until which to end. Format: "YYYY-MM-DD HH:MM:SS"
        category: Product type (spot, linear, inverse).
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


if __name__ == "__main__":
    import_bybit_kline(symbol="BTCUSDT", interval="D", start="2024-09-01 00:00:00", end="2024-09-14 00:00:00")
