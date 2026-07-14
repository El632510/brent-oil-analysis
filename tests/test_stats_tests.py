import numpy as np
import pandas as pd
import pytest

from src.stats_tests import run_adf_test, rolling_stats


def test_run_adf_test_detects_stationary_series():
    rng = np.random.default_rng(42)
    stationary_series = pd.Series(rng.normal(0, 1, 500))

    result = run_adf_test(stationary_series, "white_noise")

    assert result["is_stationary"] is True
    assert result["p_value"] < 0.05


def test_run_adf_test_detects_non_stationary_series():
    trending_series = pd.Series(np.arange(500, dtype=float))

    result = run_adf_test(trending_series, "trend")

    assert result["is_stationary"] is False


def test_rolling_stats_returns_expected_columns():
    series = pd.Series(range(50), dtype=float)

    result = rolling_stats(series, window=10)

    assert "rolling_mean" in result.columns
    assert "rolling_std" in result.columns
    assert result["rolling_mean"].isna().sum() == 9
