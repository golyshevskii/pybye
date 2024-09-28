import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from backtesting import Backtest
from config import BYBIT_DATA_PATH
from core.scripts.tools.logger import get_logger
from tests.tools.backtest import BreakoutStrategy

logger = get_logger(__name__)


def optimize(bt: Backtest):
    """
    Optimize the TP and SL percentages

    Params:
        bt: The Backtest object
    """
    optimizer, heatmap = bt.optimize(
        TP_PERCENTAGE=range(1, 10, 1),
        SL_PERCENTAGE=range(1, 5, 1),
        maximize="Equity Final [$]",
        return_heatmap=True,
    )
    logger.info(f"\n\n{'='*20} STATS {'='*20}\n{optimizer}\n\n{'='*20} SL & TP {'='*20}\n{heatmap}\n\n")

    heatmap = heatmap.reset_index(name="Equity_Final")
    heatmap = heatmap.pivot(index="TP_PERCENTAGE", columns="SL_PERCENTAGE", values="Equity_Final")

    # Create the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={"label": "Equity Final [$]"})
    plt.title("Equity Final Heatmap for TP and SL Percentages")
    plt.xlabel("SL Percentage")
    plt.ylabel("TP Percentage")
    plt.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, required=False, default="BTCUSDT")

    args = parser.parse_args()
    SYMBOL = args.symbol

    D_kline = pd.read_csv(f"{BYBIT_DATA_PATH}kline/bybit_kline_{SYMBOL}_spot_D.csv")
    H_kline = pd.read_csv(f"{BYBIT_DATA_PATH}kline/bybit_kline_{SYMBOL}_spot_60.csv")

    # Convert start_time to datetime and set it as index for better results in the backtest
    D_kline["start_time"] = pd.to_datetime(D_kline["start_time"], unit="ms", utc=True)
    D_kline.set_index("start_time", inplace=True)
    D_kline.sort_index(inplace=True, ascending=True)

    H_kline["start_time"] = pd.to_datetime(H_kline["start_time"], unit="ms", utc=True)
    H_kline.set_index("start_time", inplace=True)
    H_kline.sort_index(inplace=True, ascending=True)

    # Renaming columns to match backtesting format
    H_kline = H_kline[["open_price", "high_price", "low_price", "close_price", "volume"]]
    H_kline.columns = ["Open", "High", "Low", "Close", "Volume"]

    # Run the backtest
    bs = BreakoutStrategy
    bs.RL = D_kline["resistance"]

    bt = Backtest(H_kline, bs, cash=100, commission=0.01)
    # optimize(bt)

    stats = bt.run()
    logger.info(f"{SYMBOL}\n{stats}")
    bt.plot()
