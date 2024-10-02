import pandas as pd


def calc_ema_ls_signals(df: pd.DataFrame, kline_rn: int, lookback: int):
    """Calculates the EMA Long/Short signals"""
    start = max(0, kline_rn - lookback)
    end = kline_rn
    rows = df.iloc[start:end]

    # Check if all fast EMA values are below or above slow EMA
    if all(rows["FEMA"] > rows["SEMA"]):
        return 2  # LONG
    elif all(rows["FEMA"] < rows["SEMA"]):
        return 1  # SHORT

    return 0


def set_scalp_signal(df: pd.DataFrame, kline_rn: int, lookback: int, **kwargs):
    """
    Sets scalping signals based on the Bollinger Bands and EMA.

    Params:
        df: DataFrame containing the kline data
        kline_rn: Row number of the current candle
        lookback: Lookback period for the signal
    Returns:
        2 for LONG, 1 for SHORT, 0 for NO SIGNAL
    """
    bbl = f'BBL_{kwargs["bbands_len"]}_{kwargs["bbands_std"]}'
    bbu = f'BBU_{kwargs["bbands_len"]}_{kwargs["bbands_std"]}'

    if calc_ema_ls_signals(df, kline_rn, lookback) == 2 and df.Close[kline_rn] <= df[bbl][kline_rn]:
        # and df.RSI[current_candle]<60
        return 2
    if calc_ema_ls_signals(df, kline_rn, lookback) == 1 and df.Close[kline_rn] >= df[bbu][kline_rn]:
        # and df.RSI[current_candle]>40
        return 1
    return 0
