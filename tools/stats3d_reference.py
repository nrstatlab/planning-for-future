#!/usr/bin/env python3
"""Reference values for the 3D Statistics calculator, computed independently.

    python3 tools/stats3d_reference.py      # writes tools/stats3d_reference.json

Needs numpy, scipy and statsmodels (a scratch virtual environment is enough;
nothing on the site needs them). tools/check_stats3d.js runs the page's own
library, assets/stats3d-lib.js, on the same data and compares every number.

Where scipy has the test, scipy computes it (ttest_ind, mannwhitneyu,
wilcoxon, kruskal, bartlett, f_oneway, kstest, the distribution fits with
fixed location). Where it has not (z tests, the chi-square variance test,
Fisher's z, the runs test, the textbook Spearman tie correction) the value is
computed here from the textbook formula with scipy's distributions, and the
maximum-likelihood estimates scipy finds only by a coarse optimiser are found
here by solving the likelihood equations with scipy.optimize.
"""
import json
import math
import pathlib

import numpy as np
import statsmodels.api as sm
from scipy import optimize, special, stats

OUT = pathlib.Path(__file__).with_name("stats3d_reference.json")
rng = np.random.default_rng(20261108)


def r6(a):
    return [float(v) for v in a]


# ---------------------------------------------------------------- data sets
DATA = {}
DATA["course"] = {"y": [12, 18, 20, 28, 32], "x1": [2, 4, 6, 8, 10], "x2": [1, 3, 2, 5, 4]}
a = rng.normal(50, 10, 100)
b = 0.6 * a + rng.normal(0, 8, 100)
c = 0.3 * a - 0.4 * b + rng.normal(0, 6, 100)
DATA["big"] = {"y": r6(np.round(a, 2)), "x1": r6(np.round(b, 2)), "x2": r6(np.round(c, 2))}
DATA["counts"] = {"y": r6(rng.poisson(3.2, 40)), "x1": r6(rng.poisson(4.0, 35)), "x2": r6(rng.poisson(3.6, 30))}
DATA["small"] = {"y": [-3.2, 1.4, 0.7, -0.6, 2.9, 4.1, -1.8, 3.3, 0.2, 5.6, -2.4, 1.9, 6.2, 2.5, 3.8],
                 "x1": [1.1, -0.4, 2.2, 0.9, 3.5, -1.3, 0.4, 2.8, 1.7, -2.1, 4.4, 0.6]}
DATA["two"] = {"y": [3, 5], "x1": [4, 9]}
DATA["skewed"] = {"y": r6(np.round(rng.gamma(2.5, 1.6, 60), 3)),
                  "x1": r6(np.round(rng.beta(2.2, 3.5, 30), 4)),
                  "x2": r6(np.round(rng.weibull(1.7, 60) * 3.0, 3))}
DATA["nb"] = {"y": r6(rng.negative_binomial(3, 0.4, 50))}
DATA["binom"] = {"y": r6(rng.binomial(8, 0.35, 45))}
# Five variables of unequal sizes (the calculator takes up to 5 x 50), and the
# three machines of Design & Analysis of Experiments, Unit 1, Worked Problem 1.
DATA["five"] = {"g%d" % (i + 1): r6(np.round(rng.normal(20 + 1.5 * i, 3 + 0.4 * i, n), 1))
                for i, n in enumerate([12, 15, 10, 8, 20])}
DATA["machines"] = {"A": [22, 25, 24, 21, 26, 23, 24], "B": [20, 23, 22, 21, 24], "C": [25, 23, 27, 26, 24, 25]}

cases = []


def add(fn, args, expect, tol=None):
    cases.append({"fn": fn, "args": args, "expect": expect, **({"tol": tol} if tol else {})})


def D(name, var):
    return {"data": name, "var": var}


