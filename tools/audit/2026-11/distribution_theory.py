#!/usr/bin/env python3
"""Recompute the worked numbers of Distribution Theory (content check, November 2026).
The R output of set.seed() samples and of the precip data set (Practical 5) cannot be
reproduced without R; Practical 5 is checked for internal consistency only."""
import math
import numpy as np
from scipy import stats, special

ok = lambda a, b, tol=6e-7: abs(a - b) <= tol * max(1, abs(b))

# Unit 1
assert ok(math.exp(10), 22026.47, 1e-6) and ok(math.exp(10.125), 24959.26, 1e-6) and ok(math.exp(9.75), 17154.23, 1e-6)
v = (math.exp(.25) - 1) * math.exp(20.25); assert ok(v, 176937735.28, 1e-8) and ok(math.sqrt(v), 13301.79, 1e-6)
assert ok(stats.norm.sf((math.log(30000) - 10) / .5), 0.268319, 2e-5)
assert ok(math.exp(-.25), 0.778801) and ok(1e6 * (1 - math.pi / 4), 214601.84, 1e-7) and ok(1000 * math.sqrt(math.log(2)), 832.55, 1e-5)
assert ok(math.sqrt(2e9 - (5e4 / 1.5) ** 2), 29814.24, 1e-6) and ok(2e4 * 2 ** .4, 26390.16, 1e-6) and ok(.4 ** 2.5, 0.101193)
# Unit 2
q = 1 - math.exp(-2)
assert ok(2 / q, 2.3130353, 1e-7) and ok(6 / q - (2 / q) ** 2, 1.5889736, 1e-7)
f = lambda x: .6 * stats.norm.pdf(x) + .4 * stats.norm.pdf(x - 3)
assert ok(f(0), 0.241138) and ok(f(1.5), 0.129518) and ok(f(3), 0.162236)
mix = .6 * (stats.norm.cdf(1.7) - stats.norm.cdf(.7)) + .4 * (stats.norm.cdf(-1.3) - stats.norm.cdf(-2.3))
assert ok(mix, 0.153, 5e-4) and ok(2 * stats.norm.cdf(.5 / math.sqrt(3.16)) - 1, 0.221, 5e-4)
assert ok(10 * math.log(1 + 3 / 7), 3.5667494, 1e-7)
# Unit 3
assert ok(stats.chi2.sf(16.2, 9), 0.062821) and ok(2 * stats.t.sf(2, 15), 0.063945) and ok(stats.f.sf(24 / 7.2, 5, 10), 0.049697)
# Unit 4
assert ok(sum(k * (2 * k - 1) for k in range(1, 7)) / 36, 161 / 36) and ok(math.exp(-2 / 3), 0.5134, 1e-4)
# Practical 2-3
assert ok(stats.poisson.cdf(5, 1.5), 0.995544)
assert ok(math.sqrt(-2 * math.log(.274)), 1.609116) and ok(math.sqrt(-2 * math.log(.8821)), 0.500899)
u = np.array([.1273, .4820, .7391, .9052, .0361]); assert ok((-np.log(1 - u) / .5).mean(), 1.812126)
# Practical 4
O = np.array([2, 14, 20, 34, 22, 8.]); E = 100 * stats.binom.pmf(range(6), 5, .568)
c = ((O - E) ** 2 / E).sum(); assert ok(c, 4.007575) and ok(stats.chi2.sf(c, 4), 0.404982)
O2 = np.r_[O[0] + O[1], O[2:]]; E2 = np.r_[E[0] + E[1], E[2:]]
c = ((O2 - E2) ** 2 / E2).sum(); assert ok(c, 3.997889) and ok(stats.chi2.sf(c, 3), 0.261692)
O = np.array([60, 70, 40, 20, 8, 2.]); E = np.r_[200 * stats.poisson.pmf(range(5), 1.26), 200 * stats.poisson.sf(4, 1.26)]
c = ((O - E) ** 2 / E).sum(); assert ok(c, 1.551074) and ok(stats.chi2.sf(c, 4), 0.817558)
O2 = np.r_[O[:4], 10]; E2 = np.r_[E[:4], E[4] + E[5]]
c = ((O2 - E2) ** 2 / E2).sum(); assert ok(c, 1.438000) and ok(stats.chi2.sf(c, 3), 0.696652)
# Practical 5 (consistency of the table with the stated estimates)
P = np.diff(stats.norm.cdf([-np.inf, 20, 30, 40, 50, np.inf], 2442 / 70, math.sqrt(12963.19 / 70)))
O = np.array([13, 5, 25, 21, 6.]); c = ((O - 70 * P) ** 2 / (70 * P)).sum()
assert ok(c, 12.83977, 1e-4) and ok(stats.chi2.sf(c, 2), 0.001629, 1e-3)
# Practical 6
x = np.sort([-91.62, 5.09, -138.90, 5.19, 6.13, -17.55, 7.98, 0.17, 7.01, 5.38, 6.42, 5.59, 5.88,
             -18.36, 9.85, 3.35, 2.31, 2.87, 4.84, 8.66])
q1, med, q3 = np.quantile(x, [.25, .5, .75]); assert ok(q1, 1.775) and ok(med, 5.14) and ok(q3, 6.2025)
r = stats.kstest(x, stats.cauchy(med, (q3 - q1) / 2).cdf)
assert ok(r.statistic, 0.16904, 1e-4) and ok(r.pvalue, 0.5604, 1e-3)
# Practicals 7-10
t = np.array([31, 58, 87, 119, 153, 192, 238, 296, 378, 520.]); n = 10
xb = t.mean(); s2 = t.var(); k = xb ** 2 / s2; assert ok(k, 2.000984) and ok(xb / s2, 0.009657, 1e-6)
seq = []
for _ in range(4):
    k += n * (math.log(k) - math.log(xb) + np.log(t).mean() - special.digamma(k)) / (n * (special.polygamma(1, k) - 1 / k))
    seq.append(round(k, 6))
assert seq == [1.82424, 1.839272, 1.839405, 1.839405] and ok(k / xb, 0.008877, 1e-6)
mu = np.log(t).mean(); sg2 = np.log(t).var()
assert ok(mu, 5.037875) and ok(sg2, 0.686784) and ok(math.exp(mu), 154.142088) and ok(math.exp(mu + sg2 / 2), 217.297367)
assert ok(stats.norm.sf((math.log(200) - mu) / math.sqrt(sg2)), 0.376658)
F = (np.arange(1, 11) - .3) / 10.4; X = np.log(t); Y = np.log(-np.log(1 - F))
b, a = np.polyfit(X, Y, 1); lam = math.exp(-a / b)
assert ok(b, 1.275435) and ok(lam, 232.297728) and ok(np.corrcoef(X, Y)[0, 1], 0.999215)
assert ok(lam * math.gamma(1 + 1 / b), 215.397136) and ok(math.exp(-(200 / lam) ** b), 0.437716)
al = n / np.log(t / 31).sum(); assert ok(al, 0.623485) and ok((31 / 200) ** al, 0.312740) and ok(al * 31 / (al - 1), -51.33, 1e-4)
print("distribution-theory: all recomputed values agree")
