"""Experiments 1 and 2 -- import and visualize a time series, then decompose it
into trend, seasonal and residual components.

Everything in this course RUNS. statsmodels is installed, so decomposition,
ACF/PACF, ADF, ARIMA, SARIMA, VAR, the Kalman filter and spectral analysis are
all real calls against real implementations -- not simulations of them.

The series is BUILT rather than downloaded, from named parts, so the notes can
quote the TRUE trend slope and seasonal amplitude and check the decomposition
against them. A decomposition demonstrated on data whose truth you do not know
proves nothing.
"""
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL, seasonal_decompose

import fixtures as f


def main():
    print("  Experiments 1 and 2 -- import, visualize, decompose")

    s = f.monthly_sales()
    print(f"\n    series: {len(s)} monthly observations, "
          f"{s.index[0]:%Y-%m} to {s.index[-1]:%Y-%m}")
    print(f"    {'':<14}{'value':>10}")
    for label, v in (("first", s.iloc[0]), ("last", s.iloc[-1]),
                     ("mean", s.mean()), ("std", s.std()),
                     ("min", s.min()), ("max", s.max())):
        print(f"    {label:<14}{v:>10.2f}")
    assert len(s) == 120

    print("""
    the four questions to ask of ANY series, before any model:
      1. is there a TREND?          -- the mean is not constant
      2. is there SEASONALITY?      -- a fixed-period repeating pattern
      3. is the VARIANCE constant?  -- or does it grow with the level?
      4. are there OUTLIERS or level shifts?
         Answer these by LOOKING at the plot first. Every failure to
         identify a model correctly starts with skipping this step""")

    # ---- experiment 2: classical decomposition --------------------------
    print("\n    --- experiment 2: decomposition")
    dec = seasonal_decompose(s, model="additive", period=12)

    fitted_slope = np.polyfit(np.arange(len(s)), s.values, 1)[0]
    seasonal_amp = (dec.seasonal.max() - dec.seasonal.min()) / 2
    print(f"\n      {'component':<14}{'recovered':>12}{'true':>10}")
    print(f"      {'trend slope':<14}{fitted_slope:>12.4f}"
          f"{f.TRUE_TREND_SLOPE:>10.4f}")
    print(f"      {'seasonal amp':<14}{seasonal_amp:>12.4f}"
          f"{f.TRUE_SEASONAL_AMPLITUDE:>10.4f}")
    print(f"      {'residual std':<14}{dec.resid.std():>12.4f}{'':>10}")
    assert abs(fitted_slope - f.TRUE_TREND_SLOPE) < 0.15
    assert abs(seasonal_amp - f.TRUE_SEASONAL_AMPLITUDE) < 4
    print("""         the decomposition RECOVERED the parts the series was
         built from -- a slope near 0.8 and a seasonal amplitude near
         25. That is the check worth doing: on real data you cannot
         verify a decomposition, so verify the METHOD on data whose
         answer you already know""")

    # ---- the seasonal pattern -------------------------------------------
    monthly = dec.seasonal.groupby(dec.seasonal.index.month).mean()
    print(f"\n      the recovered seasonal component, by month:")
    print("      " + "".join(f"{m:>7}" for m in range(1, 13)))
    print("      " + "".join(f"{monthly[m]:>7.1f}" for m in range(1, 13)))
    assert abs(monthly.sum()) < 1e-6, "an additive seasonal must sum to zero"
    print(f"""         the twelve values sum to {monthly.sum():.1e} -- ZERO, by
         construction. An additive seasonal component is defined to
         average out over a full cycle, which is why it can be
         subtracted without changing the series' level""")

    # ---- additive against multiplicative ---------------------------------
    print("\n    additive or multiplicative? -- decide from the PLOT:")
    print(f"      {'':<16}{'model':<26}{'when'}")
    for label, model, when in (
            ("constant swing", "y = T + S + R", "seasonal amplitude does not grow"),
            ("growing swing", "y = T x S x R", "amplitude grows with the level")):
        print(f"      {label:<16}{model:<26}{when}")

    # demonstrate rather than assert
    t = np.arange(120)
    mult = (100 + 0.8 * t) * (1 + 0.25 * np.sin(2 * np.pi * t / 12))
    mult = pd.Series(mult, index=s.index)
    early = mult.iloc[:24].max() - mult.iloc[:24].min()
    late = mult.iloc[-24:].max() - mult.iloc[-24:].min()
    print(f"\n      on a MULTIPLICATIVE series, the peak-to-trough swing is")
    print(f"        first two years: {early:.1f}")
    print(f"        last two years : {late:.1f}   ({late / early:.2f}x)")
    assert late > 1.5 * early
    print("""         a growing swing is the whole diagnostic. Fit an additive
         model to it and the residuals are small early and large late --
         which is heteroscedasticity, and it invalidates every
         confidence interval the model produces.
         The fix is a LOG TRANSFORM: log(T x S x R) = log T + log S +
         log R turns a multiplicative series into an additive one""")

    logged = np.log(mult)
    early_l = logged.iloc[:24].max() - logged.iloc[:24].min()
    late_l = logged.iloc[-24:].max() - logged.iloc[-24:].min()
    print(f"\n      after log: {early_l:.4f} against {late_l:.4f} "
          f"({late_l / early_l:.2f}x)")
    assert abs(late_l / early_l - 1) < 0.15
    print("""         the swing is now nearly CONSTANT. That is the
         transformation to reach for whenever a series fans out, and it
         is why so many economic series are modelled in logs""")

    # ---- STL, the modern alternative --------------------------------------
    print("\n    STL, which classical decomposition cannot do:")
    stl = STL(s, period=12, robust=True).fit()
    early_seas = stl.seasonal.iloc[:12].std()
    late_seas = stl.seasonal.iloc[-12:].std()
    print(f"      classical: ONE seasonal pattern, repeated identically")
    print(f"      STL      : the pattern may EVOLVE  "
          f"(std {early_seas:.2f} early, {late_seas:.2f} late)")
    n_missing = int(dec.trend.isna().sum())
    print(f"\n      classical trend is missing at {n_missing} of {len(s)} points "
          f"(6 at each end)")
    print(f"      STL trend is missing at {int(stl.trend.isna().sum())}")
    assert n_missing == 12 and stl.trend.isna().sum() == 0
    print("""         classical decomposition forces every January to be
         identical, and it LOSES SIX POINTS AT EACH END because a
         centred 12-month moving average cannot be computed there.
         STL lets the shape drift, handles outliers with a robust fit,
         and covers the whole series -- which is why it is the default
         in modern practice and worth naming in an exam""")

    return s


if __name__ == "__main__":
    main()