# ---------------------------------------------------------------- functions
for p in [0.001, 0.025, 0.3, 0.5, 0.8, 0.975, 0.9999]:
    add("normInv", [p], {"": float(stats.norm.ppf(p))})
    for df in [1, 3, 12, 57.5]:
        add("tInv", [p, df], {"": float(stats.t.ppf(p, df))})
        add("chi2Inv", [p, df], {"": float(stats.chi2.ppf(p, df))})
        add("fInv", [p, df, 7], {"": float(stats.f.ppf(p, df, 7))})
for z in [-6.5, -2.1, -0.3, 0, 1.2, 3.7, 8.2]:
    add("normCdf", [z], {"": float(stats.norm.cdf(z))})
    add("tCdf", [z, 4.5], {"": float(stats.t.cdf(z, 4.5))})
for v in [0.2, 1.5, 7.3, 30.0]:
    add("chi2Sf", [v, 6], {"": float(stats.chi2.sf(v, 6))})
    add("fSf", [v, 3, 20], {"": float(stats.f.sf(v, 3, 20))})
for x in [0.5, 1.3, 4.0, 11.7]:
    add("digamma", [x], {"": float(special.digamma(x))})
    add("trigamma", [x], {"": float(special.polygamma(1, x))})
for n, d in [(5, 0.3), (20, 0.12), (40, 0.25), (100, 0.07), (100, 0.2), (60, 0.4)]:
    add("kolmogorovCdf", [n, d], {"": float(stats.kstwo.cdf(d, n))})


def pos(s, p):
    n = len(s)
    if p <= 1:
        return s[0]
    if p >= n:
        return s[-1]
    lo = int(math.floor(p))
    return s[lo - 1] + (p - lo) * (s[lo] - s[lo - 1])


# ---------------------------------------------------------------- describe
for name, dset in DATA.items():
    for var, x in dset.items():
        x = np.array(x, float)
        n = len(x)
        s = sorted(x)
        m = x.mean()
        e = {"n": n, "mean": m, "median": float(np.median(x)), "min": s[0], "max": s[-1],
             "q1": pos(s, (n + 1) / 4), "q3": pos(s, 3 * (n + 1) / 4),
             "varN": float(np.var(x)), "sdN": float(np.std(x)),
             "mu3": float(np.mean((x - m) ** 3)), "mu4": float(np.mean((x - m) ** 4)),
             "mdMean": float(np.mean(abs(x - m))), "mdMedian": float(np.mean(abs(x - np.median(x))))}
        if n > 1:
            e.update(var=float(np.var(x, ddof=1)), sd=float(np.std(x, ddof=1)), se=float(stats.sem(x)))
        if np.var(x) > 0:
            e.update(gamma1=float(stats.skew(x)), gamma2=float(stats.kurtosis(x)),
                     beta2=float(stats.kurtosis(x, fisher=True) + 3),
                     skPearson=float(3 * (m - np.median(x)) / np.std(x)))
            if m != 0:
                e["cv"] = float(100 * np.std(x) / m)
        if min(x) > 0:
            e.update(gm=float(stats.gmean(x)), hm=float(stats.hmean(x)))
        add("describe", [D(name, var)], e)

# ---------------------------------------------------------------- two and three variables
PAIRS = [("course", "y", "x1"), ("course", "x1", "x2"), ("big", "y", "x1"), ("big", "x1", "x2"),
         ("small", "y", "x1"), ("two", "y", "x1")]


def textbook_spearman(x, y):
    rx, ry = stats.rankdata(x), stats.rankdata(y)
    cf = 0
    for arr in (x, y):
        _, counts = np.unique(arr, return_counts=True)
        cf += sum((m ** 3 - m) / 12 for m in counts if m > 1)
    n = len(x)
    return 1 - 6 * (np.sum((rx - ry) ** 2) + cf) / (n * (n * n - 1))


