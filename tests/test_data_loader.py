import sys
import os

import pandas as pd
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from data_loader import load_raw_prices, add_log_returns


@pytest.fixture
def sample_csv(tmp_path):
    """Build a tiny CSV with both date formats mixed in, like the real file."""
    csv_content = (
        "Date,Price\n"
        "20-May-87,18.63\n"
        "21-May-87,18.45\n"
        "\"Nov 08, 2022\",96.85\n"
        "\"Nov 09, 2022\",93.05\n"
    )
    file_path = tmp_path / "sample_prices.csv"
    file_path.write_text(csv_content)
    return str(file_path)


def test_load_raw_prices_parses_both_date_formats(sample_csv):
    df = load_raw_prices(sample_csv)

    assert len(df) == 4
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])


def test_load_raw_prices_sorts_by_date(sample_csv):
    df = load_raw_prices(sample_csv)

    assert df["Date"].is_monotonic_increasing


def test_load_raw_prices_raises_on_bad_date(tmp_path):
    bad_csv = tmp_path / "bad_prices.csv"
    bad_csv.write_text("Date,Price\nnot-a-date,10.0\n")

    with pytest.raises(ValueError):
        load_raw_prices(str(bad_csv))


def test_add_log_returns_first_row_is_nan(sample_csv):
    df = load_raw_prices(sample_csv)
    df = add_log_returns(df)

    assert pd.isna(df["log_return"].iloc[0])
    assert df["log_return"].iloc[1:].notna().all()


def test_add_log_returns_values_are_reasonable(tmp_path):
    # use consecutive days here, unlike sample_csv which deliberately jumps
    # decades to test date parsing - a 35 year gap would make log returns
    # meaningless for this particular check
    csv_content = (
        "Date,Price\n"
        "20-May-87,18.63\n"
        "21-May-87,18.45\n"
        "22-May-87,18.55\n"
    )
    file_path = tmp_path / "consecutive_prices.csv"
    file_path.write_text(csv_content)

    df = load_raw_prices(str(file_path))
    df = add_log_returns(df)

    # daily oil price moves shouldn't be more than +/- 50% in log terms
    assert df["log_return"].dropna().abs().max() < 0.5
