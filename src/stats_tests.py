"""
Statistical tests used to justify modeling choices before the Bayesian
change point model is built.
"""
import pandas as pd
from statsmodels.tsa.stattools import adfuller


def run_adf_test(series: pd.Series, series_name: str = "series") -> dict:
    """
    Run the Augmented Dickey-Fuller test for stationarity.

    Null hypothesis: the series has a unit root (i.e. it is non-stationary).
    A small p-value (typically < 0.05) lets us reject that and treat the
    series as stationary.

    Returns a dict with the test statistic, p-value, and a plain-English
    verdict so this can be dropped straight into a report or notebook cell.
    """
    clean_series = series.dropna()
    result = adfuller(clean_series)

    adf_stat, p_value, used_lag, n_obs, critical_values, _ = result
    is_stationary = p_value < 0.05

    verdict = (
        f"{series_name} is stationary (p={p_value:.4g})"
        if is_stationary
        else f"{series_name} is NOT stationary (p={p_value:.4g})"
    )

    return {
        "series_name": series_name,
        "adf_statistic": adf_stat,
        "p_value": p_value,
        "used_lag": used_lag,
        "n_obs": n_obs,
        "critical_values": critical_values,
        "is_stationary": is_stationary,
        "verdict": verdict,
    }


def rolling_stats(series: pd.Series, window: int = 30) -> pd.DataFrame:
    """Compute rolling mean and rolling standard deviation for a series."""
    return pd.DataFrame({
        "rolling_mean": series.rolling(window).mean(),
        "rolling_std": series.rolling(window).std(),
    })