for name, vy, vx in PAIRS:
    x = np.array(DATA[name][vy], float)
    y = np.array(DATA[name][vx], float)
    m = min(len(x), len(y))
    x, y = x[:m], y[:m]
    lr = stats.linregress(x, y)
    e = {"r": float(stats.pearsonr(x, y)[0]) if m > 2 else float(np.corrcoef(x, y)[0, 1]),
         "byx": float(lr.slope), "ayx": float(lr.intercept),
         "bxy": float(stats.linregress(y, x).slope), "cov": float(np.cov(x, y)[0, 1]),
         "covN": float(np.cov(x, y, ddof=0)[0, 1]),
         "spearman": float(textbook_spearman(x, y))}
    if m > 2:
        e["spearmanRanksR"] = float(stats.spearmanr(x, y)[0])
    add("bivariate", [{"data": name, "var": vy, "len": m}, {"data": name, "var": vx, "len": m}], e)

for name in ["course", "big"]:
    y, x1, x2 = (np.array(DATA[name][v], float) for v in ("y", "x1", "x2"))

    def resid(a, b):
        X = sm.add_constant(b)
        return sm.OLS(a, X).fit().resid

    e = {"r12_3": float(np.corrcoef(resid(y, x2), resid(x1, x2))[0, 1]),
         "r13_2": float(np.corrcoef(resid(y, x1), resid(x2, x1))[0, 1]),
         "r23_1": float(np.corrcoef(resid(x1, y), resid(x2, y))[0, 1]),
         "R1_23": float(math.sqrt(sm.OLS(y, sm.add_constant(np.column_stack([x1, x2]))).fit().rsquared)),
         "R2_13": float(math.sqrt(sm.OLS(x1, sm.add_constant(np.column_stack([y, x2]))).fit().rsquared))}
    args = [D(name, "y"), D(name, "x1"), D(name, "x2")]
    add("trivariate", args, e)
    fit = sm.OLS(y, sm.add_constant(np.column_stack([x1, x2]))).fit()
    ci = fit.conf_int(0.05)
    add("regress2", args + [0.05], {
        "b.0": fit.params[0], "b.1": fit.params[1], "b.2": fit.params[2],
        "se.0": fit.bse[0], "se.1": fit.bse[1], "se.2": fit.bse[2],
        "t.1": fit.tvalues[1], "p.1": fit.pvalues[1], "p.2": fit.pvalues[2],
        "ci.1.0": ci[1][0], "ci.1.1": ci[1][1], "r2": fit.rsquared, "adjR2": fit.rsquared_adj,
        "F": fit.fvalue, "pF": fit.f_pvalue})
    fit1 = sm.OLS(y, sm.add_constant(x1)).fit()
    ci1 = fit1.conf_int(0.05)
    add("regress1", [D(name, "y"), D(name, "x1"), 0.05], {
        "a": fit1.params[0], "b": fit1.params[1], "seA": fit1.bse[0], "seB": fit1.bse[1],
        "tB": fit1.tvalues[1], "pB": fit1.pvalues[1], "pA": fit1.pvalues[0],
        "ciB.0": ci1[1][0], "ciB.1": ci1[1][1], "F": fit1.fvalue, "pF": fit1.f_pvalue})
    for alt, sp in (("two", "two-sided"), ("less", "less"), ("greater", "greater")):
        r12_3 = e["r12_3"]
        df = len(y) - 3
        t = r12_3 * math.sqrt(df) / math.sqrt(1 - r12_3 ** 2)
        pv = {"two": 2 * stats.t.sf(abs(t), df), "less": stats.t.cdf(t, df), "greater": stats.t.sf(t, df)}[alt]
        add("partialTest", args + [0.05, alt], {"stat": t, "p": pv})
    R2 = e["R1_23"] ** 2
    F = (R2 / 2) / ((1 - R2) / (len(y) - 3))
    add("multipleTest", args + [0.05], {"stat": F, "p": stats.f.sf(F, 2, len(y) - 3)})

