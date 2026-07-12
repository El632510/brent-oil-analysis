# Brent Oil Price Change Point Analysis

Analyzing how major geopolitical and economic events relate to structural
changes in Brent crude oil prices (1987-2022), for Birhan Energies.

This is the Week 10 challenge project (10 Academy - AI Mastery program).

## Project Status

- [x] Task 1: Data understanding, event research, initial EDA
- [ ] Task 2: Bayesian change point modeling (PyMC)
- [ ] Task 3: Interactive dashboard (Flask + React)

## Project Structure

```
brent-oil-analysis/
├── .github/workflows/     # CI: runs tests on push
├── data/
│   ├── raw/                # original BrentOilPrices.csv
│   ├── processed/          # generated plots / model outputs
│   └── events.csv          # researched list of major oil market events
├── docs/
│   └── workflow.md         # analysis workflow + assumptions/limitations
├── notebooks/
│   └── 01_eda.ipynb        # Task 1 exploratory analysis
├── src/
│   └── data_loader.py      # data loading and log return calculation
├── tests/
│   └── test_data_loader.py
└── scripts/                 # reserved for Task 2/3 helper scripts
```

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the tests

```bash
pytest tests/ -v
```

## Running the EDA notebook

```bash
jupyter notebook notebooks/01_eda.ipynb
```

## Data

Source: daily Brent crude oil prices, May 1987 - Nov 2022 (`data/raw/BrentOilPrices.csv`).
Note: the raw file mixes two date formats (`DD-Mon-YY` for older rows,
`Mon DD, YYYY` for newer rows) - `src/data_loader.py` handles both.

## Key Findings So Far (Task 1)

- Raw prices are non-stationary (ADF test, p ≈ 0.29)
- Log returns are stationary (ADF test, p ≈ 0) - this is what we model going forward
- Volatility clusters over time (calm vs. turbulent regimes), most visibly around
  2008-09, 2014-16, and 2020

See `docs/workflow.md` for the full write-up, assumptions, and limitations,
and `data/events.csv` for the researched event list.
