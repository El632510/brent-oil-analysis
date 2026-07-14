# Backend (Flask API)

Serves the precomputed Task 2 analysis results to the React dashboard.

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make sure `data/processed/` has been generated first (see the root
README's "Running the analysis" section) - the API reads from those
files, it does not run PyMC sampling on request.

## Running

```bash
PYTHONPATH=. python run.py
```

Runs on http://127.0.0.1:5000 by default.

## API Endpoints

### `GET /api/health`
Simple liveness check.
```json
{"status": "ok"}
```

### `GET /api/prices`
Historical daily Brent prices.

Query params (optional): `start_date`, `end_date` (format `YYYY-MM-DD`)

```
GET /api/prices?start_date=2020-01-01&end_date=2020-06-30
```
```json
{
  "count": 182,
  "prices": [
    {"Date": "2020-01-02", "Price": 66.25, "log_price": 4.19, "log_return": 0.01},
    ...
  ]
}
```

### `GET /api/change-points`
The Bayesian change point model results.
```json
{
  "change_point_date": "2020-04-21",
  "hdi_low_date": "2019-08-12",
  "hdi_high_date": "2020-12-31",
  "mu_before": -0.0043,
  "mu_after": 0.0043,
  "pct_change_in_mean_return": 199.29,
  "prob_mean_increased": 0.765,
  "avg_price_before": 57.2,
  "avg_price_after": 40.42,
  "price_pct_change": -29.34,
  "associated_events": [ { "event_name": "...", "days_from_change_point": -1 }, ... ],
  "analysis_window_start": "2019-06-03",
  "analysis_window_end": "2020-12-31"
}
```

### `GET /api/events`
The researched events dataset.
```json
{
  "count": 16,
  "events": [
    {"event_date": "1990-08-02", "event_name": "Iraq invades Kuwait", "category": "geopolitical_conflict", "description": "..."},
    ...
  ]
}
```

### `GET /api/summary`
Headline statistics for dashboard summary cards.
```json
{
  "total_days": 9011,
  "date_range_start": "1987-05-20",
  "date_range_end": "2022-11-14",
  "min_price": 9.1,
  "max_price": 143.95,
  "avg_price": 48.42,
  "avg_daily_volatility": 0.02553
}
```

## Structure

```
backend/
├── app/
│   ├── __init__.py       # app factory, blueprint registration
│   ├── services.py       # data access layer (reads data/processed/)
│   └── routes/
│       ├── prices.py
│       ├── change_points.py
│       ├── events.py
│       └── summary.py
└── run.py                # entry point
```