# ---------------------------------------------------------------- tests of means and variances
ALTS = (("two", "two-sided"), ("less", "less"), ("greater", "greater"))


def pz(z, alt):
    return {"two": 2 * stats.norm.sf(abs(z)), "less": stats.norm.cdf(z), "greater": stats.norm.sf(z)}[alt]


for name, v1, v2 in [("big", "y", "x1"), ("small", "y", "x1"), ("counts", "y", "x1"), ("two", "y", "x1")]:
    x = np.array(DATA[name][v1], float)
    y = np.array(DATA[name][v2], float)
    for alt, sp in ALTS:
        mu0 = float(np.mean(x) * 0.9 + 0.3)
        r = stats.ttest_1samp(x, mu0, alternative=sp)
        tc = stats.t.ppf(0.975, len(x) - 1)
        se = stats.sem(x)
        add("t1", [D(name, v1), mu0, 0.05, alt], {"stat": r.statistic, "p": r.pvalue,
            "ci.0": np.mean(x) - tc * se, "ci.1": np.mean(x) + tc * se})
        z = (np.mean(x) - mu0) / (7.5 / math.sqrt(len(x)))
        add("z1", [D(name, v1), mu0, 7.5, 0.05, alt], {"stat": z, "p": pz(z, alt)})
        s0 = float(np.var(x, ddof=1) * 1.3)
        chi = (len(x) - 1) * np.var(x, ddof=1) / s0
        k = len(x) - 1
        pc = {"two": 2 * min(stats.chi2.cdf(chi, k), stats.chi2.sf(chi, k)),
              "less": stats.chi2.cdf(chi, k), "greater": stats.chi2.sf(chi, k)}[alt]
        add("chiVar", [D(name, v1), s0, 0.05, alt], {"stat": chi, "p": min(1, pc),
            "ci.0": k * np.var(x, ddof=1) / stats.chi2.ppf(0.975, k),
            "ci.1": k * np.var(x, ddof=1) / stats.chi2.ppf(0.025, k)})
        r = stats.ttest_ind(x, y, equal_var=True, alternative=sp)
        add("t2pooled", [D(name, v1), D(name, v2), 0, 0.05, alt], {"stat": r.statistic, "p": r.pvalue})
        if len(x) > 2 or len(y) > 2:
            r = stats.ttest_ind(x, y, equal_var=False, alternative=sp)
            v1n, v2n = np.var(x, ddof=1) / len(x), np.var(y, ddof=1) / len(y)
            dfw = (v1n + v2n) ** 2 / (v1n ** 2 / (len(x) - 1) + v2n ** 2 / (len(y) - 1))
            add("t2welch", [D(name, v1), D(name, v2), 0, 0.05, alt], {"stat": r.statistic, "p": r.pvalue, "df": dfw})
        z2 = (np.mean(x) - np.mean(y) - 0.5) / math.sqrt(4.0 / len(x) + 9.0 / len(y))
        add("z2", [D(name, v1), D(name, v2), 2.0, 3.0, 0.5, 0.05, alt], {"stat": z2, "p": pz(z2, alt)})
        F = np.var(x, ddof=1) / np.var(y, ddof=1)
        d1, d2 = len(x) - 1, len(y) - 1
        pf = {"two": 2 * min(stats.f.cdf(F, d1, d2), stats.f.sf(F, d1, d2)),
              "less": stats.f.cdf(F, d1, d2), "greater": stats.f.sf(F, d1, d2)}[alt]
        add("fVar", [D(name, v1), D(name, v2), 0.05, alt], {"stat": F, "p": min(1, pf),
            "ci.0": F / stats.f.ppf(0.975, d1, d2), "ci.1": F / stats.f.ppf(0.025, d1, d2)})
        m = min(len(x), len(y))
        if m > 1:
            r = stats.ttest_rel(x[:m], y[:m], alternative=sp)
            add("tpaired", [{"data": name, "var": v1, "len": m}, {"data": name, "var": v2, "len": m}, 0, 0.05, alt],
                {"stat": r.statistic, "p": r.pvalue})

