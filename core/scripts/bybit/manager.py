from config import BYBIT_CONFIG_PATH, BYBIT_DATA_PATH
from core.scripts.bybit.api import get_kline, get_symbol_info
from core.scripts.tools.files import read_file
from core.scripts.tools.logger import get_logger
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
    logger.debug("BEGIN")

    data = get_kline(category=category, symbol=symbol, interval=interval, start=start, end=end)

    config = MARKET_CONFIG["kline"]
    packed_data = pack_data(
        data["result"]["list"],
        config["columns"],
        {"category": category, "symbol": symbol, "interval": interval},
    )

    file_name = config["file_name"].format(symbol=symbol, category=category, interval=interval)
    packed_data.to_csv(f"{BYBIT_DATA_PATH}kline/{file_name}", index=False)

    logger.debug("END")
    return file_name


def import_bybit_symbol_info(category: str = "spot", symbol: str = None) -> str:
    """
    Imports symbol info from the Bybit API.

    Params:
        category: Product type (spot, linear, inverse).
        symbol: Symbol name. Example: BTCUSDT
    """
    logger.debug("BEGIN")
    data = get_symbol_info(category=category, symbol=symbol)

    config = MARKET_CONFIG["symbol_info"]
    packed_data = pack_data(data["result"]["list"], config["columns"], {"category": category})

    file_name = config["file_name"].format(symbol=symbol, category=category)
    packed_data.to_csv(f"{BYBIT_DATA_PATH}info/{file_name}", index=False)

    logger.debug("END")
    return file_name
