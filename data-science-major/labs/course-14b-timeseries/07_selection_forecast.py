"""Experiments 7 and 8 -- model selection by AIC/BIC and cross-validation, then
forecasting with prediction intervals.

The two experiments belong together because they answer the same question from
opposite ends: AIC asks "which model fits best per parameter spent?" and
rolling-origin cross-validation asks "which model actually forecast well?"
They do not always agree, and when they disagree the second one wins.
"""
import warnings

import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

import fixtures as f

warnings.filterwarnings("ignore")


def fit_sarimax(series, order, seasonal=(0, 0, 0, 0)):
    return SARIMAX(series, order=order, seasonal_order=seasonal,
                   enforce_stationarity=False,
                   enforce_invertibility=False).fit(disp=False)


def rolling_origin_cv(series, order, seasonal, initial=72, horizon=6, step=6):
    """Rolling-origin cross-validation -- the ONLY correct CV for a series.

    Train on [0, t), forecast the next `horizon`, score, then move t forward.
    k-fold CV is invalid here: it would train on data that comes AFTER the
    validation fold, which is time travel.
    """
    errors, folds = [], 0
    t = initial
    while t + horizon <= len(series):
        m = fit_sarimax(series.iloc[:t], order, seasonal)
        fc = m.forecast(steps=horizon)
        errors.extend(series.iloc[t:t + horizon].values - fc.values)
        folds += 1
        t += step
    return float(np.sqrt(np.mean(np.square(errors)))), folds


