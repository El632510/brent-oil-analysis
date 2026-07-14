"""
Match a detected change point date against the researched events dataset,
and express the model's mu_1/mu_2 shift as numbers a stakeholder can act on.
"""
import numpy as np
import pandas as pd


def load_events(path: str) -> pd.DataFrame:
    """Load the events CSV and parse event_date to datetime."""
    events = pd.read_csv(path)
    events["event_date"] = pd.to_datetime(events["event_date"])
    return events


def find_nearest_events(change_point_date, events: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    """
    Rank events by how close their date is to the detected change point.
    Returns the top_n closest events with a days_from_change_point column.
    """
    events = events.copy()
    events["days_from_change_point"] = (events["event_date"] - change_point_date).dt.days
    events["abs_days"] = events["days_from_change_point"].abs()
    nearest = events.sort_values("abs_days").head(top_n)
    return nearest.drop(columns="abs_days")


def summarize_price_shift(prices: pd.DataFrame, change_point_date, price_col="Price") -> dict:
    """
    Compute the average raw price before and after the change point date,
    since stakeholders think in dollars per barrel, not log return units.
    """
    before = prices[prices["Date"] < change_point_date][price_col]
    after = prices[prices["Date"] >= change_point_date][price_col]

    avg_before = before.mean()
    avg_after = after.mean()
    pct_change = ((avg_after - avg_before) / avg_before) * 100

    return {
        "avg_price_before": round(avg_before, 2),
        "avg_price_after": round(avg_after, 2),
        "pct_change": round(pct_change, 2),
    }


def build_impact_report(change_point_result: dict, prices: pd.DataFrame,
                         events: pd.DataFrame) -> dict:
    """
    Combine the change point date, nearby events, and the price shift into
    a single dict that's easy to render in a notebook, report, or API.
    """
    change_date = change_point_result["change_point_date"] \
        if "change_point_date" in change_point_result else change_point_result["tau_date"]

    nearby_events = find_nearest_events(change_date, events)
    price_shift = summarize_price_shift(prices, change_date)

    return {
        "change_point_date": str(change_date.date()),
        "likely_associated_events": nearby_events.to_dict(orient="records"),
        "price_shift": price_shift,
    }
