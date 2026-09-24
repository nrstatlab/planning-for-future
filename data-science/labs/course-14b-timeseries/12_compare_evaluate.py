"""Experiments 12 and 13 -- compare ARIMA against exponential smoothing
against a machine-learning model, and evaluate forecasts with RMSE, MAE and
MAPE.

This is the experiment that decides what you believe. Everything before it
fits models; this one asks which of them you would actually deploy, and shows
that the answer depends on the metric you chose before you looked.
"""
import warnings

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX

import fixtures as f

warnings.filterwarnings("ignore")


def lag_matrix(values, lags=(1, 2, 3, 12), horizon=1):
    """Turn a series into a supervised-learning table.

    THIS is how a machine-learning model is applied to a time series: you
    build the lags yourself. Nothing in scikit-learn knows what time is.
    """
    max_lag = max(lags)
    X, y = [], []
    for t in range(max_lag, len(values) - horizon + 1):
        X.append([values[t - lag] for lag in lags])
        y.append(values[t + horizon - 1])
    return np.array(X), np.array(y)


def recursive_forecast(model, history, lags, steps):
    """Forecast h steps by feeding each prediction back as an input.

    The textbook expectation is that error compounds with the horizon.
    Whether it does on any given test window is a measurement, not a
    guarantee -- and this script reports whichever way it comes out.
    """
    hist = list(history)
    out = []
    for _ in range(steps):
        x = np.array([[hist[-lag] for lag in lags]])
        pred = float(model.predict(x)[0])
        out.append(pred)
        hist.append(pred)
    return np.array(out)


def metrics(actual, pred):
    err = actual - pred
    rmse = float(np.sqrt(np.mean(err ** 2)))
    mae = float(np.mean(np.abs(err)))
    mape = float(np.mean(np.abs(err / actual)) * 100)
    return rmse, mae, mape