def main():
    print("  Experiments 7 and 8 -- model selection and forecasting")

    sales = f.monthly_sales()
    train, test = f.train_test(sales, horizon=12)

    # ================================================= experiment 7
    print("\n    --- experiment 7: AIC, BIC and rolling-origin CV")

    print("""
    AIC = -2 log L + 2k          penalty 2 per parameter
    BIC = -2 log L + k log n     penalty log(n) per parameter
         with n = 108, log(n) = 4.68, so BIC penalises a parameter
         more than twice as hard as AIC. BIC therefore picks SMALLER
         models, and that difference is the whole of the comparison""")

    grid = [
        ((0, 1, 1), (0, 1, 1, 12)),
        ((1, 1, 1), (0, 1, 1, 12)),
        ((1, 1, 1), (1, 1, 1, 12)),
        ((2, 1, 1), (1, 1, 1, 12)),
        ((2, 1, 2), (1, 1, 1, 12)),
    ]
    print(f"\n      {'model':<28}{'k':>3}{'AIC':>10}{'BIC':>10}{'CV RMSE':>10}")
    rows = {}
    for order, seasonal in grid:
        label = (f"SARIMA{order}"
                 f"{seasonal[:3]}{seasonal[3]}".replace(" ", ""))
        m = fit_sarimax(train, order, seasonal)
        cv_rmse, folds = rolling_origin_cv(train, order, seasonal)
        k = len(m.params)
        rows[label] = {"aic": m.aic, "bic": m.bic, "cv": cv_rmse, "k": k,
                       "order": order, "seasonal": seasonal}
        print(f"      {label:<28}{k:>3}{m.aic:>10.2f}{m.bic:>10.2f}"
              f"{cv_rmse:>10.3f}")

    by_aic = min(rows, key=lambda x: rows[x]["aic"])
    by_bic = min(rows, key=lambda x: rows[x]["bic"])
    by_cv = min(rows, key=lambda x: rows[x]["cv"])
    print(f"\n      lowest AIC : {by_aic}  (k = {rows[by_aic]['k']})")
    print(f"      lowest BIC : {by_bic}  (k = {rows[by_bic]['k']})")
    print(f"      lowest CV  : {by_cv}  (k = {rows[by_cv]['k']})")
    assert rows[by_bic]["k"] <= rows[by_aic]["k"], "BIC must not pick a larger model"
    if by_aic == by_bic:
        print(f"""         AIC AND BIC AGREED here, on a {rows[by_aic]['k']}-parameter model. That
         happens when one specification is clearly better than its
         neighbours -- the heavier BIC penalty only bites when two
         models fit almost equally well.
         When they DO disagree, BIC always picks the smaller one, by
         construction: with n = {len(train)}, log(n) = {np.log(len(train)):.2f}, so BIC charges more
         than twice AIC's rate per parameter.""")
    else:
        print(f"""         BIC PICKED A MODEL WITH {rows[by_aic]['k'] - rows[by_bic]['k']} FEWER PARAMETER(S), which is
         what a heavier penalty does by construction.""")
    print(f"""         Which to use? BIC is CONSISTENT -- given enough data it
         picks the true model if it is in the set. AIC is EFFICIENT --
         it picks the best predictor, whether or not the truth is in
         the set. For FORECASTING, which is what this course is for,
         AIC is the better default.
         AND ROLLING-ORIGIN CV IS BETTER STILL. Here it disagreed with
         both: it chose {by_cv} ({rows[by_cv]['k']} parameters) where
         AIC and BIC chose {by_aic} ({rows[by_aic]['k']}).
         AIC estimates out-of-sample error from a formula and an
         assumption; CV measures it. When you can afford the refits,
         measure""" if by_cv != by_aic else """         Which to use? BIC is consistent, AIC is efficient, and for
         forecasting AIC is the better default -- and here CV agreed
         with it""")

    print(f"\n      the CV used {rolling_origin_cv(train, (0,1,1), (0,1,1,12))[1]} "
          f"rolling folds, each training on everything before the fold")
    print("""         k-FOLD CROSS-VALIDATION IS INVALID ON A TIME SERIES.
         Randomly held-out folds put future observations in the
         training set, so the model interpolates a gap it has seen
         both sides of -- which is not forecasting, and scores far too
         well. Rolling origin is the correct analogue, and every fold
         trains only on the past""")

    # ================================================= experiment 8
    print("\n    --- experiment 8: forecasts, and their intervals")

    best = rows[by_cv]
    m = fit_sarimax(train, best["order"], best["seasonal"])
    res = m.get_forecast(steps=12)
    mean = res.predicted_mean
    ci = res.conf_int(alpha=0.05)
    lo = ci.iloc[:, 0].values
    hi = ci.iloc[:, 1].values
    actual = test.values

    print(f"\n      {by_cv}, 12 months ahead")
    print(f"      {'h':>3}{'actual':>10}{'forecast':>10}{'lo 95':>10}"
          f"{'hi 95':>10}{'width':>9}  in?")
    inside = 0
    for h in range(12):
        ok = lo[h] <= actual[h] <= hi[h]
        inside += ok
        print(f"      {h + 1:>3}{actual[h]:>10.2f}{mean.values[h]:>10.2f}"
              f"{lo[h]:>10.2f}{hi[h]:>10.2f}{hi[h] - lo[h]:>9.2f}"
              f"  {'yes' if ok else 'NO'}")
    cover = inside / 12
    rmse = float(np.sqrt(np.mean((actual - mean.values) ** 2)))
    mae = float(np.mean(np.abs(actual - mean.values)))
    print(f"\n      coverage {inside}/12 = {cover:.0%}   RMSE {rmse:.3f}   "
          f"MAE {mae:.3f}")
    assert cover >= 0.7, "a 95% interval should cover most of the time"

    from scipy import stats as sps
    binom_p = float(sps.binomtest(inside, 12, 0.95).pvalue)
    print(f"""
         AND THE COVERAGE IS {cover:.0%}, NOT 95%. Report that, do not
         round it up. Two things are going on, and both matter:
         1. TWELVE POINTS IS A TINY SAMPLE. Under a true 95% interval,
            seeing {inside} or fewer hits out of 12 has probability
            {binom_p:.3f} -- unusual, not damning.
         2. SARIMA INTERVALS ARE KNOWN TO BE TOO NARROW. They treat
            the fitted parameters as if they were the true ones, so
            they price in shock uncertainty and ignore ESTIMATION
            uncertainty. With 108 observations and 5 parameters that
            omission is not small.
         The honest summary: nominal 95%, empirical {cover:.0%}, and if
         the interval matters for a decision, widen it or get it by
         bootstrap or backtesting rather than from the formula""")

    # ---- the widening ----------------------------------------------------
    w1, w12 = hi[0] - lo[0], hi[11] - lo[11]
    print(f"""
         THE INTERVAL WIDENS WITH THE HORIZON: {w1:.2f} at h = 1 and
         {w12:.2f} at h = 12, a factor of {w12 / w1:.2f}. That is not a defect --
         it is the model correctly reporting that it knows less about
         next December than about next month.
         A point forecast without an interval hides exactly this, and
         it is the single most common failure in a forecasting
         report""")

    print("""
      why the interval grows, in one line:
        Var(y_{t+h} | data) accumulates the variance of every shock
        between now and t+h. For a random walk it grows LINEARLY in h,
        so the interval widens as sqrt(h) -- and for a stationary
        series it flattens out at the unconditional variance""")

    # demonstrate both shapes
    rw = f.random_walk(n=200)
    rw_m = fit_sarimax(rw, (0, 1, 0))
    rw_ci = rw_m.get_forecast(steps=16).conf_int()
    rw_w = (rw_ci.iloc[:, 1] - rw_ci.iloc[:, 0]).values
    ar_m = fit_sarimax(f.ar_series((0.5,), n=200), (1, 0, 0))
    ar_ci = ar_m.get_forecast(steps=16).conf_int()
    ar_w = (ar_ci.iloc[:, 1] - ar_ci.iloc[:, 0]).values
    print(f"\n      {'h':>3}{'random walk width':>20}{'ratio to sqrt(h)':>18}"
          f"{'AR(1) width':>14}")
    for h in (1, 4, 9, 16):
        print(f"      {h:>3}{rw_w[h - 1]:>20.3f}"
              f"{rw_w[h - 1] / (rw_w[0] * np.sqrt(h)):>18.4f}"
              f"{ar_w[h - 1]:>14.3f}")
    assert abs(rw_w[15] / (rw_w[0] * 4) - 1) < 0.05, "random walk widens as sqrt(h)"
    assert ar_w[15] / ar_w[0] < 1.5, "a stationary forecast interval flattens"
    print(f"""         THE RANDOM WALK'S INTERVAL IS EXACTLY sqrt(h) TIMES ITS
         one-step width -- the ratio column is 1.0000 at every
         horizon. The AR(1)'s stops growing: {ar_w[0]:.3f} to {ar_w[15]:.3f} and
         then flat, because a stationary process forgets its starting
         point and the forecast converges on the unconditional mean.
         That contrast is worth drawing: it is the difference between
         a series you can forecast far ahead and one you cannot""")

    # ---- naive baselines, which any model must beat -----------------------
    print("\n    the two baselines every forecast must beat:")
    naive = np.repeat(train.values[-1], 12)
    snaive = train.values[-12:]
    print(f"      {'method':<28}{'RMSE':>9}{'MAE':>9}")
    results = {}
    for label, pred in (("naive (last value)", naive),
                        ("seasonal naive (last year)", snaive),
                        (f"{by_cv}", mean.values)):
        r = float(np.sqrt(np.mean((actual - pred) ** 2)))
        a = float(np.mean(np.abs(actual - pred)))
        results[label] = r
        print(f"      {label:<28}{r:>9.3f}{a:>9.3f}")
    assert results[by_cv] < results["seasonal naive (last year)"]
    improvement = 100 * (1 - results[by_cv] / results["seasonal naive (last year)"])
    print(f"""         THE MODEL BEATS SEASONAL NAIVE BY {improvement:.0f}%. Quote that
         comparison, not the RMSE alone: an RMSE of {results[by_cv]:.2f} means
         nothing until you know that repeating last year scores
         {results['seasonal naive (last year)']:.2f}.
         Seasonal naive is the honest baseline for seasonal data, and
         a surprising number of published forecasting models fail to
         beat it. It is this course's DummyClassifier""")

    return rows


if __name__ == "__main__":
    main()
