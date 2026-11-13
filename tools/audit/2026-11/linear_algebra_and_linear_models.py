"""Recompute the worked numbers of Linear Algebra and Linear Models (content check, November 2026)."""
import numpy as np
from scipy import stats

ok = lambda a, b, tol=5e-7: abs(a - b) <= tol

# Unit 4, Example 4.1
assert ok(2 * stats.t.sf(6 / np.sqrt(2), 2), 0.051317)
# Unit 4, Example 4.2: correlations and variance inflation factors
x = np.array([[1, 2, 3, 4, 5], [2, 4, 6, 8, 11], [1, 3, 2, 5, 4]], float)
r = np.corrcoef(x)
assert ok(r[0, 1], 0.995893) and ok(r[0, 2], 0.8) and ok(r[1, 2], 0.769554)
vif = np.diag(np.linalg.inv(r))
assert all(ok(a, b, 5e-5) for a, b in zip(vif, (184.2593, 162.6667, 3.7037))), vif
assert all(ok(1 - 1 / a, b, 5e-9) for a, b in zip(vif, (0.99457286, 0.99385246, 0.73)))
# Unit 2, Example 2.1 and 2.3
A = np.ones((3, 3)) + np.eye(3)
assert [round(np.trace(np.linalg.matrix_power(A, k))) for k in (1, 2, 3)] == [6, 18, 66]
assert np.allclose(np.linalg.inv(A), np.eye(3) - np.ones((3, 3)) / 4)
# Unit 1, Example 1.3
B = np.array([[1, 0], [0, 1], [1, 1.0]])
assert np.allclose(np.linalg.pinv(B), np.array([[2, -1, 1], [-1, 2, 1]]) / 3)
print("linear-algebra-and-linear-models: all recomputed values agree")


# ---- Practical page: Practicals 10 to 14 --------------------------------
def practical():
    import numpy as np
    from scipy import stats
    ok = lambda a, b, tol=6e-7: abs(a - b) <= tol
    X = np.array([[2, 4, 6, 8, 10], [1, 3, 2, 5, 4], [5, 4, 6, 5, 8]], float).T
    S = np.cov(X, rowvar=False)
    assert np.allclose(S, [[10, 4, 3.5], [4, 2.5, .5], [3.5, .5, 2.3]])
    assert ok(np.trace(S), 14.8) and ok(np.linalg.det(S), 1.575) and ok(np.prod(np.diag(S)), 57.5)
    R = np.corrcoef(X, rowvar=False)
    assert ok(R[0, 2], 0.729800) and ok(R[1, 2], 0.208514)
    r231 = (R[1, 2] - R[0, 1] * R[0, 2]) / np.sqrt((1 - R[0, 1] ** 2) * (1 - R[0, 2] ** 2))
    assert ok(r231, -0.915, 6e-4) and ok(np.linalg.det(R), 0.027, 6e-4)
    # 11
    x = np.array([1, 1, 2, 2, 3, 3, 4, 4.]); y = np.array([3, 4, 6, 7, 8, 10, 11, 13.])
    Sxx = ((x - x.mean()) ** 2).sum(); Sxy = ((x - x.mean()) * (y - y.mean())).sum(); Syy = ((y - y.mean()) ** 2).sum()
    b1 = Sxy / Sxx; b0 = y.mean() - b1 * x.mean(); SSE = Syy - b1 * Sxy
    assert (Sxx, Sxy, Syy) == (10, 28, 83.5) and ok(b1, 2.8) and ok(b0, .75) and ok(SSE, 5.1)
    R2 = 1 - SSE / Syy
    assert ok(R2, 0.938922) and ok(1 - (1 - R2) * 7 / 6, 0.928743)
    t = stats.t.ppf(.975, 6); se = np.sqrt(SSE / 6 / Sxx)
    assert ok(t, 2.446912) and ok(se, 0.291548) and ok(b1 - t * se, 2.086609) and ok(b1 + t * se, 3.513391)
    pe = sum(((y[x == g] - y[x == g].mean()) ** 2).sum() for g in (1, 2, 3, 4))
    F = ((SSE - pe) / 2) / (pe / 4)
    assert ok(pe, 5) and ok(F, 0.04) and ok(stats.f.sf(F, 2, 4), 0.961169)
    # 12
    x1, x2 = X[:, 0], X[:, 1]; y = np.array([12, 18, 20, 28, 32.])
    D = np.column_stack([np.ones(5), x1, x2]); A = D.T @ D
    assert np.allclose(A, [[5, 30, 15], [30, 220, 106], [15, 106, 55]]) and np.allclose(D.T @ y, [110, 760, 374])
    assert ok(np.linalg.det(A), 720, 1e-6)
    b = np.linalg.solve(A, D.T @ y); assert np.allclose(b, [19 / 3, 37 / 18, 10 / 9])
    SST = ((y - y.mean()) ** 2).sum(); SSE = ((y - D @ b) ** 2).sum()
    assert ok(SST, 256) and ok(SSE, 1.555556) and ok(1 - SSE / SST, 0.993924) and ok(1 - (SSE / 2) / (SST / 4), 0.987847)
    F = ((SST - SSE) / 2) / (SSE / 2); assert ok(F, 163.571429, 1e-5) and ok(stats.f.sf(F, 2, 2), 0.006076)
    C = np.linalg.inv(A); assert ok(C[1, 1], 5 / 72) and ok(C[2, 2], 5 / 18)
    for j, (se_, t_, p_) in ((1, (0.232406, 8.844692, 0.012543)), (2, (0.464811, 2.390457, 0.139337))):
        se = np.sqrt(SSE / 2 * C[j, j]); tt = b[j] / se
        assert ok(se, se_) and ok(tt, t_, 2e-6) and ok(2 * stats.t.sf(tt, 2), p_)
    # 13
    r01, r02, r12 = np.corrcoef(y, x1)[0, 1], np.corrcoef(y, x2)[0, 1], np.corrcoef(x1, x2)[0, 1]
    assert ok(r01, 0.988212) and ok(r02, 0.869626) and ok(r12, .8)
    assert ok((r01 - r02 * r12) / np.sqrt((1 - r02 ** 2) * (1 - r12 ** 2)), 0.987457)
    assert ok((r02 - r01 * r12) / np.sqrt((1 - r01 ** 2) * (1 - r12 ** 2)), 0.860663)
    assert ok(np.sqrt((r01 ** 2 + r02 ** 2 - 2 * r01 * r02 * r12) / (1 - r12 ** 2)), 0.996957)
    # 14
    Z = np.array([[1, 2, 3, 4, 5], [2, 4, 6, 8, 11], [1, 3, 2, 5, 4]], float).T
    ev = sorted(np.linalg.eigvalsh(np.corrcoef(Z, rowvar=False)), reverse=True)
    assert all(ok(a, b) for a, b in zip(ev, (2.714426, 0.282689, 0.002884)))
    assert ok(np.sqrt(ev[0] / ev[2]), 30.67827, 1e-4)
    print("practical 10-14: all agree")


practical()