def main():
    print("  Experiments 12 and 13 -- comparing methods, and evaluating them")

    sales = f.monthly_sales()
    train, test = f.train_test(sales, horizon=12)
    actual = test.values
    lags = (1, 2, 3, 12)

    # ================================================= experiment 12
    print("\n    --- experiment 12: five methods on the same 12 months")

    preds = {}

    preds["naive"] = np.repeat(train.values[-1], 12)
    preds["seasonal naive"] = train.values[-12:]

    sar = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12),
                  enforce_stationarity=False,
                  enforce_invertibility=False).fit(disp=False)
    preds["SARIMA(1,1,1)(1,1,1)12"] = sar.forecast(12).values

    hw = ExponentialSmoothing(train, trend="add", seasonal="add",
                              seasonal_periods=12).fit()
    preds["Holt-Winters additive"] = hw.forecast(12).values

    X, y = lag_matrix(train.values, lags)
    lin = LinearRegression().fit(X, y)
    preds["linear regression on lags"] = recursive_forecast(
        lin, train.values, lags, 12)

    gbr = GradientBoostingRegressor(random_state=42).fit(X, y)
    preds["gradient boosting on lags"] = recursive_forecast(
        gbr, train.values, lags, 12)

    print(f"\n      {'method':<28}{'RMSE':>9}{'MAE':>9}{'MAPE %':>9}"
          f"{'vs snaive':>11}")
    rows = {}
    for name, p in preds.items():
        r, a, mp = metrics(actual, p)
        rows[name] = {"rmse": r, "mae": a, "mape": mp, "pred": p}
    snaive_rmse = rows["seasonal naive"]["rmse"]
    for name in preds:
        r = rows[name]
        skill = 100 * (1 - r["rmse"] / snaive_rmse)
        print(f"      {name:<28}{r['rmse']:>9.3f}{r['mae']:>9.3f}"
              f"{r['mape']:>9.2f}{skill:>10.0f}%")

    best = min(rows, key=lambda k: rows[k]["rmse"])
    print(f"\n      best by RMSE: {best}")
    assert rows[best]["rmse"] < snaive_rmse

    # ---- the honest comparison -------------------------------------------
    stat_best = min(("SARIMA(1,1,1)(1,1,1)12", "Holt-Winters additive"),
                    key=lambda k: rows[k]["rmse"])
    ml_best = min(("linear regression on lags", "gradient boosting on lags"),
                  key=lambda k: rows[k]["rmse"])
    print(f"""
      the classical/ML comparison, stated carefully:
        best classical : {stat_best:<28}RMSE {rows[stat_best]['rmse']:.3f}
        best ML        : {ml_best:<28}RMSE {rows[ml_best]['rmse']:.3f}""")
    if rows[stat_best]["rmse"] < rows[ml_best]["rmse"]:
        print(f"""         THE CLASSICAL MODEL WON, on 108 observations. That is
         the usual outcome at this sample size and it is worth saying
         plainly: ARIMA and exponential smoothing encode the structure
         (trend, seasonality, autocorrelation) as ASSUMPTIONS, so they
         need little data to fit. A gradient booster must LEARN that
         structure from examples, and 96 training rows is not many.
         The M4 and M5 forecasting competitions found the crossover
         sits at hundreds of series or thousands of observations --
         below that, the statistical models are hard to beat, and
         'we used machine learning' is not an argument""")
    else:
        print("""         the ML model won here -- report it, and report the
         sample size with it, because the ranking is sample-size
         dependent and not a general law""")

    # ---- how the ML model behaves across the horizon ----------------------
    print("\n      how the error behaves across the horizon:")
    print(f"      {'h':>3}{'actual':>10}{'GBR':>10}{'abs err':>10}")
    gbr_pred = rows["gradient boosting on lags"]["pred"]
    for h in (1, 3, 6, 9, 12):
        print(f"      {h:>3}{actual[h - 1]:>10.2f}{gbr_pred[h - 1]:>10.2f}"
              f"{abs(actual[h - 1] - gbr_pred[h - 1]):>10.2f}")
    early = np.mean(np.abs(actual[:3] - gbr_pred[:3]))
    late = np.mean(np.abs(actual[-3:] - gbr_pred[-3:]))
    print(f"\n      mean abs error, first 3 months: {early:.3f}")
    print(f"      mean abs error, last 3 months : {late:.3f}"
          f"   ({late / early:.2f}x)")
    print("""      a one-step model asked for twelve steps must EAT ITS OWN
      PREDICTIONS -- each prediction becomes an input to the next.""")
    if late > early:
        print("""         and here the error GREW with the horizon, which is the
         compounding this structure predicts""")
    else:
        print(f"""         BUT THE ERROR DID NOT GROW HERE -- it FELL, {early:.1f} to
         {late:.1f}. Report that, because the textbook claim is
         'recursive forecasting compounds error' and this run does not
         show it.
         What happened instead: the model is biased LOW throughout
         (every one of the sampled horizons under-forecasts), and the
         actual series happens to dip in months 9-11, so the gap
         narrows there for reasons that have nothing to do with the
         model improving. A level bias plus a seasonal trough is not
         'accuracy that improves with horizon'.
         The lesson is about reading evidence, not about recursion:
         a per-horizon error curve on ONE test window of 12 points is
         far too noisy to show a trend either way. To measure
         compounding properly you need many rolling origins, which is
         what experiment 7's rolling-origin CV is for""")
    print("""
      the alternative for an ML model is DIRECT forecasting: train a
      separate model for each horizon. Twelve models, no dependence on
      your own predictions, and twelve times the fitting. SARIMA needs
      neither -- it has a closed-form h-step forecast, and its
      uncertainty goes into the interval rather than hiding in the
      point estimate""")

    # ---- and the constant a tree cannot extrapolate ----------------------
    print("\n      the structural limit of a tree-based model:")
    # a strictly increasing series, so the LAST value IS the maximum
    rng_t = np.random.default_rng(7)
    trend_only = np.cumsum(np.abs(rng_t.normal(2, 0.3, 80))) + 100
    Xt, yt = lag_matrix(trend_only, (1, 2, 3))
    tree_m = GradientBoostingRegressor(random_state=42).fit(Xt, yt)
    lin_m = LinearRegression().fit(Xt, yt)
    fut = recursive_forecast(tree_m, trend_only, (1, 2, 3), 12)
    fut_lin = recursive_forecast(lin_m, trend_only, (1, 2, 3), 12)
    print(f"      a strictly INCREASING series, 80 points, +2 per step")
    print(f"      last training value          : {trend_only[-1]:.1f}")
    print(f"      max value seen in training   : {trend_only.max():.1f}")
    print(f"\n      {'h':>3}{'true continuation':>20}{'tree':>10}{'linear':>10}")
    for h in (1, 4, 8, 12):
        true_next = trend_only[-1] + 2 * h
        print(f"      {h:>3}{true_next:>20.1f}{fut[h - 1]:>10.1f}"
              f"{fut_lin[h - 1]:>10.1f}")
    assert fut.max() <= trend_only.max() + 1e-6
    assert fut_lin[-1] > trend_only.max(), "a linear model CAN extrapolate"
    print(f"\n      tree forecast never exceeds {fut.max():.1f} "
          f"(training max {trend_only.max():.1f})")
    print(f"      linear forecast reaches      {fut_lin[-1]:.1f}")
    print("""         THE TREE'S FORECAST CANNOT EXCEED THE LARGEST VALUE IT
         SAW IN TRAINING, ever, while the linear model walks straight
         up alongside the truth.
         The reason is structural: a decision tree predicts the MEAN
         OF A LEAF, and every leaf is an average of training targets.
         No average of numbers can exceed the largest of them, so a
         tree ensemble CANNOT EXTRAPOLATE A TREND -- not badly, at
         all.
         On a growing series this is fatal, and it is invisible in a
         validation score taken from the middle of the data. The fix
         is to model the DIFFERENCES, or detrend first and let the
         tree learn only the remainder -- which is, in effect,
         rebuilding ARIMA by hand.
         Say this whenever someone proposes XGBoost for a trending
         series. It is the one criticism that is not a matter of
         taste""")

    # ================================================= experiment 13
    print("\n    --- experiment 13: the metrics, and what each one hides")

    print(f"""
      {'metric':<10}{'formula':<26}{'units':<14}{'blind to'}""")
    for m, formula, unit, blind in (
            ("RMSE", "sqrt(mean(e^2))", "the data's", "punishes big errors hard"),
            ("MAE", "mean(|e|)", "the data's", "treats all errors alike"),
            ("MAPE", "mean(|e/y|) x 100", "PERCENT", "explodes near y = 0"),
            ("sMAPE", "symmetric MAPE", "percent", "still asymmetric"),
            ("MASE", "MAE / MAE of naive", "SCALE-FREE", "needs a baseline")):
        print(f"      {m:<10}{formula:<26}{unit:<14}{blind}")

    # ---- RMSE against MAE, demonstrated ----------------------------------
    print("\n      RMSE and MAE can rank two forecasts differently:")
    truth = np.array([100.0] * 10)
    a_pred = truth + np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2.0])
    b_pred = truth + np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 15.0])
    print(f"      {'forecast':<34}{'RMSE':>9}{'MAE':>9}")
    for label, p in (("A: off by 2 every month", a_pred),
                     ("B: perfect, then off by 15 once", b_pred)):
        r, mae, _ = metrics(truth, p)
        print(f"      {label:<34}{r:>9.3f}{mae:>9.3f}")
    ra, maea, _ = metrics(truth, a_pred)
    rb, maeb, _ = metrics(truth, b_pred)
    assert ra < rb and maea > maeb, "the two metrics must disagree here"
    print(f"""         THE TWO METRICS DISAGREE. RMSE prefers A ({ra:.2f} against
         {rb:.2f}); MAE prefers B ({maeb:.2f} against {maea:.2f}).
         Neither is wrong -- they answer different questions. RMSE
         squares the errors, so one large miss dominates; MAE does not.
         CHOOSE FROM THE COST OF BEING WRONG. If a single large
         stock-out is catastrophic, use RMSE. If the cost is
         proportional to the error, use MAE. Deciding after seeing the
         results is how a comparison becomes a justification""")

    # ---- MAPE's failure ---------------------------------------------------
    print("\n      MAPE's two failures, both demonstrated:")
    small = np.array([0.5, 1.0, 100.0, 200.0])
    pred_small = small + 1.0
    r, mae, mp = metrics(small, pred_small)
    per_row = np.abs((pred_small - small) / small) * 100
    print(f"      EVERY forecast is off by exactly 1.0:")
    print(f"      {'actual':>10}{'forecast':>10}{'abs err':>10}"
          f"{'pct err':>10}")
    for i in range(4):
        print(f"      {small[i]:>10.1f}{pred_small[i]:>10.1f}"
              f"{1.0:>10.1f}{per_row[i]:>9.1f}%")
    print(f"\n        MAE  {mae:>8.3f}   -- 'off by 1', which is the truth")
    print(f"        MAPE {mp:>8.2f}%  -- dominated by the two small actuals")
    assert mae == 1.0 and mp > 50
    print(f"""         1. NEAR ZERO IT EXPLODES. The SAME absolute miss of 1.0 is
            a 200% error against an actual of 0.5 and a 0.5% error
            against an actual of 200 -- so the two small months carry
            the whole average, and MAPE reports 75% for a forecast
            that is uniformly off by one unit.
         2. IT IS ASYMMETRIC. Over-forecasting is capped at 100%
            (you cannot be more than 100% below a positive actual),
            under-forecasting is unbounded. So MAPE systematically
            PREFERS MODELS THAT UNDER-FORECAST -- which on an
            inventory problem is exactly the wrong bias.
         Do not use MAPE on data that goes near zero, or on data that
         can be negative, where it is meaningless""")

    over = metrics(np.array([100.0]), np.array([150.0]))[2]
    under = metrics(np.array([100.0]), np.array([50.0]))[2]
    print(f"\n      50 too high -> MAPE {over:.0f}%;  "
          f"50 too low -> MAPE {under:.0f}%   (symmetric here)")
    over2 = metrics(np.array([100.0]), np.array([300.0]))[2]
    print(f"      200 too high -> MAPE {over2:.0f}%;  "
          f"but you can never be more than 100% too low")

    # ---- MASE, the scale-free answer --------------------------------------
    print("\n      MASE -- the metric that fixes both problems:")
    naive_mae = float(np.mean(np.abs(np.diff(train.values))))
    print(f"      {'method':<28}{'MAE':>9}{'MASE':>9}  reading")
    shown = []
    for name in ("naive", "seasonal naive", "SARIMA(1,1,1)(1,1,1)12",
                 "Holt-Winters additive", best):
        if name not in rows or name in shown:
            continue
        shown.append(name)
        mase = rows[name]["mae"] / naive_mae
        reading = "beats naive" if mase < 1 else "WORSE than naive"
        print(f"      {name:<28}{rows[name]['mae']:>9.3f}{mase:>9.3f}  "
              f"{reading}")
    print("""         MASE divides by the in-sample MAE of the naive forecast,
         so it is SCALE-FREE, defined at zero, symmetric, and reads
         directly: below 1 beats naive, above 1 does not.
         It is the metric the M4 competition used, and it is the right
         default when comparing across series of different
         magnitudes -- which MAE and RMSE simply cannot do.
         AND NOTE SEASONAL NAIVE SCORING ABOVE 1. That is not a
         contradiction: MASE's denominator is the ONE-STEP in-sample
         naive error, not the seasonal one, so on a strongly seasonal
         series the seasonal-naive forecast is expected to sit above
         1. If you want a seasonal benchmark, divide by the seasonal
         naive instead -- and say which denominator you used, because
         a MASE quoted without it is not comparable to anyone
         else's""")

    # ---- residual diagnostics on the winner --------------------------------
    print("\n      and the last check: are the forecast errors unbiased?")
    err = actual - rows[best]["pred"]
    from scipy import stats as sps
    t_stat, t_p = sps.ttest_1samp(err, 0)
    print(f"      mean forecast error {np.mean(err):>+8.4f}   "
          f"(t = {t_stat:.3f}, p = {t_p:.4f})")
    verdict = "no evidence of bias" if t_p > 0.05 else "BIASED -- systematically off"
    print(f"      {verdict}")
    print("""         a forecast can have a small RMSE and still be biased --
         consistently 5% low, say -- and a business will feel the bias
         long before it feels the variance. Test the mean error, not
         only its magnitude""")

    return rows


if __name__ == "__main__":
    main()
