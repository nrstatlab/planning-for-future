"""Experiments 3 and 4 -- compute and plot ACF and PACF, and test stationarity
with the Augmented Dickey-Fuller test.

These two experiments decide everything that follows. p and q come from the
PACF and ACF; d comes from the ADF test. Get them wrong and every model in
experiments 5-8 is fitted to the wrong specification.

The series here are generated from KNOWN coefficients, so the identification
rules can be CHECKED rather than recited.
"""
import numpy as np
from statsmodels.tsa.stattools import acf, adfuller, kpss, pacf

import fixtures as f


def bar(value, width=28, lo=-1.0, hi=1.0):
    """A text ACF plot. The point of an ACF is its SHAPE, and a table of
    numbers hides the shape that the identification rules depend on."""
    mid = width // 2
    pos = int(round((value - lo) / (hi - lo) * (width - 1)))
    pos = max(0, min(width - 1, pos))
    row = [" "] * width
    row[mid] = "|"
    row[pos] = "#" if pos != mid else "#"
    return "".join(row)


def show_correlogram(series, nlags=14, title=""):
    a = acf(series, nlags=nlags, fft=False)
    p = pacf(series, nlags=nlags)
    ci = 1.96 / np.sqrt(len(series))
    print(f"\n      {title}   (95% band = +/-{ci:.3f})")
    print(f"      {'lag':>4}{'ACF':>9} {'':<28}{'PACF':>9} {'':<28}")
    for k in range(1, nlags + 1):
        sa = "*" if abs(a[k]) > ci else " "
        sp = "*" if abs(p[k]) > ci else " "
        print(f"      {k:>4}{a[k]:>9.3f}{sa}{bar(a[k])}"
              f"{p[k]:>9.3f}{sp}{bar(p[k])}")
    return a, p, ci


def significant_lags(vals, ci, upto=14):
    return [k for k in range(1, upto + 1) if abs(vals[k]) > ci]


