"""
Bayesian change point model for Brent oil log returns.

The model assumes the log returns switch from one mean/volatility regime
to another at some unknown day, tau. We put a discrete uniform prior on
tau over the whole date range and let the data tell us where it most
likely falls.
"""
import numpy as np
import pandas as pd
import pymc as pm
import arviz as az


def build_change_point_model(log_returns: np.ndarray) -> pm.Model:
    """
    Build (but do not sample) a single change point model for a 1D array
    of log returns.

    Parameters:
        tau   - discrete uniform prior over all time indices, the switch point
        mu_1  - mean log return before tau
        mu_2  - mean log return after tau
        sigma - shared standard deviation (kept simple for interpretability)

    The likelihood uses pm.math.switch to pick mu_1 or mu_2 depending on
    whether each time index is before or after tau.
    """
    n_obs = len(log_returns)
    time_idx = np.arange(n_obs)

    with pm.Model() as model:
        tau = pm.DiscreteUniform("tau", lower=0, upper=n_obs - 1)

        mu_1 = pm.Normal("mu_1", mu=0, sigma=0.1)
        mu_2 = pm.Normal("mu_2", mu=0, sigma=0.1)
        sigma = pm.HalfNormal("sigma", sigma=0.1)

        mu = pm.math.switch(tau >= time_idx, mu_1, mu_2)

        pm.Normal("observed_returns", mu=mu, sigma=sigma, observed=log_returns)

    return model


def sample_model(model: pm.Model, draws: int = 2000, tune: int = 1000,
                  chains: int = 2, target_accept: float = 0.9, seed: int = 42,
                  cores: int = 1):
    """
    Run MCMC sampling on the given model and return the InferenceData trace.
    Sensible defaults are used so this runs in a reasonable time on a laptop.
    cores defaults to 1 for portability across environments with limited
    or unusual CPU detection (e.g. some containers/sandboxes).
    """
    with model:
        trace = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            target_accept=target_accept,
            random_seed=seed,
            cores=cores,
            progressbar=True,
        )
    return trace


def summarize_trace(trace) -> pd.DataFrame:
    """Return the standard ArviZ summary table (mean, sd, r_hat, ess, etc.)."""
    return az.summary(trace, var_names=["tau", "mu_1", "mu_2", "sigma"])


def most_likely_change_point(trace, dates: pd.Series) -> dict:
    """
    Take the posterior samples of tau (an integer index into the series)
    and map the most probable value back to an actual calendar date.
    """
    tau_samples = trace.posterior["tau"].values.flatten()
    most_common_idx = pd.Series(tau_samples).mode()[0]

    hdi = az.hdi(trace, var_names=["tau"])
    tau_low, tau_high = hdi["tau"].values

    return {
        "tau_index": int(most_common_idx),
        "tau_date": dates.iloc[int(most_common_idx)],
        "hdi_low_date": dates.iloc[int(tau_low)],
        "hdi_high_date": dates.iloc[int(tau_high)],
    }


def quantify_impact(trace) -> dict:
    """
    Summarize the posterior for mu_1 and mu_2 and translate the shift
    into a percentage change, which is the number stakeholders actually
    care about.
    """
    mu_1_samples = trace.posterior["mu_1"].values.flatten()
    mu_2_samples = trace.posterior["mu_2"].values.flatten()

    mu_1_mean = mu_1_samples.mean()
    mu_2_mean = mu_2_samples.mean()

    # avoid division by zero for a near-flat pre-change mean
    pct_change = np.nan
    if abs(mu_1_mean) > 1e-8:
        pct_change = ((mu_2_mean - mu_1_mean) / abs(mu_1_mean)) * 100

    prob_increase = float((mu_2_samples > mu_1_samples).mean())

    return {
        "mu_1_mean": mu_1_mean,
        "mu_2_mean": mu_2_mean,
        "pct_change": pct_change,
        "prob_mean_increased": prob_increase,
    }