# correlation tests
for name, v1, v2 in [("big", "y", "x1"), ("small", "y", "x1"), ("course", "y", "x2")]:
    m = min(len(DATA[name][v1]), len(DATA[name][v2]))
    x = np.array(DATA[name][v1][:m], float)
    y = np.array(DATA[name][v2][:m], float)
    args = [{"data": name, "var": v1, "len": m}, {"data": name, "var": v2, "len": m}]
    for alt, sp in ALTS:
        r = stats.pearsonr(x, y, alternative=sp)
        df = m - 2
        t = r[0] * math.sqrt(df) / math.sqrt(1 - r[0] ** 2)
        add("rZero", args + [0.05, alt], {"stat": t, "p": r[1]})
        if m > 3:
            z = (math.atanh(r[0]) - math.atanh(0.3)) * math.sqrt(m - 3)
            zc = stats.norm.ppf(0.975)
            add("rFisher", args + [0.3, 0.05, alt], {"stat": z, "p": pz(z, alt),
                "ci.0": math.tanh(math.atanh(r[0]) - zc / math.sqrt(m - 3)),
                "ci.1": math.tanh(math.atanh(r[0]) + zc / math.sqrt(m - 3))})

# ANOVA, Bartlett, Kruskal-Wallis
for name, vs in [("counts", ["y", "x1", "x2"]), ("big", ["y", "x1", "x2"]), ("small", ["y", "x1"]),
                 ("five", ["g1", "g2", "g3", "g4", "g5"]), ("five", ["g2", "g4", "g5"]), ("machines", ["A", "B", "C"])]:
    groups = [np.array(DATA[name][v], float) for v in vs]
    args = [[D(name, v) for v in vs], 0.05]
    r = stats.f_oneway(*groups)
    add("anova1", args, {"stat": r.statistic, "p": r.pvalue})
    r = stats.bartlett(*groups)
    add("bartlett", args, {"stat": r.statistic, "p": r.pvalue})
    r = stats.kruskal(*groups)
    add("kruskal", args, {"stat": r.statistic, "p": r.pvalue})

# ---------------------------------------------------------------- non-parametric
for name, v, m0 in [("small", "y", 0.5), ("big", "y", 48.0), ("counts", "y", 3.0), ("small", "x1", 0.0)]:
    x = np.array(DATA[name][v], float)
    plus, minus = int(np.sum(x > m0)), int(np.sum(x < m0))
    n = plus + minus
    lower, upper = stats.binom.cdf(plus, n, 0.5), stats.binom.sf(plus - 1, n, 0.5)
    for alt, sp in ALTS:
        pv = {"two": min(1, 2 * min(lower, upper)), "less": lower, "greater": upper}[alt]
        add("signTest", [D(name, v), m0, 0.05, alt], {"stat": plus, "p": pv})
        d = x - m0
        d = d[d != 0]
        ties = len(np.unique(np.abs(d))) < len(d)
        method = "exact" if (not ties and len(d) <= 50) else "approx"
        r = stats.wilcoxon(d, alternative=sp, method=method, correction=True, zero_method="wilcox")
        rk = stats.rankdata(np.abs(d))
        add("wilcoxon", [D(name, v), m0, 0.05, alt], {"stat": float(np.sum(rk[d > 0])), "p": r.pvalue})

for name, v1, v2 in [("small", "y", "x1"), ("big", "y", "x1"), ("counts", "y", "x2"), ("course", "y", "x1")]:
    x = np.array(DATA[name][v1], float)
    y = np.array(DATA[name][v2], float)
    ties = len(np.unique(np.concatenate([x, y]))) < len(x) + len(y)
    method = "exact" if (not ties and len(x) <= 20 and len(y) <= 20) else "asymptotic"
    for alt, sp in ALTS:
        r = stats.mannwhitneyu(x, y, alternative=sp, method=method, use_continuity=True)
        add("mannWhitney", [D(name, v1), D(name, v2), 0.05, alt], {"stat": r.statistic, "p": r.pvalue})


