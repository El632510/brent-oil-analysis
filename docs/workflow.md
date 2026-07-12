# Analysis Workflow: Brent Oil Price Change Point Analysis

## 1. Business Objective

Birhan Energies needs to understand how major geopolitical and economic events
relate to structural shifts in Brent crude oil prices, so that investors,
policymakers, and energy companies can better interpret price movements and
plan around future shocks.

## 2. Planned Steps

1. **Data loading & cleaning**
   - Load the daily Brent price series (1987-2022).
   - Parse dates (two different formats appear in the raw file - older rows
     use `DD-Mon-YY`, newer rows use `Mon DD, YYYY`).
   - Sort chronologically and check for missing values or duplicate dates.

2. **Event research & compilation**
   - Research major oil-market events: wars, OPEC/OPEC+ decisions,
     sanctions, and economic shocks.
   - Store them as a structured CSV (`event_name`, `start_date`, `category`,
     `description`) so they can later be programmatically compared against
     detected change points.

3. **Exploratory Data Analysis (EDA)**
   - Plot the raw price series to visually identify long-run trends and
     shocks.
   - Test stationarity with the Augmented Dickey-Fuller (ADF) test.
   - Compute log returns (`log(P_t) - log(P_t-1)`) and re-test stationarity,
     since raw prices are expected to be non-stationary.
   - Examine rolling volatility to check for volatility clustering.

4. **Change point modeling (Task 2)**
   - Build a Bayesian change point model in PyMC on log returns.
   - Define a discrete uniform prior over the switch point `tau`, two regime
     means (`mu_1`, `mu_2`), and use `pm.math.switch` to select the active
     regime in the likelihood.
   - Run MCMC sampling and check convergence (r_hat, trace plots).

5. **Interpretation**
   - Identify the most probable change point date(s) from the posterior of
     `tau`.
   - Compare detected dates against the researched event list to form
     hypotheses about likely triggers.
   - Quantify the shift (e.g. "average return moved from X to Y").

6. **Communication (Task 3)**
   - Build a small Flask + React dashboard so stakeholders can explore price
     history, detected change points, and event overlays themselves.
   - Write a final report summarizing methodology, findings, and limits.

## 3. Assumptions and Limitations

**Assumptions**
- Event dates are treated as approximately correct starting points - the
  actual market impact of an event is rarely confined to a single day.
- A single change point is a simplifying starting model; the real series
  almost certainly contains multiple structural breaks over 35 years.
- Regimes are assumed to be internally stable (constant mean/variance within
  a regime), which is a simplification of real market behavior.

**Limitations**
- The event list is curated by us and is not exhaustive - smaller events or
  regional shocks may be missing.
- Daily closing prices ignore intraday volatility.

**Correlation vs. Causation**

This is the most important limitation to be explicit about. A change point
model tells us **when** the statistical properties of the price series
changed - it does not tell us **why**. If a detected change point falls near
a known event, that is a temporal association, not proof that the event
caused the shift. Markets often price in anticipated events before they
happen (e.g. OPEC meeting speculation), and multiple events can cluster
close together in time, making it hard to isolate a single cause. Throughout
this analysis, findings will be phrased as an event being **"associated
with"** a detected change, never as an event **"causing"** a change, unless
much stronger causal evidence (e.g. a controlled natural experiment) is
available - which is not the case here.
