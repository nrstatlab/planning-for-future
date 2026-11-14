"""Content check, November 2026: Theoretical Discrete Distributions, Design and Analysis of
Experiments, Statistical Quality Control. Recomputes the practical pages and the unit examples
that need more than a line of arithmetic."""
import math
import numpy as np
from scipy import stats

def close(a, b, tol): assert abs(a - b) <= tol, (a, b)

# ---- Theoretical Discrete Distributions, practical ----
f = np.array([2, 6, 30, 52, 67, 56, 32, 10, 1]); p = (f * np.arange(9)).sum() / 256 / 8
close(p, 0.5078, 5e-5)
assert np.allclose(256 * stats.binom.pmf(np.arange(9), 8, p), [0.88, 7.28, 26.28, 54.23, 69.93, 57.72, 29.77, 8.78, 1.13], atol=0.011)
e = 100 * stats.poisson.pmf(range(5), 0.75); assert np.allclose(e, [47.24, 35.43, 13.29, 3.32, 0.62], atol=0.006)
E = [e[0], e[1], 100 - e[0] - e[1]]; close(sum((o - x) ** 2 / x for o, x in zip([46, 38, 16], E)), 0.32, 0.005)
fx = np.array([25, 38, 40, 31, 23, 16, 11, 7, 4, 3, 2]); x = np.arange(11)
assert (fx * x).sum() == 577 and (fx * x * x).sum() == 2683
assert np.allclose(200 * stats.nbinom.pmf(x, 4, 0.581), [22.79, 38.19, 40.01, 33.53, 24.59, 16.48, 10.36, 6.20, 3.57, 2.00, 1.09], atol=0.015)
pg = 1 / 2.35; assert np.allclose(100 * stats.geom.pmf(np.arange(1, 6), pg), [42.55, 24.45, 14.04, 8.07, 4.63], atol=0.006)
close(100 * (1 - pg) ** 5, 6.26, 0.006)
h = stats.hypergeom.pmf(range(6), 50, 10, 5); assert np.allclose(h, [0.3106, 0.4313, 0.2098, 0.0442, 0.0040, 0.0001], atol=6e-5)
E = list(500 * h[:3]) + [500 * h[3:].sum()]; close(sum((o - x) ** 2 / x for o, x in zip([155, 225, 95, 25], E)), 1.37, 0.005)
# Unit 3, numerical check of the Poisson limit
assert np.allclose(stats.nbinom.pmf(range(5), 200, 0.985), [0.049, 0.146, 0.220, 0.222, 0.169], atol=6e-4)

# ---- Design and Analysis of Experiments ----
T = np.array([[22, 26, 28, 24], [30, 36, 34, 32], [20, 24, 22, 26.]])          # practical, Experiment 3
cf = T.sum() ** 2 / 12; sst = (T ** 2).sum() - cf; ssr = (T.sum(1) ** 2).sum() / 4 - cf; ssc = (T.sum(0) ** 2).sum() / 3 - cf
close(ssr, 224, 1e-9); close(ssc, 38.67, 0.005); close((ssr / 2) / ((sst - ssr - ssc) / 6), 31.50, 0.005)
Y = np.array([[18, 24, 23, 22, 29], [21, 27, 25, 26, 31], [19, 22, 24, 20, 27], [20, 26, 28, 27, 34.]])  # Unit 1, Worked Problem 2
cf = Y.sum() ** 2 / 20; tss = (Y ** 2).sum() - cf; st = (Y.sum(0) ** 2).sum() / 4 - cf; sb = (Y.sum(1) ** 2).sum() / 5 - cf
close(st, 235.30, 1e-6); close(sb, 72.55, 1e-6); mse = (tss - st - sb) / 12
close(st / 4 / mse, 34.10, 0.005); close(stats.t.ppf(0.995, 12) * math.sqrt(2 * mse / 4), 2.84, 0.005)
g = [[74, 71, 69, 77, 72, 68, 75], [78, 75, 80, 73, 76, 79, 74], [70, 73, 68, 75, 71, 69, 72], [76, 72, 78, 74, 79, 73, 77]]
close(stats.f_oneway(*g).statistic, 5.97, 0.01)                                # Unit 1, exercise 1
close(stats.f.ppf(0.99, 4, 12), 5.41, 0.005); close(stats.f.ppf(0.99, 3, 12), 5.95, 0.005)
close((4 * 12 + 5 * 3 * 4) / 19, 5.68, 0.005); close((6.667 + 10 + 9) / 5, 5.133, 0.001)   # Unit 5 efficiencies

# ---- Statistical Quality Control ----
X = np.array([[12,14,11,13,10],[13,16,12,11,15],[10,12,13,11,9],[14,13,17,12,16],[11,10,14,12,8],
              [15,13,12,14,16],[12,15,11,13,17],[10,9,12,11,13],[13,14,12,15,11],[12,13,11,14,10]])
xb = X.mean(1).mean(); R = (X.max(1) - X.min(1)).mean(); S = X.std(1, ddof=1).mean()
close(xb, 12.54, 1e-9); close(R, 4.6, 1e-9); close(S, 1.828, 0.0005)
close(xb + 0.577 * R, 15.19, 0.005); close(xb + 1.427 * S, 15.15, 0.005); close(2.089 * S, 3.82, 0.005)
pb = 22 / 520; assert np.allclose([pb + 3 * math.sqrt(pb * (1 - pb) / n) for n in (100, 120, 90, 110)], [0.1027, 0.0974, 0.1060, 0.0999], atol=6e-5)
u = 37 / 8; assert np.allclose([u + 3 * math.sqrt(u / n) for n in (1, 1.5, 2, 2.5)], [11.08, 9.89, 9.19, 8.71], atol=0.006)
for pp, pa, aoq, ati in ((.01, .9098, .00864, 135.7), (.03, .5578, .01590, 470.1), (.08, .0916, .00696, 913.0)):
    a = stats.poisson.cdf(1, 50 * pp); close(a, pa, 5e-5); close(a * pp * 0.95, aoq, 6e-6); close(50 + (1 - a) * 950, ati, 0.06)
ps = np.linspace(.001, .1, 4000)
close((stats.poisson.cdf(1, 50 * ps) * ps * .95).max(), 0.0160, 5e-5); close((stats.poisson.cdf(2, 100 * ps) * ps * .9).max(), 0.0123, 5e-5)
close(stats.binom.cdf(2, 50, .02), 0.9216, 5e-5); close(stats.binom.cdf(2, 50, .08), 0.226, 5e-4); close(stats.binom.cdf(3, 200, .03), 0.147, 5e-4)
assert np.allclose(stats.poisson.cdf(3, [1, 2, 3, 4, 5, 6]), [.981, .857, .647, .433, .265, .151], atol=6e-4)
assert np.allclose(stats.binom.cdf(1, 20, [.01, .03, .05, .10, .15, .20]), [.983, .880, .736, .392, .176, .069], atol=6e-4)
close(stats.poisson.pmf(2, 2.5) + stats.poisson.pmf(3, 2.5), 0.470, 5e-4)       # double sampling
print("discrete_doe_sqc: all checks pass")