def runs_ref(x, alt):
    med = float(np.median(x))
    seq = [1 if v > med else 0 for v in x if v != med]
    n1, n2 = sum(seq), len(seq) - sum(seq)
    R = 1 + sum(1 for i in range(1, len(seq)) if seq[i] != seq[i - 1])
    if n1 <= 20 and n2 <= 20:
        tot = math.comb(n1 + n2, n1)

        def pr(r):
            if r % 2 == 0:
                k = r // 2
                return 2 * math.comb(n1 - 1, k - 1) * math.comb(n2 - 1, k - 1) / tot
            k = (r - 1) // 2
            return (math.comb(n1 - 1, k - 1) * math.comb(n2 - 1, k) + math.comb(n1 - 1, k) * math.comb(n2 - 1, k - 1)) / tot
        lower = sum(pr(r) for r in range(2, R + 1))
        upper = sum(pr(r) for r in range(R, n1 + n2 + 1))
        return R, {"two": min(1, 2 * min(lower, upper)), "less": lower, "greater": upper}[alt]
    N = n1 + n2
    mu = 2 * n1 * n2 / N + 1
    var = 2 * n1 * n2 * (2 * n1 * n2 - N) / (N * N * (N - 1))
    diff = R - mu
    cc = {"two": 0.5 * np.sign(diff), "greater": 0.5, "less": -0.5}[alt]
    z = (diff - cc) / math.sqrt(var)
    return R, pz(z, alt)


for name, v in [("small", "y"), ("big", "y"), ("big", "x2"), ("counts", "y")]:
    x = np.array(DATA[name][v], float)
    for alt, _ in ALTS:
        R, pv = runs_ref(x, alt)
        add("runsTest", [D(name, v), 0.05, alt], {"stat": R, "p": pv})

# ---------------------------------------------------------------- distribution fitting
FITS = {}


def mle(key, x, opts):
    x = np.asarray(x, float)
    n = len(x)
    if key == "normal":
        return [x.mean(), x.std()]
    if key == "lognormal":
        s, _, sc = stats.lognorm.fit(x, floc=0)
        return [math.log(sc), s]
    if key == "exponential":
        return [1 / stats.expon.fit(x, floc=0)[1]]
    if key == "laplace":
        loc, sc = stats.laplace.fit(x)
        return [loc, sc]
    if key == "gamma":
        a, _, sc = stats.gamma.fit(x, floc=0)
        return [a, 1 / sc]
    if key in ("beta1", "beta2"):
        y = x if key == "beta1" else x / (1 + x)
        l1, l2 = np.mean(np.log(y)), np.mean(np.log1p(-y))
        f = lambda p: [special.digamma(p[0]) - special.digamma(p[0] + p[1]) - l1,
                       special.digamma(p[1]) - special.digamma(p[0] + p[1]) - l2]
        return list(optimize.root(f, [1.0, 1.0], tol=1e-14).x)
    if key == "cauchy":
        nll = lambda p: -np.sum(stats.cauchy.logpdf(x, p[0], abs(p[1])))
        q1, q3 = np.percentile(x, [25, 75])
        res = optimize.minimize(nll, [np.median(x), (q3 - q1) / 2], method="Nelder-Mead",
                                options={"xatol": 1e-12, "fatol": 1e-14, "maxiter": 20000})
        return [res.x[0], abs(res.x[1])]
    if key == "weibull":
        lx = np.log(x)
        g = lambda k: np.sum(x ** k * lx) / np.sum(x ** k) - 1 / k - lx.mean()
        k = optimize.brentq(g, 1e-3, 100, xtol=1e-15)
        return [k, np.mean(x ** k) ** (1 / k)]
    if key == "logistic":
        def score(p):
            z = (x - p[0]) / p[1]
            t = np.tanh(z / 2)
            return [np.sum(t) / p[1], np.sum(z * t - 1) / p[1]]
        return list(optimize.root(score, [x.mean(), math.sqrt(3) * x.std() / math.pi], tol=1e-14).x)
    if key == "pareto":
        b, _, sc = stats.pareto.fit(x, floc=0)
        return [b, sc]
    if key == "uniform":
        return [x.min(), x.max()]
    if key == "poisson":
        return [x.mean()]
    if key == "geometric":
        return [1 / (1 + x.mean())]
    if key == "binomial":
        nn = opts.get("binomN") or x.max()
        return [x.mean() / nn, nn]
    if key == "negbinomial":
        m = x.mean()
        sc = lambda r: np.sum(special.digamma(x + r)) - n * special.digamma(r) + n * math.log(r / (r + m))
        r = optimize.brentq(sc, 1e-6, 1e6, xtol=1e-14)
        return [r, r / (r + m)]
    raise KeyError(key)


