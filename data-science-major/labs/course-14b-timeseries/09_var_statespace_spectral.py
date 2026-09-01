"""Experiments 9, 10 and 11 -- multivariate VAR on macroeconomic data,
state-space models with the Kalman filter, and spectral analysis.

All three are real statsmodels calls. The macro data is generated with a KNOWN
lag structure -- gdp leads inflation, and depresses unemployment -- so the
VAR's Granger causality results can be CHECKED against the truth rather than
merely reported, which is the only way to show that the test works.
"""
import warnings

import numpy as np
from statsmodels.tsa.api import VAR
from statsmodels.tsa.statespace.structural import UnobservedComponents

import fixtures as f

warnings.filterwarnings("ignore")


def main():
    print("  Experiments 9, 10 and 11 -- VAR, state-space and spectral")

    # ================================================= experiment 9
    print("\n    --- experiment 9: vector autoregression")

    data = f.macro(n=200)
    print(f"\n      three series, {len(data)} periods, built with a KNOWN "
          f"lag structure:")
    print("        gdp[t]          = 0.6*gdp[t-1] + e")
    print("        inflation[t]    = 0.3*inflation[t-1] + 0.5*GDP[t-1] + e")
    print("        unemployment[t] = 0.5*unemp[t-1] - 0.4*GDP[t-1] + e")
    print("""         so GDP causes the other two and NEITHER causes GDP.
         That asymmetry is what Granger causality should find, and
         checking it against a known answer is the point""")

    print(f"\n      order selection:")
    model = VAR(data)
    sel = model.select_order(maxlags=6)
    print(f"      {'criterion':<10}{'chosen lag':>12}")
    for crit in ("aic", "bic", "hqic", "fpe"):
        print(f"      {crit.upper():<10}{getattr(sel, crit):>12}")
    chosen = sel.aic
    assert chosen >= 1

    res = model.fit(maxlags=1)
    print(f"\n      VAR(1) fitted -- the coefficient matrix "
          f"(row = equation, column = lagged variable):")
    coefs = res.coefs[0]
    names = list(data.columns)
    print("      " + " " * 15 + "".join(f"{n[:12]:>14}" for n in names))
    for i, n in enumerate(names):
        print(f"      {n:<15}" + "".join(f"{coefs[i, j]:>14.4f}"
                                         for j in range(len(names))))
    print(f"""
      compare against the truth:
        gdp   -> inflation    true  0.500   estimated {coefs[1, 0]:>7.4f}
        gdp   -> unemployment true -0.400   estimated {coefs[2, 0]:>7.4f}
        infl  -> gdp          true  0.000   estimated {coefs[0, 1]:>7.4f}""")
    assert abs(coefs[1, 0] - 0.5) < 0.15
    assert abs(coefs[2, 0] + 0.4) < 0.15
    assert abs(coefs[0, 1]) < 0.15
    print("""         the VAR RECOVERED the structure, including the two zeros
         it was not told about. A VAR is 'atheoretical' -- it puts
         every lag of every variable in every equation and lets the
         data decide, which is its strength and the reason it needs a
         lot of data""")

    # ---- Granger causality -----------------------------------------------
    print("\n      Granger causality (H0: X does NOT help predict Y):")
    print(f"      {'X':<16}{'->':^4}{'Y':<16}{'p-value':>10}  conclusion")
    checks = [("gdp", "inflation", True), ("gdp", "unemployment", True),
              ("inflation", "gdp", False), ("unemployment", "gdp", False)]
    for x, y, should in checks:
        p = res.test_causality(y, [x], kind="f").pvalue
        found = p < 0.05
        mark = "as built" if found == should else "MISMATCH"
        print(f"      {x:<16}{'->':^4}{y:<16}{p:>10.4f}  "
              f"{'causes' if found else 'no evidence':<12} {mark}")
        assert found == should, f"{x}->{y} disagrees with the generating truth"
    print("""         ALL FOUR MATCH THE GENERATING PROCESS, including both
         NON-causal directions. That is the harder half: a test that
         only ever finds effects is not a test""")

    print("""
      and the warning that belongs with every Granger result:
        'Granger causes' means 'helps predict', NOTHING MORE. It
        cannot distinguish a real cause from a common third driver
        that moves one series before the other, and it says nothing
        about intervention. Ice cream sales Granger-cause drownings.
         Say 'X Granger-causes Y' out loud, never 'X causes Y'""")

    # ---- forecasting with a VAR ------------------------------------------
    train_v = data.iloc[:-12]
    test_v = data.iloc[-12:]
    fitted = VAR(train_v).fit(maxlags=1)
    fc = fitted.forecast(train_v.values[-1:], steps=12)
    print(f"\n      VAR forecast RMSE, 12 periods ahead:")
    print(f"      {'series':<16}{'VAR':>9}{'univariate AR(1)':>19}")
    from statsmodels.tsa.arima.model import ARIMA
    verdicts = {}
    for j, n in enumerate(names):
        var_rmse = float(np.sqrt(np.mean((test_v[n].values - fc[:, j]) ** 2)))
        uni = ARIMA(train_v[n], order=(1, 0, 0)).fit()
        uni_rmse = float(np.sqrt(np.mean(
            (test_v[n].values - uni.forecast(12).values) ** 2)))
        verdicts[n] = (var_rmse, uni_rmse)
        print(f"      {n:<16}{var_rmse:>9.4f}{uni_rmse:>19.4f}"
              f"   {'VAR wins' if var_rmse < uni_rmse else 'UNIVARIATE wins'}")
    assert verdicts["gdp"][0] > verdicts["gdp"][1], "gdp has no incoming links"
    assert verdicts["inflation"][0] < verdicts["inflation"][1]
    print(f"""         THE VAR LOST ON GDP AND WON ON THE OTHER TWO, and that
         is exactly right rather than a disappointment. GDP was built
         as a pure AR(1) with NOTHING feeding into it, so the VAR's
         extra coefficients are estimating zeros -- pure variance, no
         signal. Inflation and unemployment DO depend on lagged GDP,
         and there the VAR has real information the univariate model
         cannot see.
         The rule: a VAR helps only where cross-series information
         exists. Fitting one to unrelated series buys you k^2 p
         parameters and nothing else, which is why VARs are usually
         limited to three or four variables""")

    # ================================================= experiment 10
    print("\n    --- experiment 10: state-space models and the Kalman filter")

    print("""
    every model in this course is a state-space model underneath.
    statsmodels' SARIMAX runs the KALMAN FILTER to evaluate its
    likelihood -- so you have been using one since experiment 5.

      the two equations, and that is the whole framework:
        state:       x[t] = T x[t-1] + noise      (how the world moves)
        observation: y[t] = Z x[t]   + noise      (what you get to see)
         the state is UNOBSERVED. The filter's job is to infer it from
         noisy observations, optimally, one step at a time""")

    sales = f.monthly_sales()
    uc = UnobservedComponents(sales, level="local linear trend",
                              seasonal=12).fit(disp=False)
    print(f"\n      a local-linear-trend + seasonal model on the sales series:")
    print(f"      {'component':<24}{'variance':>12}")
    for name in uc.params.index:
        print(f"      {name:<24}{uc.params[name]:>12.4f}")

    level = np.asarray(uc.level["smoothed"])
    seas = np.asarray(uc.seasonal["smoothed"])
    print(f"\n      the filter DECOMPOSED the series while fitting it:")
    print(f"      {'':<24}{'first':>10}{'last':>10}{'change':>10}")
    print(f"      {'estimated level':<24}{level[0]:>10.2f}"
          f"{level[-1]:>10.2f}{level[-1] - level[0]:>10.2f}")
    implied_slope = (level[-1] - level[0]) / (len(sales) - 1)
    print(f"      implied trend slope: {implied_slope:.4f}   "
          f"(true {f.TRUE_TREND_SLOPE})")
    assert abs(implied_slope - f.TRUE_TREND_SLOPE) < 0.2
    zero_var = [n for n in uc.params.index if uc.params[n] < 1e-6]
    if zero_var:
        print(f"""
         AND NOTE THE ZEROS: {', '.join(x.replace('sigma2.', '') for x in zero_var)} came
         back at 0.0000. The filter is saying those components DO NOT
         VARY -- the slope is a fixed number and the seasonal pattern
         repeats exactly.
         That is correct: the series was built with a constant 0.8
         slope and a fixed sine. A variance estimated at exactly zero
         is the state-space way of reporting 'this component is
         deterministic', and it is a result rather than a convergence
         failure""")
    print("""         it recovered the 0.8 slope the series was built with --
         the same answer experiment 2's decomposition gave, reached a
         completely different way. Decomposition SPLITS the series
         after the fact; the state-space model TREATS the components
         as unobserved states and estimates them jointly with the
         parameters""")

    # ---- what the Kalman filter can do that ARIMA cannot ------------------
    print("\n      what a state-space model does that ARIMA cannot:")
    print(f"      {'capability':<34}{'ARIMA':<10}{'state-space'}")
    for cap, ar, ss in (("missing observations", "refit", "HANDLED NATIVELY"),
                        ("time-varying parameters", "no", "yes"),
                        ("components you can inspect", "no", "yes"),
                        ("real-time updating", "refit", "one recursion"),
                        ("multiple related series", "no", "yes")):
        print(f"      {cap:<34}{ar:<10}{ss}")

    gappy = sales.copy()
    gappy.iloc[40:46] = np.nan
    uc_gap = UnobservedComponents(gappy, level="local linear trend",
                                  seasonal=12).fit(disp=False)
    smoothed_fit = np.asarray(uc_gap.fittedvalues)[40:46]
    truth = sales.iloc[40:46].values
    print(f"\n      six observations deleted, then estimated by the filter:")
    print(f"      {'t':>4}{'true':>10}{'estimate':>12}{'error':>10}")
    for i in range(6):
        print(f"      {40 + i:>4}{truth[i]:>10.2f}{smoothed_fit[i]:>12.2f}"
              f"{smoothed_fit[i] - truth[i]:>+10.2f}")
    gap_rmse = float(np.sqrt(np.mean((smoothed_fit - truth) ** 2)))
    print(f"      RMSE over the gap: {gap_rmse:.3f}   "
          f"(series std {sales.std():.2f})")
    assert gap_rmse < sales.std()
    print("""         NO IMPUTATION STEP WAS RUN. The Kalman filter simply
         skips the update at a missing time and keeps predicting the
         state forward, so a gap costs precision and nothing else.
         Every other method in this course would need the hole filled
         first -- and filling it with the mean, which is the usual
         reflex, injects a fake observation the model then trusts""")

    # ================================================= experiment 11
    print("\n    --- experiment 11: spectral analysis")

    print("""
    the time domain asks 'what happened when?'
    the FREQUENCY domain asks 'WHICH CYCLES is this made of?'
         same information, different question -- and for a series
         with several overlapping cycles the second is far easier to
         answer by eye""")

    from scipy import signal as sg
    t = np.arange(512)
    rng = np.random.default_rng(f.SEED)
    composite = (3 * np.sin(2 * np.pi * t / 12)      # period 12
                 + 1.5 * np.sin(2 * np.pi * t / 4)   # period 4
                 + rng.normal(0, 1, 512))
    freqs, power = sg.periodogram(composite, scaling="spectrum")
    order = np.argsort(power)[::-1][:4]
    print(f"\n      a series built from cycles of period 12 and 4, plus noise")
    print(f"      the four strongest frequencies found:")
    print(f"      {'rank':>5}{'frequency':>12}{'period':>10}{'power':>10}")
    periods = []
    for r, idx in enumerate(order, 1):
        per = 1 / freqs[idx] if freqs[idx] > 0 else np.inf
        periods.append(round(per))
        print(f"      {r:>5}{freqs[idx]:>12.5f}{per:>10.2f}{power[idx]:>10.3f}")
    assert 12 in periods and 4 in periods, "both true cycles must be found"
    print("""         PERIOD 12 AND PERIOD 4 BOTH RECOVERED, and they are the
         two the series was built from. The periodogram found them
         without being told they were there, which is what makes
         spectral analysis useful on data whose cycles you do not
         already know""")

    print("\n      the same method on the monthly sales series:")
    detrended = sg.detrend(sales.values)
    fs, ps = sg.periodogram(detrended, scaling="spectrum")
    top = np.argsort(ps)[::-1][:3]
    print(f"      {'rank':>5}{'period (months)':>18}{'power':>10}")
    found = []
    for r, idx in enumerate(top, 1):
        per = 1 / fs[idx] if fs[idx] > 0 else np.inf
        found.append(per)
        print(f"      {r:>5}{per:>18.2f}{ps[idx]:>10.2f}")
    assert abs(found[0] - 12) < 1.5, "the annual cycle must dominate"
    print(f"""         the dominant period is {found[0]:.1f} months -- the annual
         cycle, recovered from the data rather than assumed.
         THAT is the practical use of a periodogram: it tells you what
         m should be in SARIMA(p,d,q)(P,D,Q,m) when you do not already
         know. Guessing m is the commonest seasonal-model error, and
         this is how you stop guessing""")

    print("""
      two warnings that belong with any periodogram:
        1. it assumes the cycle is STATIONARY and fixed in period.
           A cycle that drifts smears across several frequencies.
        2. detrend FIRST. A trend is a very low frequency and it will
           dominate the spectrum and hide everything else""")
    fs_raw, ps_raw = sg.periodogram(sales.values, scaling="spectrum")
    raw_top = 1 / fs_raw[np.argsort(ps_raw)[::-1][0]]
    print(f"\n      undetrended, the strongest period is {raw_top:.1f} months "
          f"-- i.e. the whole series length, which is the trend")


if __name__ == "__main__":
    main()
