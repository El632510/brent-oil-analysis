import pandas as pd
import pytest

from src.event_analysis import find_nearest_events, summarize_price_shift, build_impact_report


@pytest.fixture
def sample_events():
    return pd.DataFrame({
        "event_date": pd.to_datetime(["2020-01-01", "2020-04-20", "2021-06-01"]),
        "event_name": ["Event A", "Event B", "Event C"],
        "category": ["cat1", "cat2", "cat3"],
        "description": ["desc A", "desc B", "desc C"],
    })


@pytest.fixture
def sample_prices():
    dates = pd.date_range("2020-01-01", periods=10, freq="D")
    prices = [50, 50, 50, 50, 50, 30, 30, 30, 30, 30]
    return pd.DataFrame({"Date": dates, "Price": prices})


def test_find_nearest_events_orders_by_distance(sample_events):
    change_point = pd.Timestamp("2020-04-21")

    nearest = find_nearest_events(change_point, sample_events, top_n=2)

    assert nearest.iloc[0]["event_name"] == "Event B"
    assert len(nearest) == 2


def test_summarize_price_shift_computes_correct_averages(sample_prices):
    change_point = pd.Timestamp("2020-01-06")

    result = summarize_price_shift(sample_prices, change_point)

    assert result["avg_price_before"] == 50.0
    assert result["avg_price_after"] == 30.0
    assert result["pct_change"] == -40.0


def test_build_impact_report_combines_events_and_price_shift(sample_prices, sample_events):
    change_point_result = {"change_point_date": pd.Timestamp("2020-01-06")}

    report = build_impact_report(change_point_result, sample_prices, sample_events)

    assert report["change_point_date"] == "2020-01-06"
    assert "price_shift" in report
    assert len(report["likely_associated_events"]) == 3
