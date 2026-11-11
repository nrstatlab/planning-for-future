#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recompute the numerical answers of the UGC NET model questions.

    python3 ugc_model_verify.py        (needs numpy, scipy and sympy)

For each unit, CHECKS maps a question number to (key, value, tolerance or
None): the value is computed here from the data of the question, by a route
that does not use the explanation, and must equal EXPECT, the value of the
keyed option typed in from the page. The key must also be the one in the data.
Run when a unit is written or changed; it is not part of the build.
"""
import importlib
import math
import sys
from fractions import Fraction as F

import numpy as np
from scipy import integrate, stats

sys.path.insert(0, __import__("os").path.dirname(__file__))
inf = math.inf


def p2_unit01():
    c = {}
    # 1: statements I, II true, III false
    pab = 0.5 + 0.6 - 0.8
    c[1] = ("B", (abs(pab - 0.3) < 1e-12, abs(1 - 0.8 - 0.2) < 1e-12, abs((0.5 - pab) / 0.4 - 0.4) < 1e-9), (True, True, False))
    import itertools
    der = sum(all(p[i] != i for i in range(4)) for p in itertools.permutations(range(4)))
    c[2] = ("A", F(der, 24), F(3, 8))
    c[3] = ("C", F(20 * 5, 50 * 2 + 30 * 3 + 20 * 5), F(10, 29))
    c[4] = ("D", sum(F(5, 6) ** (2 * k - 1) * F(1, 6) for k in range(1, 400)), F(5, 11), 1e-12)
    Fx = lambda x: 0 if x < 0 else (x + 1) / 4 if x < 1 else 0.75 if x < 2 else 1
    c[6] = ("C", (Fx(2) - Fx(0.5), Fx(1) - Fx(1 - 1e-12)), (5 / 8, 1 / 4), 1e-9)
    c[7] = ("B", integrate.quad(lambda x: 3 * x * x, .5, 1)[0] / integrate.quad(lambda x: 3 * x * x, .25, 1)[0], 8 / 9, 1e-10)
    c[8] = ("D", stats.foldnorm.mean(0, scale=2), 2 * math.sqrt(2 / math.pi), 1e-10)
    c[9] = ("A", sum(k * (1 / k ** 2 - 1 / (k + 1) ** 2) for k in range(1, 2000000)), math.pi ** 2 / 6, 1e-5)
    rng = np.random.default_rng(1)
    N = rng.poisson(4, 400000)
    S = np.array([rng.gamma(4 / 3, 1.5, n).sum() for n in N])      # mean 2, variance 3
    c[10] = ("C", S.var(), 28, 0.5)
    g = stats.chi2(6)
    c[11] = ("B", (g.var(), g.expect(lambda x: 1 / x)), (12, 0.25), 1e-6)
    c[12] = ("D", float(stats.gamma(3, scale=.5).stats(moments="s")), 2 / math.sqrt(3), 1e-10)
    c[13] = ("C", stats.poisson(2).pmf(4), 2 / (3 * math.e ** 2), 1e-12)
    c[14] = ("A", stats.geom(1 / 3).sf(5) / stats.geom(1 / 3).sf(2), 8 / 27, 1e-12)
    c[15] = ("D", stats.hypergeom(20, 8, 5).var(), 18 / 19, 1e-12)
    pm = stats.binom(9, .4).pmf(range(10))
    c[16] = ("B", tuple(int(i) for i in np.flatnonzero(np.isclose(pm, pm.max()))), (3, 4))
    c[17] = ("C", stats.binom(5, 2 / 5).var(), 6 / 5, 1e-12)
    c[18] = ("D", integrate.quad(lambda t: 1 - (1 - math.exp(-t / 6)) ** 3, 0, inf)[0], 11, 1e-8)
    qd, md = stats.norm.ppf(.75), math.sqrt(2 / math.pi)
    c[19] = ("A", (round(qd * 15), round(md * 15)), (10, 12))
    c[21] = ("B", stats.beta(2, 3).var(), 1 / 25, 1e-12)
    ln = stats.lognorm(1)
    c[22] = ("C", (ln.mean(), ln.median(), ln.var()), (math.e ** .5, 1, math.e * (math.e - 1)), 1e-9)
    c[23] = ("A", integrate.quad(lambda t: math.exp(-t * t), 0, inf)[0], math.sqrt(math.pi) / 2, 1e-10)
    E = lambda f: integrate.dblquad(lambda x, y: 2 * f(x, y), 0, 1, 0, lambda y: y)[0]
    ex, ey = E(lambda x, y: x), E(lambda x, y: y)
    cov = E(lambda x, y: x * y) - ex * ey
    c[24] = ("B", cov / math.sqrt((E(lambda x, y: x * x) - ex ** 2) * (E(lambda x, y: y * y) - ey ** 2)), .5, 1e-9)
    c[25] = ("D", (.5 * 2 / 1 * 1, 4 * (1 - .25)), (1, 3), 1e-12)
    c[26] = ("C", integrate.dblquad(lambda y, x: math.exp(-y), 0, 50, lambda x: 2 * x, 100)[0], .5, 1e-8)
    c[27] = ("A", 4 * 4 + 9 - 2 * 2 * (-.5 * 2 * 3), 37, 1e-12)
    cv = stats.multinomial(12, [1 / 2, 1 / 3, 1 / 6]).cov()
    c[28] = ("B", cv[0, 1] / math.sqrt(cv[0, 0] * cv[1, 1]), -1 / math.sqrt(2), 1e-12)
    c[29] = ("D", 1 - F(4, 36), F(8, 9))
    c[31] = ("A", (3 / 9) ** 2 * stats.chi2(9).var(), 2, 1e-12)
    c[33] = ("C", stats.beta(4, 2).mean(), 2 / 3, 1e-12)
    x = rng.standard_normal((4, 400000))
    c[34] = ("D", stats.kstest((x[0] - x[1]) / np.sqrt(x[2] ** 2 + x[3] ** 2), stats.t(2).cdf).pvalue > 0.001, True)
    c[35] = ("B", stats.kstest(2 / 3 * rng.exponential(3, (5, 300000)).sum(0), stats.chi2(10).cdf).pvalue > 0.001, True)
    c[36] = ("A", stats.kstest(-2 * np.log(rng.random(300000)), stats.chi2(2).cdf).pvalue > 0.001, True)
    c[37] = ("C", (stats.kstest(x[0] / x[1], stats.cauchy.cdf).pvalue > .001,
                   stats.kstest(x[0] ** 2 + x[1] ** 2, stats.expon(scale=2).cdf).pvalue > .001,
                   stats.kstest(x[0] ** 2 / (x[0] ** 2 + x[1] ** 2), stats.beta(.5, .5).cdf).pvalue > .001), (True, True, True))
    c[38] = ("D", integrate.quad(lambda u: min(1, 1 / (2 * u)), 0, 1, points=[.5])[0], (1 + math.log(2)) / 2, 1e-9)
    c[41] = ("B", stats.uniform(-1, 2).var(), 1 / 3, 1e-12)
    c[46] = ("D", 4 * (1 / (2 * math.sqrt(4))) ** 2, 1 / 4, 1e-12)
    for a, ok in ((.3, True), (.45, True), (.5, False), (.7, False)):
        r = [sum(k ** (2 * a) for k in range(1, n + 1)) / n ** 2 for n in (10 ** 3, 10 ** 5)]
        assert (r[1] < r[0] * .8) == ok, a
    c[47] = ("B", True, True)
    c[48] = ("A", integrate.quad(lambda t: 2 / t ** 2, 1, inf)[0], 2, 1e-9)
    c[49] = ("C", round(1 - stats.norm.cdf((26 - 24) / math.sqrt(48 / 12)), 4), 0.1587)
    c[50] = ("D", stats.poisson(10 ** 7).cdf(10 ** 7), .5, 1e-3)
    return c


def p2_unit02():
    import sympy as sp
    x, y, n, k = sp.symbols("x y n k", positive=True)
    c = {}
    c[3] = ("B", sp.limit((1 + 2 / n) ** (3 * n), n, sp.oo), sp.exp(6))
    a = [math.sin(i * math.pi / 2) + (-1) ** i for i in range(1, 401)]
    c[4] = ("A", (round(max(a[100:])), round(min(a[100:]))), (1, -2))
    v = 1.0
    for _ in range(200):
        v = math.sqrt(6 + v)
    c[5] = ("C", v, 3, 1e-12)
    c[7] = ("D", sp.summation(1 / (k * (k + 1) * (k + 2)), (k, 1, sp.oo)), sp.Rational(1, 4))
    c[8] = ("A", (sp.integrate(1 / (x * sp.log(x) ** 2), (x, 2, sp.oo)).is_finite,
                  sp.integrate(1 / (x * sp.log(x)), (x, 2, sp.oo)).is_finite), (True, False))
    c[9] = ("D", sp.summation(k / 2 ** k, (k, 1, sp.oo)), 2)
    c[10] = ("C", sp.summation(k ** 2 / 2 ** k, (k, 1, sp.oo)), 6)
    c[12] = ("B", sp.limit(sp.factorial(n) / n ** n / (sp.factorial(n + 1) / (n + 1) ** (n + 1)), n, sp.oo), sp.E)
    c[16] = ("B", (max(t / (1 + 10 ** 6 * t * t) for t in np.linspace(0, 1, 200001)) < 1e-3,
                   abs(max(10 ** 3 * t / (1 + 10 ** 6 * t * t) for t in np.linspace(0, 1, 200001)) - .5) < 1e-6), (True, True))
    f = x ** 3 - 3 * x
    c[17] = ("D", sp.solve(sp.Eq(sp.diff(f, x), (f.subs(x, 2) - f.subs(x, 0)) / 2), x), [2 / sp.sqrt(3)])
    X = sp.symbols("X", real=True)
    g = lambda t: math.exp(t) - 1 - t - t * t / 2
    grid = np.linspace(-30, 30, 600001)
    gv = np.array([g(t) for t in grid])
    c[18] = ("A", int(np.sum(np.sign(gv[1:]) != np.sign(gv[:-1]))) <= 2 and g(-1e-3) < 0 < g(1e-3), True)
    c[19] = ("B", sp.series(sp.exp(X) * sp.cos(X), X, 0, 6).coeff(X, 4), sp.Rational(-1, 6))
    c[21] = ("C", sp.integrate(x ** 2 * sp.exp(-x ** 2), (x, 0, sp.oo)), sp.sqrt(sp.pi) / 4)
    c[23] = ("A", sum(10 ** 6 / (10 ** 12 + j * j) for j in range(1, 10 ** 6 + 1)), math.pi / 4, 1e-6)
    t = sp.symbols("t")
    c[25] = ("D", sp.simplify(sp.diff(sp.integrate(sp.exp(-t ** 2), (t, X, X ** 2)), X).subs(X, 1)), sp.exp(-1))
    c[26] = ("C", sp.integrate(sp.sin(X) ** 4 * sp.cos(X) ** 2, (X, 0, sp.pi / 2)), sp.pi / 32)
    Y = sp.symbols("Y", real=True)
    F = X ** 3 + Y ** 3 - 3 * X * Y
    crit = sp.solve([sp.diff(F, X), sp.diff(F, Y)], [X, Y], dict=True)
    H = sp.hessian(F, (X, Y))
    kinds = {(s[X], s[Y]): ("min" if H.subs(s).det() > 0 and H.subs(s)[0, 0] > 0 else "saddle" if H.subs(s).det() < 0 else "?")
             for s in crit if s[X].is_real}
    c[28] = ("D", kinds, {(0, 0): "saddle", (1, 1): "min"})
    c[29] = ("A", integrate.dblquad(lambda yy, xx: math.exp(yy * yy), 0, 1, lambda xx: xx, 1)[0], (math.e - 1) / 2, 1e-9)
    th = np.linspace(0, 2 * math.pi, 2000001)
    c[30] = ("C", float(np.max(2 * math.sqrt(2) * np.cos(th) * math.sqrt(2) * np.sin(th))), 2, 1e-9)
    c[31] = ("D", integrate.dblquad(lambda r, a: r / (1 + r * r), 0, 2 * math.pi, 0, 1)[0], math.pi * math.log(2), 1e-9)
    kk = sp.symbols("kk")
    c[34] = ("A", sp.solve(sp.Matrix([[1, 2, 3], [2, 3, 4], [3, 5, kk]]).det(), kk), [7])
    c[36] = ("B", int(np.linalg.matrix_rank(np.ones((4, 4)) - 4 * np.eye(4))), 3)
    A = sp.Matrix([[1, 2, 0], [0, 1, 0], [3, 1, 2]])       # det 2
    c[38] = ("D", (A.det(), (2 * A).adjugate().det()), (2, 256))
    D = sp.diag(1, 2, 3)
    c[39] = ("C", (D ** 2 - D + sp.eye(3)).det(), 21)
    lam, mu = sp.symbols("lam mu")
    Mx = sp.Matrix([[1, 1, 1], [1, 2, 3], [1, 2, lam]])
    c[40] = ("B", (sp.solve(Mx.det(), lam), Mx.subs(lam, 3).rank(), Mx.subs(lam, 3).row_join(sp.Matrix([6, 10, 11])).rank(),
                   Mx.subs(lam, 3).row_join(sp.Matrix([6, 10, 10])).rank()), ([3], 2, 3, 2))
    q, _ = np.linalg.qr(np.array([[1, 1], [1, 0], [0, 1.0]]))
    u2 = q[:, 1] * np.sign(q[0, 1])
    c[41] = ("A", tuple(np.round(u2 * math.sqrt(6), 9)), (1, -1, 2), 1e-8)
    c[42] = ("C", (sp.Matrix([[4, 1], [2, 3]]) ** 3).trace(), 133)
    P = sp.Matrix([[1, 0, 0], [0, 1, 0], [1, 1, 0]])      # idempotent, rank 2
    c[43] = ("B", (P * P == P, P.rank(), (sp.eye(3) + P).det()), (True, 2, 4))
    B = sp.Matrix([[1, 2], [3, 4]])
    c[44] = ("D", B.inv() == (B - 5 * sp.eye(2)) / 2, True)
    S = sp.Matrix([[0, 2, -1], [-2, 0, 3], [1, -3, 0]])
    Pm = (sp.eye(3) - S) * (sp.eye(3) + S).inv()
    c[47] = ("B", sp.simplify(Pm.T * Pm) == sp.eye(3), True)
    pd = lambda a: bool(np.all(np.linalg.eigvalsh((1 - a) * np.eye(3) + a * np.ones((3, 3))) > 0))
    c[48] = ("C", (pd(-.49), pd(-.51), pd(.99), pd(1.01), pd(0)), (True, False, True, False, True))
    ev = np.linalg.eigvalsh(np.ones((3, 3)) - np.eye(3))
    c[49] = ("D", (int(np.sum(abs(ev) > 1e-9)), int(np.sum(ev > 1e-9) - np.sum(ev < -1e-9))), (3, -1))
    return c


def p2_unit03():
    import itertools
    c = {}
    S2, N, n = 20, 50, 10
    c[1] = ("B", ((1 / n - 1 / N) * S2, (N - 1) / N * S2 / n), (1.60, 1.96), 1e-12)
    c[2] = ("D", F(math.comb(8, 2), math.comb(10, 4)), F(2, 15))
    c[3] = ("A", (4 * .25 / .05 ** 2) / (1 + (4 * .25 / .05 ** 2) / 1600), 320, 1e-9)
    c[5] = ("B", F(sum(len(set(s)) for s in itertools.product(range(5), repeat=3)), 125), F(61, 25))
    pop = [1, 2, 3, 6]
    prs = list(itertools.permutations(pop, 2))
    c[6] = ("D", F(sum(a * b for a, b in prs), 12) - F(sum(a for a, b in prs), 12) ** 2, F(-7, 6))
    Nh, Sh, ch = np.array([400, 600]), np.array([10, 20]), np.array([4, 16])
    c[7] = ("A", tuple(100 * Nh * Sh / (Nh * Sh).sum()), (25, 75), 1e-9)
    W = Nh / 1000
    c[9] = ("D", .9 / 100 * (W * Sh ** 2).sum(), 2.52, 1e-12)
    c[10] = ("B", tuple(100 * (Nh * Sh / np.sqrt(ch)) / (Nh * Sh / np.sqrt(ch)).sum()), (40, 60), 1e-9)
    nh = 100 * Nh * Sh / (Nh * Sh).sum()
    c[12] = ("C", float((W ** 2 * Sh ** 2 * (1 / nh - 1 / Nh)).sum()), 2.28, 1e-12)
    # 8: order of the three variances for a population made to these strata
    c[8] = ("C", 2.28 <= 2.52, True)
    y = np.arange(1, 13)
    means = [y[i::4].mean() for i in range(4)]
    c[15] = ("C", (float(np.var(means)), (1 / 3 - 1 / 12) * y.var(ddof=1)), (1.25, 3.25), 1e-12)
    # 13, 14: a linear trend, N = nk
    Nn, nn, kk = 60, 6, 10
    yy = np.arange(1, Nn + 1.0)
    vsy = np.var([yy[i::kk].mean() for i in range(kk)])
    vran = (1 / nn - 1 / Nn) * yy.var(ddof=1)
    vst = sum((1 - 1 / kk) * yy[h * kk:(h + 1) * kk].var(ddof=1) for h in range(nn)) / nn ** 2
    c[14] = ("D", vst <= vsy <= vran, True)
    rho = (vsy / (yy.var(ddof=1) / nn * (Nn - 1) / Nn) - 1) / (nn - 1)
    c[13] = ("A", (vsy < vran) == (rho < -1 / (Nn - 1)), True)
    c[16] = ("B", .5 * .4 / .5, .4, 1e-12)
    c[17] = ("D", (22 / 44 * 50, 22 + .6 * (50 - 44)), (25, 25.6), 1e-12)
    c[18] = ("A", round(100 / (1 - .64)), 278)
    c[20] = ("B", (100 + 64 - 2 * .8 * 10 * 8) / 36, 1, 1e-12)
    c[21] = ("C", 1 + 9 * .1, 1.9, 1e-12)
    c[23] = ("D", 20 / 10 + 100 / 50, 4, 1e-12)
    c[24] = ("B", 100 * (1 - .64) / 20 + .64 * 100 / 100, 2.44, 1e-12)
    c[25] = ("A", (20 / .2 + 30 / .4) / 2, 87.5, 1e-12)
    c[26] = ("C", 10 / .5 + 20 / .25 + 30 / .5, 160, 1e-12)
    c[28] = ("B", F(10 + 20 + 30 + 40, 4 * 40), F(5, 8))
    c[29] = ("C", (90 / 3) / ((250 - 90) / 16), 3, 1e-12)
    c[30] = ("A", (50 - 10) / 5, 8, 1e-12)
    T = np.array([20, 30, 40])
    c[31] = ("D", (float((T @ [-1, 0, 1]) ** 2 / (5 * 2)), float((T ** 2).sum() / 5 - T.sum() ** 2 / 15)), (40, 40), 1e-12)
    c[32] = ("B", ((3 - 1) * (4 - 1), 3 * 4 * (2 - 1)), (6, 12))
    c[35] = ("B", 36 - 1 - 3 * 5, 20)
    c[37] = ("C", round((3 * 30 + 4 * 4 * 5) / (19 * 5), 2), 1.79)
    c[38] = ("A", (round(stats.t.ppf(.975, 12), 3), round(2.179 * math.sqrt(2 * 8 / 4), 2)), (2.179, 4.36))
    # 40: the missing-plot formula minimises the error SS
    rng = np.random.default_rng(3)
    Y = rng.normal(10, 2, (4, 5))            # blocks x treatments, cell (0, 0) missing
    def ess(x):
        Z = Y.copy(); Z[0, 0] = x
        return ((Z - Z.mean(1, keepdims=True) - Z.mean(0) + Z.mean()) ** 2).sum()
    from scipy import optimize
    B, Tt, G = Y[0, 1:].sum(), Y[1:, 0].sum(), Y.sum() - Y[0, 0]
    c[40] = ("D", (abs(optimize.minimize_scalar(ess).x - (4 * B + 5 * Tt - G) / 12) < 1e-5, (4 * 50 + 5 * 40 - 340) / 12), (True, 5.0))
    c[41] = ("A", (4 * (20 + 24 + 22) - 2 * 120) / 6, 4, 1e-12)
    A = 44 + 30 - 26 - 20
    c[42] = ("C", (A / 10, A ** 2 / 20), (2.8, 39.2), 1e-12)
    c[43] = ("B", 24 - 1 - 2 - 7, 14)
    combos = ["(1)", "a", "b", "ab", "c", "ac", "bc", "abc"]
    sign = lambda t, eff: (-1) ** sum(1 for l in eff if l not in t)
    c[44] = ("D", tuple(t for t in combos if sign(t, "abc") > 0), ("a", "b", "c", "abc"))
    c[45] = ("A", tuple(t for t in combos if sum(l in t for l in "abc") % 2 == 0), ("(1)", "ab", "ac", "bc"))
    c[46] = ("C", "".join(sorted(set("ABC") ^ set("BCD"))), "AD")
    ok = lambda v, b, r, k, l: b * k == v * r and l * (v - 1) == r * (k - 1) and b >= v
    c[48] = ("D", (ok(7, 7, 3, 3, 1), ok(9, 12, 4, 3, 1), ok(6, 10, 5, 3, 2), ok(8, 8, 4, 4, 2)), (True, True, True, False))
    c[49] = ("C", F(1 * 7, 3 * 3), F(7, 9))
    return c


UNITS = {("p2", 1): p2_unit01, ("p2", 2): p2_unit02, ("p2", 3): p2_unit03}


def same(a, b, tol):
    if isinstance(a, tuple):
        return len(a) == len(b) and all(same(x, y, tol) for x, y in zip(a, b))
    if tol is None or isinstance(a, (bool, np.bool_)):
        return bool(a == b)
    return abs(float(a) - float(b)) <= tol


def main():
    bad = 0
    for (paper, n), fn in UNITS.items():
        qs = [q for q in importlib.import_module("ugc_model_data.%s_unit%02d" % (paper, n)).QUESTIONS
              if not isinstance(q, tuple)]
        checks = fn()
        for k, v in sorted(checks.items()):
            key, got, want = v[0], v[1], v[2]
            tol = v[3] if len(v) > 3 else None
            if qs[k - 1]["k"] != key:
                bad += 1
                print("%s unit %d Q%d: key in the data is %s, checked %s" % (paper, n, k, qs[k - 1]["k"], key))
            if not same(got, want, tol):
                bad += 1
                print("%s unit %d Q%d: computed %r, the keyed option says %r" % (paper, n, k, got, want))
        print("%s unit %d: %d of %d answers recomputed" % (paper, n, len(checks), len(qs)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
