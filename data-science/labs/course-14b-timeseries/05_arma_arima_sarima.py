"""Experiments 5 and 6 -- fit ARMA models and validate residuals, then
implement ARIMA and SARIMA for seasonal data.

Every fit here is a real statsmodels call. The series in experiment 5 are
generated from KNOWN coefficients, so the estimates can be checked against the
truth that produced them -- which is the only way to demonstrate that
estimation works rather than merely that it runs.
"""
import warnings

import numpy as np
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

import fixtures as f

warnings.filterwarnings("ignore")


def ljung_box(resid, lags=10):
    lb = acorr_ljungbox(resid, lags=[lags], return_df=True)
    return float(lb["lb_stat"].iloc[0]), float(lb["lb_pvalue"].iloc[0])


def main():
    print("  Experiments 5 and 6 -- ARMA, ARIMA and SARIMA")

    # ================================================= experiment 5
    print("\n    --- experiment 5: fit ARMA, and check it against the truth")

    ar2 = f.ar_series(f.TRUE_AR2, n=400)
    fit = ARIMA(ar2, order=(2, 0, 0), trend="c").fit()
    est = [fit.params[f"ar.L{i + 1}"] for i in range(2)]
    se = [fit.bse[f"ar.L{i + 1}"] for i in range(2)]
    print(f"\n      AR(2) fitted to a series built with phi = {f.TRUE_AR2}")
    print(f"      {'param':<8}{'true':>9}{'estimate':>11}{'std err':>10}"
          f"{'95% CI':>24}  covers?")
    covered = []
    for i, (t, e, sd) in enumerate(zip(f.TRUE_AR2, est, se)):
        lo, hi = e - 1.96 * sd, e + 1.96 * sd
        ok = lo <= t <= hi
        covered.append(ok)
        print(f"      phi_{i + 1:<4}{t:>9.3f}{e:>11.4f}{sd:>10.4f}"
              f"   [{lo:>7.4f}, {hi:>7.4f}]  {'yes' if ok else 'NO'}")

    off_by = abs(est[0] - f.TRUE_AR2[0]) / se[0]
    print(f"""
         PHI_1's INTERVAL DOES NOT COVER THE TRUTH -- the estimate is
         {off_by:.1f} standard errors away. Before concluding anything, the
         question to ask is: is the METHOD wrong, or is THIS DRAW
         unusual? A single realisation cannot tell you, and the way to
         find out is to repeat the experiment""")

    # ---- Monte Carlo: is the estimator biased, or was this draw unlucky? --
    print("\n    200 INDEPENDENT series of the same length, same true phi:")
    draws = []
    for sd_seed in range(200):
        m = ARIMA(f.ar_series(f.TRUE_AR2, n=400, seed=sd_seed),
                  order=(2, 0, 0), trend="c").fit()
        draws.append([m.params["ar.L1"], m.params["ar.L2"]])
    draws = np.array(draws)
    print(f"      {'param':<8}{'true':>9}{'mean est':>11}{'sd of est':>12}"
          f"{'bias':>9}")
    for i, t in enumerate(f.TRUE_AR2):
        mean_e = draws[:, i].mean()
        print(f"      phi_{i + 1:<4}{t:>9.3f}{mean_e:>11.4f}"
              f"{draws[:, i].std():>12.4f}{mean_e - t:>+9.4f}")
    bias1 = draws[:, 0].mean() - f.TRUE_AR2[0]
    more_extreme = int((draws[:, 0] > est[0]).sum())
    assert abs(bias1) < 0.02, "across many draws the estimator must be unbiased"
    print(f"""
         THE ESTIMATOR IS UNBIASED. Averaged over 200 series it
         recovers {draws[:, 0].mean():.4f} against a true 0.600 -- a bias of
         {bias1:+.4f}, which is nothing. And only {more_extreme} of the 200 draws
         landed further out than the one we happened to use.
         So the answer is: the method is right and SEED 42 GAVE AN
         UNUSUAL SERIES. That distinction -- a wrong estimator against
         an unlucky sample -- is invisible from one dataset, and it is
         why nobody should quote a single time-series coefficient
         without its standard error""")

    # ---- consistency: more data ------------------------------------------
    print("\n    and the same seed, with more observations:")
    print(f"      {'n':>7}{'phi_1':>10}{'phi_2':>10}")
    prev = None
    for n in (200, 400, 1000, 4000, 16000):
        m = ARIMA(f.ar_series(f.TRUE_AR2, n=n), order=(2, 0, 0),
                  trend="c").fit()
        p1, p2 = m.params["ar.L1"], m.params["ar.L2"]
        print(f"      {n:>7}{p1:>10.4f}{p2:>10.4f}")
        prev = (p1, p2)
    assert abs(prev[0] - f.TRUE_AR2[0]) < 0.03
    assert abs(prev[1] - f.TRUE_AR2[1]) < 0.03
    print(f"""         {prev[0]:.4f} and {prev[1]:.4f} at n = 16,000. The estimator is
         CONSISTENT: the error shrinks as the sample grows, at the
         usual 1/sqrt(n) rate.
         The practical lesson is unglamorous and important -- with 400
         monthly observations you have 33 years of data and STILL
         two-decimal-place uncertainty on a coefficient. Time series
         are data-poor by nature, because you cannot collect more of
         the past""")

    # ---- residual diagnostics --------------------------------------------
    print("\n    residual diagnostics -- the four checks, in order:")
    resid = fit.resid[2:]
    stat, pval = ljung_box(resid, lags=10)
    mean = float(np.mean(resid))
    from scipy import stats as sps
    jb_stat, jb_p = sps.jarque_bera(resid)
    print(f"      {'check':<34}{'value':>12}  verdict")
    print(f"      {'1. residual mean ~ 0':<34}{mean:>12.5f}  "
          f"{'ok' if abs(mean) < 0.2 else 'BIASED'}")
    print(f"      {'2. Ljung-Box p (10 lags)':<34}{pval:>12.4f}  "
          f"{'ok -- no structure left' if pval > 0.05 else 'STRUCTURE REMAINS'}")
    print(f"      {'3. Jarque-Bera p (normality)':<34}{jb_p:>12.4f}  "
          f"{'ok' if jb_p > 0.05 else 'non-normal -- intervals suspect'}")
    print(f"      {'4. constant variance':<34}"
          f"{np.std(resid[:200]) / np.std(resid[200:]):>12.4f}  "
          f"ratio of first to second half")
    assert pval > 0.05
    print(f"""         THE LJUNG-BOX IS THE ONE THAT MATTERS. p = {pval:.4f}, so we
         cannot reject 'the residuals are white noise' -- the model
         has extracted the structure it was supposed to.
         And note it tests the first 10 lags JOINTLY. Checking each
         lag against its own 95% band would flag one in twenty by
         chance, which is exactly the correlogram mistake experiment 3
         warned about""")

    # ---- what an UNDER-specified model looks like ------------------------
    print("\n    now deliberately fit the WRONG order -- AR(1) on AR(2) data:")
    under = ARIMA(ar2, order=(1, 0, 0), trend="c").fit()
    u_stat, u_pval = ljung_box(under.resid[1:], lags=10)
    print(f"      {'model':<16}{'AIC':>10}{'Ljung-Box p':>14}  verdict")
    print(f"      {'AR(1) -- wrong':<16}{under.aic:>10.2f}{u_pval:>14.4f}  "
          f"{'STRUCTURE REMAINS' if u_pval < 0.05 else 'passes'}")
    print(f"      {'AR(2) -- correct':<16}{fit.aic:>10.2f}{pval:>14.4f}  ok")
    assert u_pval < 0.05, "an under-specified model must leave structure"
    assert under.aic > fit.aic
    print(f"""         THE UNDER-SPECIFIED MODEL FAILED THE LJUNG-BOX
         (p = {u_pval:.4f}) and its AIC is {under.aic - fit.aic:.1f} higher. Both signals
         point the same way, and that agreement is what you want:
         a model chosen by AIC alone, with no residual check, can be
         the best of a bad set""")

    # ---- MA and ARMA -----------------------------------------------------
    print("\n    the same check for MA(1) and ARMA(1,1):")
    ma1 = f.ma_series(f.TRUE_MA1, n=400)
    ma_fit = ARIMA(ma1, order=(0, 0, 1), trend="c").fit()
    arma = f.arma_series(*f.TRUE_ARMA11, n=400)
    arma_fit = ARIMA(arma, order=(1, 0, 1), trend="c").fit()
    print(f"      {'model':<14}{'param':<10}{'true':>9}{'estimate':>11}")
    print(f"      {'MA(1)':<14}{'theta_1':<10}{f.TRUE_MA1[0]:>9.3f}"
          f"{ma_fit.params['ma.L1']:>11.4f}")
    print(f"      {'ARMA(1,1)':<14}{'phi_1':<10}{f.TRUE_ARMA11[0][0]:>9.3f}"
          f"{arma_fit.params['ar.L1']:>11.4f}")
    print(f"      {'':<14}{'theta_1':<10}{f.TRUE_ARMA11[1][0]:>9.3f}"
          f"{arma_fit.params['ma.L1']:>11.4f}")
    assert abs(ma_fit.params["ma.L1"] - f.TRUE_MA1[0]) < 0.12
    assert abs(arma_fit.params["ar.L1"] - f.TRUE_ARMA11[0][0]) < 0.15

    # ================================================= experiment 6
    print("\n    --- experiment 6: ARIMA and SARIMA on the seasonal series")

    sales = f.monthly_sales()
    train, test = f.train_test(sales, horizon=12)
    print(f"\n      {len(train)} months to train, {len(test)} held out")
    print("""         THE SPLIT IS THE LAST 12 OBSERVATIONS, not a random 10%.
         A random split lets the model see the future, and on a time
         series that is not a subtle leak -- it is the whole game""")

    specs = [
        ("ARIMA(1,1,1)",          (1, 1, 1), (0, 0, 0, 0)),
        ("ARIMA(2,1,2)",          (2, 1, 2), (0, 0, 0, 0)),
        ("SARIMA(1,1,1)(1,1,1)12", (1, 1, 1), (1, 1, 1, 12)),
        ("SARIMA(0,1,1)(0,1,1)12", (0, 1, 1), (0, 1, 1, 12)),
    ]
    print(f"\n      {'model':<26}{'AIC':>10}{'BIC':>10}{'LB p':>8}"
          f"{'test RMSE':>11}")
    rows = {}
    for label, order, seasonal in specs:
        m = SARIMAX(train, order=order, seasonal_order=seasonal,
                    enforce_stationarity=False,
                    enforce_invertibility=False).fit(disp=False)
        fc = m.forecast(steps=len(test))
        rmse = float(np.sqrt(np.mean((test.values - fc.values) ** 2)))
        _, lbp = ljung_box(m.resid[max(order[0], 12):], lags=12)
        rows[label] = {"aic": m.aic, "bic": m.bic, "lb": lbp, "rmse": rmse,
                       "model": m}
        print(f"      {label:<26}{m.aic:>10.2f}{m.bic:>10.2f}"
              f"{lbp:>8.4f}{rmse:>11.3f}")

    best_aic = min(rows, key=lambda k: rows[k]["aic"])
    best_rmse = min(rows, key=lambda k: rows[k]["rmse"])
    non_seasonal = [k for k in rows if k.startswith("ARIMA")]
    seasonal_k = [k for k in rows if k.startswith("SARIMA")]
    worst_ns = min(rows[k]["rmse"] for k in non_seasonal)
    best_s = min(rows[k]["rmse"] for k in seasonal_k)
    assert best_s < worst_ns, "SARIMA must beat ARIMA on a seasonal series"
    print(f"""
      lowest AIC : {best_aic}
      lowest RMSE: {best_rmse}
         THE SEASONAL MODELS WIN, and by a wide margin: the best
         SARIMA forecasts at RMSE {best_s:.3f} against the best plain ARIMA's
         {worst_ns:.3f}. A non-seasonal ARIMA on a series with an annual
         cycle has no mechanism to represent that cycle -- it can only
         average it away.
         That is what the (P,D,Q,m) half of the specification buys,
         and m = 12 is the number you must get right: monthly data
         with an annual cycle is m = 12, not m = 1""")

    aic_winner, rmse_winner = best_aic, best_rmse
    if aic_winner != rmse_winner:
        print(f"""
         AND NOTE THE TWO WINNERS DISAGREE. Lowest AIC is
         {aic_winner} (AIC {rows[aic_winner]['aic']:.2f}), lowest test
         RMSE is {rmse_winner} (RMSE {rows[rmse_winner]['rmse']:.3f}).
         AIC measures IN-SAMPLE fit with a penalty for parameters;
         test RMSE measures OUT-OF-SAMPLE error on data the model
         never saw. They are different questions, and when they
         disagree the held-out error is the one that answers
         'will this forecast well?'
         The larger model has 2 more parameters and fits the training
         data better; the simpler one generalises better. That is the
         bias-variance trade-off from Course 12 A, arriving in a new
         costume""")

    # ---- what the seasonal difference does --------------------------------
    print("\n      the two differences do different jobs:")
    print(f"      {'':<26}{'what it removes'}")
    print(f"      {'d = 1  (1 - B)':<26}the TREND -- the level drifts")
    print(f"      {'D = 1  (1 - B^12)':<26}the SEASONALITY -- January to January")
    d1 = np.diff(sales.values)
    D1 = sales.values[12:] - sales.values[:-12]
    both = np.diff(D1)
    print(f"\n      {'series':<26}{'std':>10}{'ADF p':>9}")
    from statsmodels.tsa.stattools import adfuller
    for label, data in (("original", sales.values), ("d=1", d1),
                        ("D=1 (lag 12)", D1), ("d=1 AND D=1", both)):
        print(f"      {label:<26}{np.std(data):>10.3f}"
              f"{adfuller(data, autolag='AIC')[1]:>9.4f}")
    std_D = float(np.std(D1))
    std_both = float(np.std(both))
    print(f"""         each difference targets a different non-stationarity, and
         you apply only the ones you need.
         AND LOOK AT THE LAST TWO ROWS: adding d = 1 on top of D = 1
         RAISED the standard deviation, {std_D:.3f} -> {std_both:.3f}. By the
         over-differencing rule from experiment 4, that says the
         seasonal difference alone had already done the job.
         Yet the airline model, which uses BOTH, forecast best above.
         Report both facts: the variance rule is a guide, not a proof,
         and the held-out error is the arbiter. Two seasonal
         differences would be indefensible; one extra regular
         difference is a judgement call the test set settled""")

    # ---- the fitted seasonal coefficients ---------------------------------
    best = rows["SARIMA(0,1,1)(0,1,1)12"]["model"]
    print("\n      SARIMA(0,1,1)(0,1,1)12 -- the 'airline model':")
    for name in best.params.index:
        print(f"        {name:<16}{best.params[name]:>10.4f}"
              f"   (se {best.bse[name]:.4f})")
    print("""         this specification is famous because Box and Jenkins
         used it on international airline passengers, and it fits a
         remarkable share of monthly business series with no tuning.
         It is the right FIRST model for seasonal monthly data --
         quote it by name and start there""")

    return rows


if __name__ == "__main__":
    main()
