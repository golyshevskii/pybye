from core.scripts.bybit.api import get_spot_asset_info

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--coin", type=str, required=False, default="USDT")

    args = parser.parse_args()
    COIN = args.coin

    print(get_spot_asset_info(coin=COIN))
