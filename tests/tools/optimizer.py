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
        TP_PERCENTAGE=range(1, 12, 1),
        SL_PERCENTAGE=range(1, 6, 1),
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