def scipy_dist(key, p):
    return {"normal": lambda: stats.norm(p[0], p[1]),
            "lognormal": lambda: stats.lognorm(p[1], scale=math.exp(p[0])),
            "exponential": lambda: stats.expon(scale=1 / p[0]),
            "laplace": lambda: stats.laplace(p[0], p[1]),
            "gamma": lambda: stats.gamma(p[0], scale=1 / p[1]),
            "beta1": lambda: stats.beta(p[0], p[1]),
            "beta2": lambda: stats.betaprime(p[0], p[1]),
            "cauchy": lambda: stats.cauchy(p[0], p[1]),
            "weibull": lambda: stats.weibull_min(p[0], scale=p[1]),
            "logistic": lambda: stats.logistic(p[0], p[1]),
            "pareto": lambda: stats.pareto(p[0], scale=p[1]),
            "uniform": lambda: stats.uniform(p[0], p[1] - p[0]),
            "poisson": lambda: stats.poisson(p[0]),
            "geometric": lambda: stats.geom(p[0], loc=-1),
            "binomial": lambda: stats.binom(int(p[1]), p[0]),
            "negbinomial": lambda: stats.nbinom(p[0], p[1])}[key]()


def nice_step(w):
    if not w > 0:
        return 1
    e = 10 ** math.floor(math.log10(w))
    f = w / e
    return (1 if f <= 1 else 2 if f <= 2 else 2.5 if f <= 2.5 else 5 if f <= 5 else 10) * e


def cells(key, x, p):
    dist = scipy_dist(key, p)
    n = len(x)
    out = []
    if key in ("poisson", "geometric", "binomial", "negbinomial"):
        lo, hi = int(min(x)), int(max(x))
        for v in range(lo, hi + 1):
            if lo == hi:
                P = 1
            elif v == lo:
                P = dist.cdf(v)
            elif v == hi:
                P = dist.sf(v - 1)
            else:
                P = dist.pmf(v)
            out.append([int(np.sum(x == v)), n * P])
    else:
        s = sorted(x)
        k = math.ceil(1 + 3.322 * math.log10(n))
        h = nice_step((s[-1] - s[0]) / k or 1)
        start = math.floor(s[0] / h) * h
        bounds = []
        while True:
            L = start + len(bounds) * h
            if L > s[-1] + 1e-12 * max(1, abs(s[-1])):
                break
            bounds.append(L)
        f = [0] * len(bounds)
        for v in s:
            f[min(len(bounds) - 1, int(math.floor((v - start) / h + 1e-12)))] += 1
        for i, L in enumerate(bounds):
            a = -np.inf if i == 0 else L
            b = np.inf if i == len(bounds) - 1 else L + h
            out.append([f[i], n * ((1 if b == np.inf else dist.cdf(b)) - (0 if a == -np.inf else dist.cdf(a)))])
    while len(out) > 1 and out[0][1] < 5:
        out[0:2] = [[out[0][0] + out[1][0], out[0][1] + out[1][1]]]
    while len(out) > 1 and out[-1][1] < 5:
        out[-2:] = [[out[-2][0] + out[-1][0], out[-2][1] + out[-1][1]]]
    i = 1
    while i < len(out) - 1:
        if out[i][1] < 5:
            out[i:i + 2] = [[out[i][0] + out[i + 1][0], out[i][1] + out[i + 1][1]]]
        else:
            i += 1
    if len(out) > 1 and out[-1][1] < 5:
        out[-2:] = [[out[-2][0] + out[-1][0], out[-2][1] + out[-1][1]]]
    return out


