import asyncio
from typing import List

from config import MEXC_API_KEY, MEXC_API_SECRET
from core.scripts.tools.logger import ANSI_COLORS, RESET
from pymexc import futures

WEBSOCKET = futures.WebSocket(api_key=MEXC_API_KEY, api_secret=MEXC_API_SECRET)
SYMBOLS = ["BTC_USDT", "SOL_USDT", "WIF_USDT", "FTN_USDT"]
PINK = ANSI_COLORS["fg"]["pink"]


async def liq(fweb_socket: futures.WebSocket, symbols: List[str]):
    async def liq_symbol(symbol: str):
        while True:
            data = await fweb_socket.deal_stream(callback=handle_message, symbol=symbol)
            print(f"{PINK}{symbol}{RESET}: {data}")

    tasks = [asyncio.create_task(liq_symbol(symbol)) for symbol in symbols]
    await asyncio.gather(*tasks)


def handle_message(message):
    print(message)


futures_client = futures.HTTP(api_key=MEXC_API_KEY, api_secret=MEXC_API_SECRET)
ws_futures_client = futures.WebSocket(api_key=MEXC_API_KEY, api_secret=MEXC_API_SECRET)

print(futures_client.index_price("MX_USDT"))
ws_futures_client.tickers_stream(handle_message)

while True:
    pass

# asyncio.run(liq(WEBSOCKET, SYMBOLS))
