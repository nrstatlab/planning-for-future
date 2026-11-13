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


# ---- Practical page: Practicals 13, 15, 16 (the others repeat unit examples, checked by hand) ----
def practical():
    # 13 split plot: y[rep][A][B]
    y = np.array([[[20, 24, 22], [26, 30, 29]], [[18, 23, 21], [27, 31, 29]], [[21, 26, 23], [27, 30, 30]]], float)
    G = y.sum(); CF = G * G / 18; tot = (y ** 2).sum() - CF
    SSR = (y.sum((1, 2)) ** 2).sum() / 6 - CF; SSA = (y.sum((0, 2)) ** 2).sum() / 9 - CF
    wp = (y.sum(2) ** 2).sum() / 3 - CF; SSB = (y.sum((0, 1)) ** 2).sum() / 6 - CF
    SSAB = (y.sum(0) ** 2).sum() / 3 - CF - SSA - SSB
    assert ok(tot, 274.277778) and ok(SSR, 5.777778) and ok(SSA, 206.722222) and ok(wp - SSR - SSA, 5.777778)
    assert ok(SSB, 52.777778) and ok(SSAB, 1.444444) and ok(tot - wp - SSB - SSAB, 1.777778)
    assert ok(SSA / 2.888889, 71.56, 1e-4) and ok(SSB / 2 / .222222, 118.75, 1e-4) and ok(SSAB / 2 / .222222, 3.25, 1e-4)
    assert ok(stats.f.ppf(.95, 1, 2), 18.51, 1e-3) and ok(stats.f.ppf(.95, 2, 8), 4.459, 1e-3)
    # 15 Youden square: fit rows + columns + treatments by least squares
    lay = [("A", 12, 0, 0), ("B", 15, 0, 1), ("C", 18, 0, 2), ("D", 21, 0, 3), ("B", 14, 1, 0), ("C", 17, 1, 1),
           ("D", 20, 1, 2), ("A", 13, 1, 3), ("C", 16, 2, 0), ("D", 22, 2, 1), ("A", 14, 2, 2), ("B", 16, 2, 3)]
    yv = np.array([l[1] for l in lay], float)
    def rss(use_t):
        X = [[1] + [l[2] == i for i in (1, 2)] + [l[3] == j for j in (1, 2, 3)] +
             ([l[0] == t for t in "BCD"] if use_t else []) for l in lay]
        X = np.array(X, float); b = np.linalg.lstsq(X, yv, rcond=None)[0]; return ((yv - X @ b) ** 2).sum(), b
    e1, b = rss(True); e0, _ = rss(False)
    assert ok(e1, 1.5) and ok(e0 - e1, 81.833333) and ok((e0 - e1) / 3 / .5, 54.56, 1e-4)
    tau = np.r_[0, b[-3:]]; tau -= tau.mean()
    assert np.allclose(16.5 + tau, [13.125, 15.125, 17.125, 20.625])
    # 16 triangular PBIBD
    lay = [("23", 15, 0), ("24", 17, 0), ("34", 21, 0), ("13", 12, 1), ("14", 14, 1), ("34", 22, 1),
           ("12", 9, 2), ("14", 13, 2), ("24", 16, 2), ("12", 10, 3), ("13", 12, 3), ("23", 16, 3)]
    tr = ["12", "13", "14", "23", "24", "34"]; yv = np.array([l[1] for l in lay], float)
    def fit(use_t):
        X = np.array([[1] + [l[2] == j for j in (1, 2, 3)] + ([l[0] == t for t in tr[1:]] if use_t else []) for l in lay], float)
        b = np.linalg.lstsq(X, yv, rcond=None)[0]; return ((yv - X @ b) ** 2).sum(), b, X
    e1, b, X = fit(True); e0, _, _ = fit(False)
    assert ok(e1, .25) and ok(e0 - e1, 117.75) and ok((yv ** 2).sum() - yv.sum() ** 2 / 12, 174.25)
    tau = np.r_[0, b[-5:]]; tau -= tau.mean()
    assert np.allclose(tau, [-5.125, -3.25, -1.125, .625, 2.25, 6.625])
    V = np.linalg.inv(X.T @ X) * (.25 / 3)
    c = lambda i, j: np.eye(6)[i] - np.eye(6)[j]
    def se(i, j):
        L = np.zeros(9); 
        if i: L[3 + i] = 1
        if j: L[3 + j] = -1
        return float(np.sqrt(L @ V @ L))
    assert ok(se(0, 1), 0.3227, 1e-4) and ok(se(0, 5), 0.3536, 1e-4)
    print("practical 13, 15, 16: all agree")


practical()
