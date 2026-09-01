"""Experiment 16 (Python equivalent) -- time series and ARIMA fundamentals.

R version: ../16_arima.R  (ts, decompose, adf.test, auto.arima, forecast)

statsmodels is not installed, so rather than call a black-box ARIMA this file
implements the pieces the syllabus actually examines -- decomposition,
differencing, stationarity, ACF and PACF -- from first principles. That is more
useful anyway: these are the calculations an exam asks you to perform by hand.
"""
import math

# 36 months of sales: level 100, upward trend, 12-month seasonality, noise.
# Built deterministically so the numbers are reproducible.
def make_series(n=36):
    out = []
    for t in range(n):
        trend = 100 + 2.0 * t
        season = 15 * math.sin(2 * math.pi * t / 12)
        noise = 3 * math.sin(t * 7.13)          # deterministic pseudo-noise
        out.append(round(trend + season + noise, 2))
    return out


SERIES = make_series()


def moving_average(v, window):
    """Centred moving average -- the trend estimate in classical decomposition."""
    half = window // 2
    out = [None] * len(v)
    for i in range(half, len(v) - half):
        if window % 2 == 0:      # even window needs the 2xM smoothing
            block = v[i - half:i + half + 1]
            out[i] = (sum(block[1:-1]) + (block[0] + block[-1]) / 2) / window
        else:
            out[i] = sum(v[i - half:i + half + 1]) / window
    return out


def difference(v, lag=1):
    return [v[i] - v[i - lag] for i in range(lag, len(v))]


def acf(v, max_lag):
    n = len(v)
    m = sum(v) / n
    denom = sum((x - m) ** 2 for x in v)
    out = []
    for k in range(1, max_lag + 1):
        num = sum((v[i] - m) * (v[i - k] - m) for i in range(k, n))
        out.append(num / denom)
    return out


def pacf(v, max_lag):
    """PACF by the Durbin-Levinson recursion."""
    r = [1.0] + acf(v, max_lag)
    phi = [[0.0] * (max_lag + 1) for _ in range(max_lag + 1)]
    out = []
    for k in range(1, max_lag + 1):
        if k == 1:
            phi[1][1] = r[1]
        else:
            num = r[k] - sum(phi[k - 1][j] * r[k - j] for j in range(1, k))
            den = 1 - sum(phi[k - 1][j] * r[j] for j in range(1, k))
            phi[k][k] = num / den if den != 0 else 0.0
            for j in range(1, k):
                phi[k][j] = phi[k - 1][j] - phi[k][k] * phi[k - 1][k - j]
        out.append(phi[k][k])
    return out


def spark(values, width=40):
    lo, hi = min(values), max(values)
    span = hi - lo or 1
    return "".join("▁▂▃▄▅▆▇█"[min(7, int((v - lo) / span * 7))] for v in values)


if __name__ == "__main__":
    print("THE SERIES                     R: ts(sales, frequency = 12)")
    print(f"  {len(SERIES)} monthly observations")
    print(f"  {spark(SERIES)}")
    print(f"  first 6: {SERIES[:6]}")

    print("\nDECOMPOSITION                  R: decompose(ts)")
    trend = moving_average(SERIES, 12)
    known = [(i, t) for i, t in enumerate(trend) if t is not None]
    print(f"  trend (12-month centred MA), first and last known values:")
    print(f"    t={known[0][0]:2d} -> {known[0][1]:7.2f}")
    print(f"    t={known[-1][0]:2d} -> {known[-1][1]:7.2f}")
    slope = (known[-1][1] - known[0][1]) / (known[-1][0] - known[0][0])
    print(f"  implied slope = {slope:.3f} per month  (series was built with 2.0)")

    print("\nSTATIONARITY BY DIFFERENCING   R: diff(ts) ; ndiffs(ts)")
    d1 = difference(SERIES)
    for name, v in (("original", SERIES), ("differenced", d1)):
        m = sum(v) / len(v)
        sd = (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5
        first, second = v[:len(v)//2], v[len(v)//2:]
        drift = abs(sum(second)/len(second) - sum(first)/len(first))
        print(f"  {name:<12} mean={m:8.2f}  sd={sd:6.2f}  "
              f"first-half vs second-half mean gap = {drift:7.2f}")
    print("  A large gap between the halves' means IS non-stationarity in the")
    print("  mean. Differencing collapses it, which is what d=1 achieves.")

    print("\nACF -- RAW SERIES              R: acf(ts)")
    a = acf(SERIES, 14)
    for k, v in enumerate(a, 1):
        print(f"    lag {k:2d}  {v:+.4f}  {'+' * int(abs(v) * 30)}")
    print("  Slow, monotonic decay and nothing else. This is the classic")
    print("  signature of a TREND, and it is so dominant that the seasonality")
    print("  built into this series is completely invisible here.")

    print("\nACF -- DIFFERENCED SERIES      R: acf(diff(ts))")
    ad = acf(d1, 14)
    for k, v in enumerate(ad, 1):
        bar = "+" * int(abs(v) * 30)
        marker = ""
        if k == 12:
            marker = "   <- local MAXIMUM: period-12 seasonality"
        elif k == 6:
            marker = "   <- MINIMUM: half a period out of phase"
        print(f"    lag {k:2d}  {v:+.4f}  {bar}{marker}")

    print("\n  💡 THE LESSON: seasonality was NOT visible in the raw ACF, because")
    print("  the trend swamped it. Only after differencing does the oscillation")
    print("  appear -- negative around lag 6, peaking again at lag 12. This is")
    print("  why the order of operations matters: difference FIRST, then read")
    print("  the ACF and PACF. Reading them on a trending series tells you")
    print("  almost nothing except 'there is a trend'.")

    print("\nPACF                           R: pacf(ts)")
    for k, v in enumerate(pacf(SERIES, 8), 1):
        print(f"    lag {k:2d}  {v:+.4f}")

    print("\n  READING THEM (Unit 5 A.4):")
    print("    ACF tails off, PACF cuts off after lag p  -> AR(p), p from PACF")
    print("    ACF cuts off after lag q, PACF tails off  -> MA(q), q from ACF")
    print("    ACF decaying slowly                       -> difference first")

    # In the DIFFERENCED series lag 12 is a local maximum and lag 6 the
    # minimum -- the fingerprint of period-12 seasonality.
    assert ad[11] > ad[10] and ad[11] > ad[12], "lag 12 must be a local maximum"
    assert ad[5] == min(ad), "lag 6 must be the minimum"
    # In the RAW series it decays monotonically over the first 12 lags.
    assert all(a[i] > a[i + 1] for i in range(11)), "raw ACF must decay monotonically"
    assert abs(slope - 2.0) < 0.4, f"recovered slope {slope} should be near 2.0"
    print("\n  raw ACF decays monotonically (trend); differenced ACF peaks at")
    print("  lag 12 and troughs at lag 6 (seasonality); slope recovered ✓")
