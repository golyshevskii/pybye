import os
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(base_dir, '.env'))

# BYBIT
BYBIT_DWH_PATH = "dwh/bybit/"
BYBIT_CONFIG_PATH = "configs/bybit/"
BYBIT_DEMO_API_KEY = os.getenv("BYBIT_DEMO_API_KEY")
BYBIT_DEMO_API_SECRET = os.getenv("BYBIT_DEMO_API_SECRET")
