"""Shared time series for Course 14 B.

Three series, all DETERMINISTIC -- built from a fixed seed, so every figure in
the notes reproduces exactly. That matters more here than in any other course:
a time series result quoted from a random draw is unreproducible, and the
whole point of ACF, ADF and AIC is that they are comparable numbers.

  * MONTHLY_SALES -- trend + annual seasonality + noise, 120 months. The
    workhorse: decomposition, ACF/PACF, ADF, ARIMA and SARIMA all use it.
  * AR2 / MA1 / ARMA11 -- series generated from KNOWN coefficients, so a
    fitted model can be checked against the truth that produced it. This is
    the only honest way to demonstrate that model identification works.
  * MACRO -- three interlinked economic series for the VAR experiment, built
    with a known lag structure.
"""
import numpy as np
import pandas as pd

SEED = 42
N_MONTHS = 120
START = "2016-01-01"


def _index(n=N_MONTHS, start=START):
    return pd.period_range(start=start, periods=n, freq="M").to_timestamp()


def monthly_sales(n=N_MONTHS, seed=SEED):
    """Trend + annual seasonality + AR(1) noise. The series the course uses.

    Built from named parts so the notes can quote the TRUE trend slope and
    the TRUE seasonal amplitude and check the decomposition against them.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    trend = 100 + 0.8 * t                       # +0.8 units per month
    season = 25 * np.sin(2 * np.pi * t / 12)    # annual, amplitude 25
    noise = np.zeros(n)
    for i in range(1, n):                        # AR(1) noise, phi = 0.5
        noise[i] = 0.5 * noise[i - 1] + rng.normal(0, 5)
    return pd.Series(trend + season + noise, index=_index(n), name="sales")


TRUE_TREND_SLOPE = 0.8
TRUE_SEASONAL_AMPLITUDE = 25.0
TRUE_NOISE_PHI = 0.5


def ar_series(phis, n=400, seed=SEED, sigma=1.0):
    """Generate an AR(p) series from KNOWN coefficients.

    A plain integer index, not dates: these series have no calendar meaning,
    and a long one overflows pandas' nanosecond timestamp range in 2262.
    """
    rng = np.random.default_rng(seed)
    p = len(phis)
    x = np.zeros(n + 100)
    e = rng.normal(0, sigma, n + 100)
    for i in range(p, n + 100):
        x[i] = sum(phis[j] * x[i - j - 1] for j in range(p)) + e[i]
    return pd.Series(x[100:], name="ar")      # burn-in dropped; plain index


def ma_series(thetas, n=400, seed=SEED, sigma=1.0):
    """Generate an MA(q) series from KNOWN coefficients."""
    rng = np.random.default_rng(seed)
    q = len(thetas)
    e = rng.normal(0, sigma, n + q)
    x = np.array([e[i + q] + sum(thetas[j] * e[i + q - j - 1] for j in range(q))
                  for i in range(n)])
    return pd.Series(x, name="ma")


def arma_series(phis, thetas, n=400, seed=SEED, sigma=1.0):
    rng = np.random.default_rng(seed)
    p, q = len(phis), len(thetas)
    burn = 100
    e = rng.normal(0, sigma, n + burn)
    x = np.zeros(n + burn)
    for i in range(max(p, q), n + burn):
        ar = sum(phis[j] * x[i - j - 1] for j in range(p))
        ma = sum(thetas[j] * e[i - j - 1] for j in range(q))
        x[i] = ar + ma + e[i]
    return pd.Series(x[burn:], name="arma")


TRUE_AR2 = (0.6, -0.3)
TRUE_MA1 = (0.7,)
TRUE_ARMA11 = ((0.6,), (0.4,))


def random_walk(n=400, seed=SEED, drift=0.0, sigma=1.0):
    """A UNIT ROOT process -- the thing the ADF test must reject stationarity for."""
    rng = np.random.default_rng(seed)
    return pd.Series(np.cumsum(rng.normal(drift, sigma, n)),
                     name="random_walk")


def macro(n=200, seed=SEED):
    """Three series with a KNOWN lag structure, for the VAR experiment.

    gdp leads inflation by one period; unemployment responds to gdp
    negatively. Because the structure is known, the fitted VAR's Granger
    causality results can be checked rather than merely reported.
    """
    rng = np.random.default_rng(seed)
    gdp = np.zeros(n)
    infl = np.zeros(n)
    unemp = np.zeros(n)
    eg, ei, eu = (rng.normal(0, 1, n) for _ in range(3))
    for t in range(2, n):
        gdp[t] = 0.6 * gdp[t - 1] + eg[t]
        infl[t] = 0.3 * infl[t - 1] + 0.5 * gdp[t - 1] + ei[t]
        unemp[t] = 0.5 * unemp[t - 1] - 0.4 * gdp[t - 1] + eu[t]
    return pd.DataFrame({"gdp": gdp, "inflation": infl, "unemployment": unemp},
                        index=_index(n))


def train_test(series, horizon=12):
    """The ONLY correct split for a time series: the last h observations."""
    return series.iloc[:-horizon], series.iloc[-horizon:]