NPARAM = {"binomial": 1}
for name, var, keys, opts in [
        ("skewed", "y", ["normal", "lognormal", "exponential", "laplace", "gamma", "beta2", "cauchy",
                         "weibull", "logistic", "pareto", "uniform"], {}),
        ("skewed", "x1", ["beta1", "normal", "gamma", "weibull", "logistic"], {}),
        ("skewed", "x2", ["weibull", "gamma", "lognormal", "normal", "cauchy"], {}),
        ("big", "y", ["normal", "logistic", "cauchy", "laplace", "uniform"], {}),
        ("counts", "y", ["poisson", "geometric", "normal"], {}),
        ("nb", "y", ["negbinomial", "poisson", "geometric"], {}),
        ("binom", "y", ["binomial", "poisson"], {"binomN": 8})]:
    x = np.array(DATA[name][var], float)
    for key in keys:
        p = mle(key, x, opts)
        dist = scipy_dist(key, p)
        disc = key in ("poisson", "geometric", "binomial", "negbinomial")
        ll = float(np.sum(dist.logpmf(x) if disc else dist.logpdf(x)))
        k = NPARAM.get(key, 1 if key in ("exponential", "poisson", "geometric") else 2)
        cs = cells(key, x, p)
        chi = sum((o - e) ** 2 / e for o, e in cs)
        df = len(cs) - 1 - k
        e = {"mle.0": p[0], "logL": ll, "aic": 2 * k - 2 * ll, "chi.stat": chi, "chi.df": df}
        if key not in ("binomial",) and len(p) > 1:
            e["mle.1"] = p[1]
        if df >= 1:
            e["chi.p"] = float(stats.chi2.sf(chi, df))
        if not disc:
            ks = stats.kstest(x, dist.cdf)
            e["ks.D"] = float(ks.statistic)
            e["ks.p"] = float(stats.kstwo.sf(ks.statistic, len(x)))
        add("fit", [key, D(name, var), dict(opts, alpha=0.05)], e,
            tol=1e-6 if key in ("cauchy",) else None)

# A distribution the visitor specifies: nothing estimated, df not reduced.
x = np.array(DATA["counts"]["y"], float)
cs = cells("poisson", x, [3.0])
chi = sum((o - e) ** 2 / e for o, e in cs)
add("fit", ["poisson", D("counts", "y"), {"alpha": 0.05, "params": [3.0]}],
    {"chi.stat": chi, "chi.df": len(cs) - 1, "chi.p": float(stats.chi2.sf(chi, len(cs) - 1))})
x = np.array(DATA["big"]["y"], float)
ks = stats.kstest(x, stats.norm(50, 10).cdf)
add("fit", ["normal", D("big", "y"), {"alpha": 0.05, "params": [50, 10]}],
    {"ks.D": float(ks.statistic), "ks.p": float(stats.kstwo.sf(ks.statistic, len(x)))})


def clean(o):
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    return o


OUT.write_text(json.dumps(clean({"data": DATA, "cases": cases}), indent=0) + "\n")
print("%d reference values in %d cases written to %s" % (
    sum(len(c["expect"]) for c in cases), len(cases), OUT.name))