def main():
    print("  Experiments 3 and 4 -- ACF, PACF and stationarity")

    # ================================================= experiment 3
    print("\n    --- experiment 3: the correlograms, and what they identify")

    print("""
    the two rules, and they are the whole of model identification:
      ACF  CUTS OFF after lag q, PACF tails off   ->  MA(q)
      PACF CUTS OFF after lag p, ACF  tails off   ->  AR(p)
      BOTH tail off                               ->  ARMA(p,q)
         'cuts off' means drops inside the confidence band and STAYS
         there. 'tails off' means decays gradually. Below, each rule is
         checked against a series built from KNOWN coefficients""")

    # ---- AR(2) -----------------------------------------------------------
    ar2 = f.ar_series(f.TRUE_AR2, n=400)
    a, p, ci = show_correlogram(ar2, title=f"AR(2), true phi = {f.TRUE_AR2}")
    sig_pacf = significant_lags(p, ci)
    print(f"\n      PACF significant at lags: {sig_pacf}")
    assert 1 in sig_pacf and 2 in sig_pacf
    assert 3 not in sig_pacf and 4 not in sig_pacf
    print(f"""         THE PACF CUT OFF AFTER LAG 2, and the true order is 2.
         The rule worked, on data whose answer we knew. Note that a
         few later lags may still poke outside the band by chance --
         with a 95% band, 1 lag in 20 does, and that is not evidence
         of structure""")

    # ---- MA(1) -----------------------------------------------------------
    ma1 = f.ma_series(f.TRUE_MA1, n=400)
    a, p, ci = show_correlogram(ma1, title=f"MA(1), true theta = {f.TRUE_MA1}")
    sig_acf = significant_lags(a, ci)
    print(f"\n      ACF significant at lags: {sig_acf}")
    assert sig_acf[0] == 1 and 2 not in sig_acf
    theoretical = f.TRUE_MA1[0] / (1 + f.TRUE_MA1[0] ** 2)
    print(f"      ACF at lag 1 = {a[1]:.4f}, theory says "
          f"theta/(1+theta^2) = {theoretical:.4f}")
    assert abs(a[1] - theoretical) < 0.06
    print("""         THE ACF CUT OFF AFTER LAG 1, and it landed on the value
         theory predicts. An MA(q) process has EXACTLY ZERO
         autocorrelation beyond lag q -- not small, zero -- because
         y_t and y_{t-q-1} share no shocks at all""")

    # ---- ARMA(1,1) -------------------------------------------------------
    arma = f.arma_series(*f.TRUE_ARMA11, n=400)
    a, p, ci = show_correlogram(arma, nlags=10, title="ARMA(1,1)")
    print("""         BOTH tail off -- neither cuts cleanly. That is the
         ARMA signature, and it is also why ARMA orders are chosen by
         AIC (experiment 7) rather than by eye: the correlogram tells
         you it is ARMA, and not which one""")

    # ---- white noise, the null case --------------------------------------
    rng = np.random.default_rng(f.SEED)
    wn = rng.normal(0, 1, 400)
    a_wn = acf(wn, nlags=20, fft=False)
    ci_wn = 1.96 / np.sqrt(400)
    outside = sum(1 for k in range(1, 21) if abs(a_wn[k]) > ci_wn)
    print(f"\n      WHITE NOISE, 20 lags: {outside} outside the 95% band")
    assert outside <= 3
    print(f"""         with a 95% band you EXPECT about 1 lag in 20 outside it
         by chance -- here {outside}. Reading structure into one stray
         spike is the commonest correlogram mistake, and the reason
         the Ljung-Box test (experiment 5) tests the lags JOINTLY
         rather than one at a time""")

    # ================================================= experiment 4
    print("\n    --- experiment 4: the Augmented Dickey-Fuller test")

    print("""
    read the hypotheses carefully, because they are the opposite way
    round from most tests you have met:
      ADF   H0: there IS a unit root (NON-stationary)
            -> a SMALL p-value means STATIONARY
      KPSS  H0: the series IS stationary
            -> a SMALL p-value means NON-stationary
         Two tests with opposite nulls. Running both is standard
         practice, precisely because failing to reject is not the same
         as accepting""")

    rw = f.random_walk(n=400)
    sales = f.monthly_sales()
    cases = [
        ("white noise", wn),
        ("AR(2), stationary", ar2.values),
        ("random walk", rw.values),
        ("random walk, differenced", np.diff(rw.values)),
        ("monthly sales", sales.values),
        ("sales, differenced", np.diff(sales.values)),
        ("sales, seasonally differenced", sales.values[12:] - sales.values[:-12]),
    ]
    print(f"\n      {'series':<32}{'ADF stat':>10}{'p':>8}  verdict")
    results = {}
    for label, data in cases:
        stat, pval = adfuller(data, autolag="AIC")[:2]
        verdict = "STATIONARY" if pval < 0.05 else "unit root"
        results[label] = pval
        print(f"      {label:<32}{stat:>10.3f}{pval:>8.4f}  {verdict}")

    assert results["white noise"] < 0.05
    assert results["random walk"] > 0.05
    assert results["random walk, differenced"] < 0.05
    print(f"""         THE RANDOM WALK IS THE POINT. Undifferenced it has
         p = {results['random walk']:.4f} -- a unit root, as it must, because a
         random walk IS the textbook unit-root process. Difference it
         once and p = {results['random walk, differenced']:.4f}.
         That is where the 'd' in ARIMA(p,d,q) comes from: d is how
         many differences it takes to reach stationarity""")

    # ---- the trap: differencing a trend-stationary series ----------------
    print("\n    the trap -- over-differencing:")
    t = np.arange(400)
    trend_stat = 0.5 * t + rng.normal(0, 3, 400)
    d0 = adfuller(trend_stat, autolag="AIC")[1]
    d1 = np.diff(trend_stat)
    d2 = np.diff(d1)
    print(f"      {'':<26}{'ADF p':>9}{'variance':>12}")
    for label, data in (("original (trend + noise)", trend_stat),
                        ("differenced once", d1),
                        ("differenced TWICE", d2)):
        print(f"      {label:<26}{adfuller(data, autolag='AIC')[1]:>9.4f}"
              f"{np.var(data):>12.3f}")
    assert np.var(d2) > np.var(d1)
    print(f"""         DIFFERENCING TWICE MADE THE VARIANCE LARGER
         ({np.var(d1):.2f} -> {np.var(d2):.2f}). That is the signature of
         over-differencing: each unnecessary difference injects noise
         and adds a spurious negative MA term.
         Difference until the ADF rejects, then STOP. If the variance
         goes up, you have gone one too far -- and 'd' is almost never
         more than 2 in practice""")

    # ---- KPSS, the complementary test -------------------------------------
    print("\n    ADF and KPSS together -- and the regression term matters:")
    print("      ADF with regression='c'  allows a constant only")
    print("      ADF with regression='ct' allows a constant AND A TREND")
    print(f"\n      {'series':<22}{'ADF c':>8}{'ADF ct':>8}{'KPSS c':>9}  conclusion")
    import warnings
    combos = {}
    for label, data in (("white noise", wn),
                        ("random walk", rw.values),
                        ("trend + noise", trend_stat)):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            adf_c = adfuller(data, regression="c", autolag="AIC")[1]
            adf_ct = adfuller(data, regression="ct", autolag="AIC")[1]
            kpss_c = kpss(data, regression="c", nlags="auto")[1]
        combos[label] = (adf_c, adf_ct, kpss_c)
        if adf_c > 0.05 and adf_ct < 0.05:
            concl = "TREND-stationary -- DETREND, do not difference"
        elif adf_c < 0.05 and kpss_c > 0.05:
            concl = "stationary -- both agree"
        elif adf_c > 0.05 and kpss_c < 0.05:
            concl = "non-stationary"
        else:
            concl = "inconclusive -- more data needed"
        print(f"      {label:<22}{adf_c:>8.4f}{adf_ct:>8.4f}{kpss_c:>9.4f}  {concl}")

    tn = combos["trend + noise"]
    rwv = combos["random walk"]
    assert tn[0] > 0.05 and tn[1] < 0.05, "trend+noise must flip under 'ct'"
    assert rwv[1] > 0.05, "a random walk stays non-stationary even under 'ct'"
    print(f"""         THE THIRD ROW IS WHY THE REGRESSION TERM MATTERS.
         'trend + noise' looks non-stationary to the plain ADF
         (p = {tn[0]:.4f}) and STATIONARY once the test is allowed a trend
         (p = {tn[1]:.4f}). It is TREND-stationary: the right treatment is to
         DETREND, not to difference.
         The random walk does not flip -- p = {rwv[1]:.4f} even under 'ct' --
         because it has a genuine unit root and no amount of
         detrending removes it.
         Difference a trend-stationary series and you over-difference
         it, which is the trap two blocks above. Deciding between
         'deterministic trend' and 'stochastic trend' is what this
         pair of tests is for""")

    return results


if __name__ == "__main__":
    main()
