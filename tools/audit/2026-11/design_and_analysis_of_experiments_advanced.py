#!/usr/bin/env python3
"""Recompute the worked numbers of Design and Analysis of Experiments (Advanced)."""
import numpy as np
from scipy import stats
from scipy.stats import studentized_range as sr

ok = lambda a, b, tol=6e-7: abs(a - b) <= tol * max(1, abs(b))
pf = lambda F, a, b: stats.f.sf(F, a, b)

# Unit 1
assert ok(pf(16.75, 2, 12), 0.000337, 1e-6) and ok(pf(42.25, 1, 12), 0.000029, 1e-6) and ok(pf(.25, 2, 12), 0.782758)
assert ok(pf(27.5, 1, 11), 0.000275, 1e-6) and ok(pf(48.491667, 1, 11), 0.000024, 1e-6) and ok(pf(.55, 1, 11), 0.473855)
assert ok(pf(26.557143, 1, 11), 0.000317, 1e-6)
# Example 1.3 by least squares
y = np.array([5, 7, 6, 6, 9, 11, 8, 10, 9, 13, 15, 14, 12, 16, 14.])
A = np.array([1] * 6 + [0] * 9); B = np.array([1] * 4 + [0] * 2 + [1] * 3 + [0] * 6)
def R(*cols):
    X = np.column_stack([np.ones(15), *cols]); b = np.linalg.lstsq(X, y, rcond=None)[0]
    return ((X @ b) ** 2).sum() - y.sum() ** 2 / 15
assert ok(R(A), 90) and ok(R(B), 121.904762) and ok(R(A, B), 160.533333) and ok(R(A, B, A * B), 161.333333)
# Example 1.4
assert ok(pf(29.833333, 3, 16), 0.000001, 1e-6) and ok(stats.t.ppf(.975, 16), 2.119905)
for p, r in ((2, 2.9980), (3, 3.1438), (4, 3.2349)):
    assert ok(sr.ppf(.95 ** (p - 1), p, 16), r, 1e-4)
assert ok(sr.ppf(.95, 4, 16), 4.0461, 1e-4)
# Unit 2
for F, p in ((635.25, 0), (210.583333, .000002), (70.583333, .000067), (28.583333, .001068), (5.25, .055702), (.583333, .469964)):
    assert ok(pf(F, 1, 7), p, 1e-6)
for F, p in ((42.666667, .000107), (2, .190947), (32.666667, .000289), (.25, .629071), (.083333, .779368)):
    assert ok(pf(F, 1, 9), p, 1e-6)
# Unit 3
assert ok(pf(59.666667, 3, 3), 0.003575, 1e-6)
# Unit 4, Example 4.3
a = 2 ** .5
pts = [(-1, -1), (1, -1), (-1, 1), (1, 1), (a, 0), (-a, 0), (0, a), (0, -a)] + [(0, 0)] * 5
f = lambda x1, x2: np.array([1, x1, x2, x1 * x1, x2 * x2, x1 * x2])
X = np.array([f(*p) for p in pts]); V = np.linalg.inv(X.T @ X)
for rho, val in ((0, .2), (.5, .190234), (1, .26875), (a, .625), (2, 2.2)):
    for ang in (0, 30, 45, 60, 90):
        t = np.radians(ang); v = f(rho * np.cos(t), rho * np.sin(t))
        assert ok(v @ V @ v, val)
print("design-and-analysis-of-experiments-advanced units: all recomputed values agree")
