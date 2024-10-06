import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

# BYBIT
BYBIT_DATA_PATH = "data/bybit/"
BYBIT_CONFIG_PATH = "configs/bybit/"
BYBIT_DEMO_API_KEY = os.getenv("BYBIT_DEMO_API_KEY")
BYBIT_DEMO_API_SECRET = os.getenv("BYBIT_DEMO_API_SECRET")

# MEXC
MEXC_DATA_PATH = "data/mexc/"
MEXC_CONFIG_PATH = "configs/mexc/"
MEXC_API_KEY = os.getenv("MEXC_API_KEY")
MEXC_API_SECRET = os.getenv("MEXC_API_SECRET")
