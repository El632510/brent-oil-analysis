"""
Functions for loading and cleaning the Brent oil price dataset.
The raw CSV has an annoying quirk: dates before ~2017 are formatted like
"20-May-87", while more recent rows are formatted like "Nov 08, 2022".
pandas can't parse both with a single format string, so we handle them
in two passes.
"""
import pandas as pd
import numpy as np


def load_raw_prices(path: str) -> pd.DataFrame:
    """
    Load the raw Brent oil price CSV and return a clean, sorted DataFrame
    with a proper datetime index.

    Args:
        path: path to the raw CSV file (Date, Price columns)

    Returns:
        DataFrame with columns ['Date', 'Price'], sorted by date ascending
    """
    df = pd.read_csv(path)

    # two different date formats show up in this file, so try the older
    # format first and fall back to the newer one for whatever doesn't parse
    parsed_dates = pd.to_datetime(df["Date"], format="%d-%b-%y", errors="coerce")
    still_missing = parsed_dates.isna()
    parsed_dates[still_missing] = pd.to_datetime(
        df.loc[still_missing, "Date"], format="%b %d, %Y", errors="coerce"
    )
    df["Date"] = parsed_dates

    if df["Date"].isna().any():
        bad_rows = df[df["Date"].isna()]
        raise ValueError(f"Could not parse {len(bad_rows)} date(s), e.g:\n{bad_rows.head()}")

    df = df.sort_values("Date").reset_index(drop=True)
    return df


def add_log_returns(df: pd.DataFrame, price_col: str = "Price") -> pd.DataFrame:
    """
    Add a log_return column to the DataFrame: log(price_t) - log(price_t-1).
    This is what we'll actually model in Task 2 since raw prices are not
    stationary but log returns roughly are.
    """
    df = df.copy()
    df["log_price"] = np.log(df[price_col])
    df["log_return"] = df["log_price"].diff()
    return df


def validate_columns(df: pd.DataFrame, required_columns=("Date", "Price")) -> None:
    """Raise an error if any required column is missing."""
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required column(s): {missing}")


def check_missing_values(df: pd.DataFrame) -> pd.Series:
    """
    Return a Series with the count of missing values per column.
    Doesn't raise or drop anything, just reports so the caller can decide.
    """
    missing_counts = df.isna().sum()
    if missing_counts.any():
        print(f"Warning: missing values found:\n{missing_counts[missing_counts > 0]}")
    return missing_counts


def check_duplicates(df: pd.DataFrame, subset="Date") -> int:
    """
    Report duplicate dates. Duplicates are only logged here, not removed,
    since deciding how to handle them (keep first, average, etc.) is an
    analysis decision, not a loading decision.
    """
    duplicate_count = df.duplicated(subset=subset).sum()
    if duplicate_count > 0:
        print(f"Warning: {duplicate_count} duplicate {subset} value(s) found.")
    return duplicate_count


def check_price_values(df: pd.DataFrame, price_col: str = "Price") -> None:
    """Flag non-numeric or non-positive prices without dropping anything."""
    non_numeric_count = pd.to_numeric(df[price_col], errors="coerce").isna().sum()
    if non_numeric_count > 0:
        print(f"Warning: {non_numeric_count} non-numeric {price_col} value(s) found.")

    non_positive_count = (df[price_col] <= 0).sum()
    if non_positive_count > 0:
        print(f"Warning: {non_positive_count} non-positive {price_col} value(s) found.")


def load_and_validate_prices(path: str) -> pd.DataFrame:
    """
    Full loading pipeline: load raw prices, validate columns, check for
    missing values, duplicates, and bad prices, then return the clean,
    sorted DataFrame with log returns added.
    """
    df = load_raw_prices(path)
    validate_columns(df)
    check_missing_values(df)
    check_duplicates(df)
    check_price_values(df)
    df = add_log_returns(df)
    return df


if __name__ == "__main__":
    # quick manual check when running this file directly
    prices = load_raw_prices("data/raw/BrentOilPrices.csv")
    prices = add_log_returns(prices)
    print(prices.head())
    print(prices.tail())
    print(f"\nDate range: {prices['Date'].min().date()} to {prices['Date'].max().date()}")
    print(f"Total rows: {len(prices)}")