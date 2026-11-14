#!/usr/bin/env python3
"""Recompute the worked numbers of Econometrics (content check, November 2026)."""
import math
import numpy as np
from scipy import stats

ok = lambda a, b, tol=6e-4: abs(a - b) <= tol * max(1, abs(b))
x = np.array([10, 20, 30, 40, 50.]); y = np.array([11, 20, 27, 34, 43.])
Sxx = ((x - 30) ** 2).sum(); Sxy = ((x - 30) * (y - 27)).sum(); b1 = Sxy / Sxx; b0 = 27 - 30 * b1
res = y - b0 - b1 * x; rss = (res ** 2).sum(); tss = ((y - 27) ** 2).sum()
assert (Sxx, Sxy) == (1000, 780) and ok(b0, 3.6) and ok(rss, 1.6) and tss == 610
se = math.sqrt(rss / 3 / Sxx); t = stats.t.ppf(.975, 3)
assert ok(se, 0.0231, 1e-3) and ok(b1 / se, 33.8, 1e-3) and ok((tss - rss) / (rss / 3), 1140.75)
assert ok(b1 - t * se, 0.7065) and ok(b1 + t * se, 0.8535) and ok(stats.f.sf(1140.75, 1, 3), 5.706e-5, 1e-3)
r1, r2, r12 = .8, .6, .5
assert ok((r1 - r2 * r12) / math.sqrt((1 - r2 ** 2) * (1 - r12 ** 2)), 0.7217)
assert ok((r1 ** 2 + r2 ** 2 - 2 * r1 * r2 * r12) / (1 - r12 ** 2), 0.6933)
X = np.array([[1, 1], [1, 2], [1, 3.]]); assert np.allclose(np.linalg.solve(X.T @ X, X.T @ [2, 4, 5]), [2 / 3, 1.5])
X = np.array([[1, 1, 2], [1, 2, 1], [1, 3, 2.]]); assert np.allclose(np.linalg.solve(X.T @ X, X.T @ [4, 5, 7]), [1.5, 1.5, .5])
assert ok((.62 / 2) / (.38 / 97), 79.1, 1e-3) and ok(stats.chi2.ppf(.95, 5), 11.07) and ok(stats.chi2.sf(10.8, 5), 0.055, 1e-2)
assert ok(.30 / math.sqrt(12.5), 0.085, 1e-2) and ok(1 - .85 / 2, 0.575) and ok(1 - (5.5 / 7) / 2, 0.607, 1e-3)
print("econometrics: all recomputed values agree")
