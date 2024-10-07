import matplotlib.pyplot as plt
import seaborn as sns
from backtesting import Backtest
from core.scripts.tools.logger import get_logger

logger = get_logger(__name__)


def optimize(bt: Backtest):
    """
    Optimize the TP and SL percentages

    Params:
        bt: The Backtest object
    """
    optimizer, heatmap = bt.optimize(
        TP_PERCENTAGE=range(1, 25, 1),
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


def optimize_mrtfs(bt: Backtest):
    """
    Optimize the TP and SL percentages

    Params:
        bt: The Backtest object
    """
    optimizer, heatmap = bt.optimize(
        TP_PERCENTAGE=range(3, 15, 2),
        SL_PERCENTAGE=range(1, 5, 1),
        RSI_PERIOD=range(7, 22, 7),
        LEMA_PERIOD=range(20, 51, 10),
        SEMA_PERIOD=range(5, 16, 5),
        LRSI_THRESHOLD=range(30, 46, 5),
        SRSI_THRESHOLD=range(50, 81, 5),
        maximize="Equity Final [$]",
        return_heatmap=True,
    )

    # heatmap = heatmap.reset_index(name="Equity_Final")
    # heatmap = heatmap.pivot(index="TP_PERCENTAGE", columns="SL_PERCENTAGE", values="Equity_Final")

    # # Create the heatmap
    # plt.figure(figsize=(10, 6))
    # sns.heatmap(heatmap, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={"label": "Equity Final [$]"})
    # plt.title("Equity Final Heatmap for TP and SL Percentages")
    # plt.xlabel("SL Percentage")
    # plt.ylabel("TP Percentage")
    # plt.show()

    return optimizer, heatmap
