"""
Data access layer for the API. Routes call these functions instead of
reading files directly, so if the storage format ever changes (e.g. move
to a real database), only this file needs to change.
"""
import json
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"
RAW_EVENTS_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "events.csv"


def get_prices(start_date=None, end_date=None):
    """Load historical price data, optionally filtered by date range."""
    df = pd.read_csv(DATA_DIR / "full_prices.csv", parse_dates=["Date"])

    if start_date:
        df = df[df["Date"] >= start_date]
    if end_date:
        df = df[df["Date"] <= end_date]

    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    return df.to_dict(orient="records")


def get_change_point_results():
    """Load the precomputed Bayesian change point results."""
    with open(DATA_DIR / "change_point_results.json") as f:
        return json.load(f)


def get_events():
    """Load the researched events dataset."""
    df = pd.read_csv(RAW_EVENTS_PATH, parse_dates=["event_date"])
    df["event_date"] = df["event_date"].dt.strftime("%Y-%m-%d")
    return df.to_dict(orient="records")


def get_summary_stats():
    """Load the precomputed summary statistics."""
    with open(DATA_DIR / "summary_stats.json") as f:
        return json.load(f)
