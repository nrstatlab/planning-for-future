#!/usr/bin/env python3
"""Recompute the worked numbers of Multivariate Analysis (content check, November 2026)."""
import math
import numpy as np
from scipy import stats
from scipy.cluster.hierarchy import linkage

ok = lambda a, b, tol=6e-6: abs(a - b) <= tol * max(1, abs(b))
# Unit 1
assert ok(2520 * .5 ** 5 * .3 ** 3 * .2 ** 2, 0.08505)
S = np.array([[9, 6, 3], [6, 16, 4], [3, 4, 25.]]); b = S[0, 1:] @ np.linalg.inv(S[1:, 1:])
assert ok(np.linalg.det(S), 2556) and np.allclose(b, [23 / 64, 1 / 16]) and ok(9 - b @ S[1:, 0], 6.65625)
# Unit 2
assert ok(2 * stats.t.sf(.8 * math.sqrt(18) / .6, 18), 0.0000229, 1e-6)
z = (math.atanh(.8) - math.atanh(.5)) * math.sqrt(17); assert ok(z, 2.264847) and ok(2 * stats.norm.sf(z), 0.023522)
assert ok(math.tanh(math.atanh(.8) - 1.96 / math.sqrt(17)), 0.5534, 1e-4) and ok(math.tanh(math.atanh(.8) + 1.96 / math.sqrt(17)), 0.9177, 1e-4)
R = np.array([[1, .6, .5], [.6, 1, .4], [.5, .4, 1.]]); R2 = 1 - np.linalg.det(R) / .84
F = (R2 / 2) / ((1 - R2) / 25); assert ok(R2, 0.440476) and ok(F, 9.8404, 1e-4) and ok(stats.f.sf(F, 2, 25), 0.000704, 1e-6)
r = .4 / math.sqrt(.63); t = r * 5 / math.sqrt(1 - r * r); assert ok(r, 0.503953) and ok(t, 2.9173, 1e-4) and ok(2 * stats.t.sf(t, 25), 0.007359)
A = np.array([[100, 60, 40], [60, 90, 30], [40, 30, 80.]]); C = np.linalg.inv(A[1:, 1:]); beta = C @ A[1:, 0]
s2 = (100 - beta @ A[1:, 0]) / 17; se = np.sqrt(s2 * np.diag(C))
assert np.allclose(beta, [4 / 7, 2 / 7]) and ok(se[0], 0.201369) and ok(se[1], 0.213584)
assert ok(2 * stats.t.sf(beta[0] / se[0], 17), 0.0114, 1e-4) and ok(2 * stats.t.sf(beta[1] / se[1], 17), 0.1986, 1e-4)
assert ok(stats.f.sf(136 / 19, 2, 17), 0.0056, 1e-4)
# Unit 3
assert ok(stats.f.sf(160 / 27, 2, 8), 0.026373) and ok(stats.f.sf(6.4, 2, 24), 0.005921) and ok(stats.f.sf(250 / 7, 1, 9), 0.000209, 1e-6)
assert ok(-24 * math.log(15 / 23), 10.2587, 1e-4) and ok(stats.norm.cdf(-math.sqrt(2) / 2), 0.23975)
assert ok(stats.f.sf(96 / 19, 1, 24), 0.0340, 1e-4) and ok(stats.f.ppf(.95, 1, 24), 4.2597, 1e-4)
# Unit 4
w = np.linalg.eigvalsh(R)[::-1]; assert all(ok(a, b) for a, b in zip(w, (2.004458, 0.613092, 0.382451)))
M = np.linalg.inv([[1, .5], [.5, 1]]) @ [[.6, .3], [.3, .6]] @ np.linalg.inv([[1, .4], [.4, 1]]) @ [[.6, .3], [.3, .6]]
assert np.allclose(sorted(np.sqrt(np.linalg.eigvals(M).real)), [0.547723, 0.621059], atol=1e-6)
P = np.array([[1, 1], [2, 1], [4, 5], [7, 7], [5, 7.]])
for m, hts in (("single", (1, 2, 2.2361, 4.4721)), ("complete", (1, 2, 3.6056, 8.4853)), ("average", (1, 2, 2.9208, 6.6145))):
    assert np.allclose(linkage(P, m)[:, 2], hts, atol=6e-5)
B = np.array([[52, -2, -50], [-2, 25, -23], [-50, -23, 73]]) / 9; w = np.linalg.eigvalsh(B)
assert ok(w[2], 12.964148) and ok(w[1], 3.702519) and abs(w[0]) < 1e-9
print("multivariate-analysis: all recomputed values agree")
