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
import re
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


def p2_unit04():
    c = {}
    n, p = 7, .3
    b = stats.binom(n, p)
    c[1] = ("B", b.expect(lambda x: x * (x - 1) / (n * (n - 1))), p * p, 1e-12)
    c[2] = ("D", stats.poisson(1.3).expect(lambda x: (-1.0) ** x), math.exp(-2.6), 1e-10)
    m = 9
    mse = lambda cc: cc * cc * (m * m - 1) - 2 * cc * (m - 1) + 1
    best = min((mse(1 / d), d) for d in (m - 2, m - 1, m, m + 1, m + 2))[1]
    c[3] = ("A", best, m + 1)
    c[4] = ("C", 1 / (m * (m + 2)) < 1 / (3 * m), True)
    c[7] = ("D", (1 - 2.0 / (10 ** 7 * 3)) ** 10 ** 7, math.exp(-2 / 3), 1e-6)
    c[8] = ("C", (6 ** 2 / 12, 12 / 6), (3, 2), 1e-12)
    c[9] = ("A", .6 / .4, 1.5, 1e-12)
    c[10] = ("D", 10 / 4, 2.5, 1e-12)
    c[13] = ("A", 20 + 1.645 * math.sqrt(90 / 10), 24.935, 1e-9)
    c[16] = ("B", (-1 + math.sqrt(1 + 4 * 6)) / 2, 2, 1e-12)
    c[17] = ("A", 1 / (4 * stats.norm.pdf(0) ** 2), math.pi / 2, 1e-12)
    I = integrate.quad(lambda x: ((x * x - 1) / 2) ** 2 * stats.norm.pdf(x), -inf, inf)[0]
    c[19] = ("D", 1 / I, 2, 1e-8)                 # sigma = 1: bound 2 sigma^4 / n per observation
    c[21] = ("C", 1 / integrate.quad(lambda u: 4 * u * u / (1 + u * u) ** 2 / (math.pi * (1 + u * u)), -inf, inf)[0], 2, 1e-8)
    lam, nn = 1.7, 6
    T = stats.poisson(nn * lam)
    var = T.expect(lambda t: (1 - 1 / nn) ** (2 * t)) - math.exp(-2 * lam)
    c[23] = ("A", (abs(T.expect(lambda t: (1 - 1 / nn) ** t) - math.exp(-lam)) < 1e-10, var > lam * math.exp(-2 * lam) / nn,
                   abs(var - math.exp(-2 * lam) * (math.exp(lam / nn) - 1)) < 1e-10), (True, True, True))
    c[27] = ("D", stats.binom(2, .5).pmf(1), .5, 1e-12)
    c[29] = ("B", stats.beta(4, 2).mean(), (5 - 1) / (5 + 1), 1e-12)      # E(range), n = 5
    g = np.array([1, -5 / 3, 1])
    c[32] = ("D", tuple(abs(float(stats.binom(2, q).pmf([0, 1, 2]) @ g)) < 1e-12 for q in (.25, .75)), (True, True))
    c[33] = ("A", round(.8 ** 10, 3), 0.107)
    c[34] = ("B", F(math.comb(8, 2), math.comb(10, 4)), F(2, 15))
    c[36] = ("A", stats.gamma(5).expect(lambda t: t * t) / (5 * 6), 1, 1e-9)
    c[37] = ("C", stats.gamma(5).expect(lambda t: 4 / t), 1, 1e-9)
    c[39] = ("B", stats.beta(1, 3).moment(2), .1, 1e-12)
    c[40] = ("D", (8, 8 * (1 / 16) ** (-1 / 4), 1 - (1 / 2) ** 4), (8, 16, 15 / 16), 1e-9)
    c[41] = ("A", (round(stats.chi2.ppf(.975, 10), 2), round(stats.chi2.ppf(.025, 10), 2), round(40 / 20.48, 2), round(40 / 3.25, 2)),
             (20.48, 3.25, 1.95, 12.31))
    c[42] = ("C", (round(stats.t.ppf(.975, 15), 3), round(50 - 2.131 * 2, 2), round(50 + 2.131 * 2, 2)), (2.131, 45.74, 54.26))
    c[43] = ("B", (round(stats.chi2.ppf(.975, 9), 2), round(stats.chi2.ppf(.025, 9), 2), round(36 / 19.02, 2), round(36 / 2.70, 2)),
             (19.02, 2.70, 1.89, 13.33))
    c[46] = ("A", (round(.2 - 1.96 * .02, 3), round(.2 + 1.96 * .02, 3)), (0.161, 0.239))
    c[47] = ("B", .2 * .8 / 25, .0064, 1e-12)
    c[48] = ("C", stats.beta(2, 2).cdf(.25), 5 / 32, 1e-12)
    c[49] = ("B", 1 - 6 * 42 / (8 * 63), .5, 1e-12)
    x, y = [1, 2, 3, 4, 5], [2, 1, 4, 3, 5]
    c[50] = ("D", (stats.kendalltau(x, y)[0], stats.spearmanr(x, y)[0]), (.6, .8), 1e-12)
    return c


def p2_unit05():
    c = {}
    N = stats.norm
    c[1] = ("B", (1 - .9, (2 - .9) / 2), (.10, .55), 1e-12)
    c[2] = ("D", (round(N.sf(.5 * 3), 4), round(N.cdf((.5 - 1) * 3), 4)), (.0668, .0668))
    c[3] = ("A", round(2 * (1 - .9599), 4), .0802)
    c[5] = ("B", round(math.exp(-math.log(20) / 2), 3), .224)
    c[6] = ("A", .05 / stats.binom(3, .5).pmf(3), .40, 1e-12)
    c[7] = ("D", (round(stats.poisson(2).cdf(2), 3), round(stats.poisson(1).sf(2), 3)), (.677, .080))
    c[8] = ("C", 1 - .9 ** 2, .19, 1e-12)
    c[9] = ("A", round(stats.chi2.isf(.05, 10), 2), 18.31)
    p0, p1 = np.array([.1, .2, .3, .4]), np.array([.4, .3, .2, .1])
    import itertools
    best = max((p1[list(s)].sum(), s) for r in range(1, 4) for s in itertools.combinations(range(4), r)
               if abs(p0[list(s)].sum() - .3) < 1e-12)
    c[11] = ("D", (best[1], round(best[0], 10)), ((0, 1), .7))
    c[17] = ("C", round(N.sf(1.645 - .5 * 4), 3), .639)
    c[18] = ("B", (math.ceil((1.645 + 1.282) ** 2 / .25), math.ceil((1.96 + 1.282) ** 2 / .25)), (35, 43))
    c[21] = ("D", 4 * (1 - 0) ** 2, 4)
    rng = np.random.default_rng(5)
    x = rng.normal(.3, 2, 12)
    t = stats.ttest_1samp(x, 0).statistic
    lam = (x.var() / ((x - 0) ** 2).mean()) ** (12 / 2)
    c[22] = ("B", lam ** (2 / 12), 1 / (1 + t * t / 11), 1e-12)
    c[23] = ("C", round(2 ** 5 * math.exp(-5), 4), .2156)
    c[25] = ("D", (.9 / .05, round(.1 / .95, 3)), (18, .105), 1e-9)
    c[26] = ("B", round(math.log(.5 / .25) / math.log(.75 * .5 / (.5 * .25)), 3), .631)
    c[27] = ("C", round((.95 * -2.944 + .05 * 2.944) / -.5, 2), 5.30)
    o = np.array([8, 9, 10, 13, 12, 8])
    c[30] = ("D", stats.chisquare(o).statistic, 2.2, 1e-12)
    tb = np.array([[20, 10], [10, 20]])
    c[31] = ("C", (round(stats.chi2_contingency(tb, correction=False)[0], 2), round(stats.chi2_contingency(tb, correction=True)[0], 2)), (6.67, 5.40))
    c[32] = ("B", 7 - 1 - 1, 5)
    c[33] = ("A", (3 - 1) * (4 - 1), 6)
    c[34] = ("D", (24 * 36 / 25, round(stats.chi2.isf(.05, 24), 2)), (34.56, 36.42), 1e-9)
    c[36] = ("B", round(math.sqrt(20 / 100), 3), .447)
    c[37] = ("A", round(2 * stats.binom(10, .5).sf(7), 3), .109)
    c[38] = ("D", 4 * N.pdf(0) ** 2, 2 / math.pi, 1e-12)
    c[39] = ("C", (60 - 50) / 5, 2.0, 1e-12)
    c[40] = ("B", (10 * 11 / 4, 10 * 11 * 21 / 24), (27.5, 96.25), 1e-12)
    d = np.array([3, -1, 5, -2, 4, 6])
    c[41] = ("A", int(stats.rankdata(abs(d))[d > 0].sum()), 18)
    c[42] = ("D", F(sum(1 for s in itertools.product([0, 1], repeat=4) if sum((i + 1) * b for i, b in enumerate(s)) <= 1), 16), F(1, 8))
    c[44] = ("C", (4 * 5 / 2, round(4 * 5 * 10 / 12, 2)), (10, 16.67), 1e-9)
    X, Y = [1, 4, 6], [2, 3, 5, 7]
    c[45] = ("B", (int(stats.rankdata(X + Y)[:3].sum()), sum(a > b for a in X for b in Y)), (11, 5))
    c[46] = ("D", F(1, math.comb(6, 3)), F(1, 20))
    are = lambda dist: 12 * dist.var() * integrate.quad(lambda u: dist.pdf(u) ** 2, *dist.support())[0] ** 2
    c[47] = ("C", (are(N), are(stats.uniform), are(stats.laplace)), (3 / math.pi, 1, 1.5), 1e-7)
    c[50] = ("D", stats.kruskal([1, 2, 3], [4, 5, 6], [7, 8, 9]).statistic, 7.2, 1e-9)
    return c


def p2_unit06():
    c = {}
    b = (560 - 50 * 100 / 10) / (310 - 50 ** 2 / 10)
    c[1] = ("B", (10 - b * 5) + b * 8, 13, 1e-12)
    xm, ym = np.linalg.solve([[3, 2], [6, 1]], [26, 31])
    c[2] = ("D", (-math.sqrt((-3 / 2) * (-1 / 6)), round(float(xm), 9), round(float(ym), 9), (-2 / 3) * (-6) > 1), (-.5, 4, 7, True), 1e-12)
    rng = np.random.default_rng(11)
    x = rng.normal(size=15); y = 1 + 2 * x + rng.normal(size=15)
    bb = np.polyfit(x, y, 1); e = y - np.polyval(bb, x)
    c[3] = ("A", (abs(e.sum()) < 1e-9, abs((x * e).sum()) < 1e-9, abs((y * e).sum() - (e * e).sum()) < 1e-9, (e * e).sum() > .1), (True, True, True, True))
    c[4] = ("C", round(.6 * math.sqrt(18) / .8, 2), 3.18)
    c[5] = ("B", math.sqrt((100 * (1 - .64) / 18) / 50), .20, 1e-12)
    X = np.column_stack([np.ones(30), rng.normal(size=(30, 4))])
    H = X @ np.linalg.inv(X.T @ X) @ X.T
    c[6] = ("D", (round(np.trace(H), 9), round(np.trace(np.eye(30) - H), 9)), (5, 25))
    c[7] = ("A", tuple(np.round(np.linalg.solve([[2, 1], [1, 2]], [4, 5]), 9)), (1, 2))
    c[8] = ("C", math.sqrt(80 / 20 * .25), 1.0, 1e-12)
    c[10] = ("A", 1 - .2 * 20 / 16, .75, 1e-12)
    c[14] = ("B", 80 / 25, 3.2, 1e-12)
    c[16] = ("D", (2.5 / 1.0, round(stats.t.ppf(.975, 20), 3), 2.5 > 2.086), (2.5, 2.086, True))
    c[17] = ("A", (round(stats.t.ppf(.975, 16), 2), round(4 - 2.12 * .5, 2), round(4 + 2.12 * .5, 2)), (2.12, 2.94, 5.06))
    c[18] = ("C", (4 / 10, 4 * (1 + 1 / 10)), (.4, 4.4), 1e-12)
    c[19] = ("B", (.6 / 4) / (.4 / 20), 7.5, 1e-12)
    c[20] = ("D", (150 / 3) / (50 / 16), 16, 1e-12)
    c[22] = ("C", ((60 - 40) / 2) / (40 / 20), 5, 1e-12)
    c[23] = ("B", (2, 30 - 6), (2, 24))
    c[24] = ("D", round((30 / 3) / (90 / 34), 2), 3.78)
    # 25: weighted least squares with weights 1 / x^2 is the mean of the ratios
    xx = rng.uniform(1, 5, 12); yy = 2 * xx + xx * rng.normal(size=12)
    w = 1 / xx ** 2
    c[25] = ("A", (w * xx * yy).sum() / (w * xx * xx).sum(), (yy / xx).mean(), 1e-12)
    c[27] = ("B", (1 / (1 + 1 / 4), (1 + 4) / 4), (.8, 1.25), 1e-12)
    c[29] = ("A", (10 + 3, 2 + 1.5), (13, 3.5), 1e-12)
    c[31] = ("C", 1 / (1 - .9), 10, 1e-9)
    c[33] = ("D", math.sqrt(100 / .01), 100, 1e-9)
    c[35] = ("C", ((30 - 6) // 2 - 2, (80 / 10) / (20 / 10)), (10, 4.0))
    c[37] = ("D", 2 * (1 - .7), .6, 1e-12)
    c[38] = ("A", 3.0 > 4 - 1.2, True)
    c[40] = ("B", 1.28 / (1 - .36), 2.0, 1e-12)
    c[41] = ("D", (round(1 / (1 + math.exp(-(-2 + .5 * 6))), 3), round(1 / (1 + math.exp(1)), 3)), (.731, .269))
    c[42] = ("A", round(math.exp(.693), 1), 2.0)
    c[45] = ("D", 2 * 3 / (3 + 1), 1.5, 1e-12)
    xs = rng.normal(0, math.sqrt(3), 400000)
    c[46] = ("A", abs(np.polyfit(xs, 2 * xs + rng.normal(size=400000) + rng.normal(0, 2, 400000), 1)[0] - 2) < .02, True)
    c[47] = ("C", (6 / 4, 10 / 5), (1.5, 2.0), 1e-12)
    c[48] = ("B", (4 - 2) > (2 - 1), True)
    c[49] = ("D", ((1 - 0) == (2 - 1), (1 - 1) < (2 - 1)), (True, True))
    return c


def p2_unit07():
    from statsmodels.tsa.arima_process import ArmaProcess
    c = {}
    acf = lambda ar, ma, k=4: ArmaProcess(np.r_[1, -np.array(ar, float)], np.r_[1, np.array(ma, float)]).acf(k)
    t = np.arange(-2, 3); y = np.array([10, 12, 15, 17, 21])
    b, a = np.polyfit(t, y, 1)
    c[2] = ("D", a + 3 * b, 23.1, 1e-9)
    c[3] = ("A", 400 - 80 - 110 - 120, 90)
    c[4] = ("C", .3 * 30 + .7 * 20, 23, 1e-12)
    psd = lambda r1, r2: bool(np.all(np.linalg.eigvalsh([[1, r1, r2], [r1, 1, r1], [r2, r1, 1]]) > -1e-12))
    c[6] = ("D", (psd(.5, .25), psd(.4, 0), psd(-.5, .4), psd(.8, .1)), (True, True, True, False))
    c[7] = ("A", (.4 - .25) / .75, .2, 1e-12)
    c[8] = ("C", round(1.96 / 10, 3), .196)
    c[14] = ("A", (1 + .5) / (1 - .5), 3, 1e-12)
    psi = ArmaProcess([1, -.5], [1, .4]).arma2ma(3)
    c[15] = ("C", (psi[1], psi[2]), (.9, .45), 1e-12)
    c[16] = ("B", sum(.25 ** j for j in range(200)), 4 / 3, 1e-12)
    c[17] = ("D", acf([], [.5])[1], .4, 1e-12)
    c[18] = ("A", max(abs(th / (1 + th * th)) for th in np.linspace(-5, 5, 100001)), .5, 1e-9)
    c[19] = ("C", (acf([], [2])[1], acf([], [.5])[1], ArmaProcess([1], [1, 2]).isinvertible, ArmaProcess([1], [1, .5]).isinvertible),
             (.4, .4, False, True), 1e-12)
    r = acf([], [.5, .5])
    c[20] = ("B", (r[1], r[2], r[3]), (1 / 2, 1 / 3, 0), 1e-12)
    c[21] = ("A", (tuple(sorted(np.round(np.roots([.4, -1.3, 1]).real, 9))), ArmaProcess([1], [1, -1.3, .4]).isinvertible), ((1.25, 2.0), True))
    c[22] = ("D", (round(1 / (1 - .64), 2), acf([.8], [])[3]), (2.78, .512), 1e-9)
    stz = lambda p1, p2: bool(ArmaProcess([1, -p1, -p2], [1]).isstationary)
    c[23] = ("C", (stz(1.2, -.1), stz(.2, .9), stz(.5, .3), stz(-.5, .6)), (False, False, True, False))
    r = acf([.5, .3], [])
    c[24] = ("B", (round(r[1], 3), round(r[2], 3)), (.714, .657))
    c[25] = ("A", (stz(1, -.5), 1 + 4 * -.5 < 0), (True, True))
    c[26] = ("D", 5 / (1 - .5), 10, 1e-12)
    pac = ArmaProcess([1, -.5, -.3], [1]).pacf(4)
    c[27] = ("C", (round(pac[2], 9), round(pac[3], 9)), (.3, 0))
    c[28] = ("B", round(acf([.5], [.4])[1], 3), .692)
    c[29] = ("A", abs(acf([.5], [-.5])[1]) < 1e-12, True)
    P = ArmaProcess([1, -.5], [1, 2])
    c[30] = ("D", (bool(P.isstationary), bool(P.isinvertible)), (True, False))
    r = acf([.5], [.4])
    c[31] = ("C", (abs(r[2] - .5 * r[1]) < 1e-12, abs(r[1] - .5) > .1), (True, True))
    c[32] = ("A", tuple(np.round(np.linalg.solve([[1, .5], [.5, 1]], [.5, .4]), 9)), (.4, .2))
    c[33] = ("D", 4 * (1 - .25), 3, 1e-12)
    c[34] = ("B", 10 * (1 - .4 * .5 - .2 * .4), 7.2, 1e-12)
    c[37] = ("B", 20 - 1 - 1, 18)
    c[39] = ("C", 10 + .5 ** 2 * 2, 10.5, 1e-12)
    c[40] = ("A", 1 + .25, 1.25, 1e-12)
    c[41] = ("B", (1, 1 + .36), (1, 1.36), 1e-12)
    c[42] = ("D", 2 * math.sqrt(4), 4, 1e-12)
    c[43] = ("A", 4 / math.sqrt(4 * 9), 2 / 3, 1e-12)
    c[44] = ("C", tuple(np.round(np.polymul([1, -1], [1, -.5]), 9)), (1, -1.5, .5))
    c[45] = ("B", acf([], [-1])[1], -.5, 1e-12)
    f = lambda lam: abs(1 + .5 * np.exp(-1j * lam)) ** 2
    c[47] = ("C", f(0) / f(math.pi), 9, 1e-9)
    g = lambda lam: 1 / (1 - 2 * .6 * math.cos(lam) + .36)
    c[48] = ("A", g(0) > g(1) > g(2) > g(3), True)
    c[49] = ("B", integrate.quad(lambda lam: f(lam) / (2 * math.pi), -math.pi, math.pi)[0], 1.25, 1e-9)
    return c


def p2_unit08():
    c = {}
    A = np.array
    c[2] = ("D", (round(1 + 2 / 9 * 3, 2), round(4 - 4 / 9, 2)), (1.67, 3.56))
    S = A([[2, 1], [1, 3.]]); a = A([1, -1.])
    c[3] = ("A", (a @ [1, 2], a @ S @ a), (-1, 3), 1e-12)
    c[4] = ("C", (stats.chi2(3).mean(), stats.chi2(3).var()), (3, 6), 1e-12)
    c[5] = ("B", tuple(A([1, 1.]) @ A([[1, r], [r, 1]]) @ A([1, -1.]) for r in (-.7, 0, .4)), (0, 0, 0), 1e-12)
    c[7] = ("D", stats.multivariate_normal([0, 0], [[2, 1], [1, 2]]).pdf([0, 0]), 1 / (2 * math.pi * math.sqrt(3)), 1e-12)
    x = A([1, 1.])
    c[8] = ("C", round(x @ np.linalg.inv([[1, .5], [.5, 1]]) @ x, 2), 1.33)
    c[9] = ("B", 9 / 10, .9, 1e-12)
    c[12] = ("C", (4 / 5) ** 2, .64, 1e-12)
    d = A([[1, 2], [3, 4], [5, 9.]]); C = np.cov(d.T)
    c[13] = ("B", (C[0, 1], round(np.corrcoef(d.T)[0, 1], 3)), (7, .971), 1e-9)
    c[16] = ("C", A([1, 1.]) @ S @ A([1, 1.]) / 7, 1, 1e-12)
    c[17] = ("B", (10 * 2, 2 * 10 * 4), (20, 80))
    rng = np.random.default_rng(8)
    Sg = A([[2, .5], [.5, 1.]])
    W = stats.wishart(5, Sg).rvs(200000, random_state=rng)
    c[19] = ("D", abs(np.linalg.det(W).mean() / np.linalg.det(Sg) - 20) < .3, True)
    S3 = A([[2, .5, .2], [.5, 1, .1], [.2, .1, 1.5]]); av = A([1, -1, 2.])
    W3 = stats.wishart(10, S3).rvs(100000, random_state=rng)
    q = (av @ np.linalg.inv(S3) @ av) / np.einsum("i,nij,j->n", av, np.linalg.inv(W3), av)
    c[20] = ("C", stats.kstest(q, stats.chi2(8).cdf).pvalue > .001, True)
    r12, r13, r23 = .6, .5, .4
    c[22] = ("A", round((r12 - r13 * r23) / math.sqrt((1 - r13 ** 2) * (1 - r23 ** 2)), 3), .504)
    R2 = (r12 ** 2 + r13 ** 2 - 2 * r12 * r13 * r23) / (1 - r23 ** 2)
    c[23] = ("D", round(math.sqrt(R2), 3), .664)
    r132 = (r13 - r12 * r23) / math.sqrt((1 - r12 ** 2) * (1 - r23 ** 2))
    c[24] = ("C", 1 - R2, (1 - r12 ** 2) * (1 - r132 ** 2), 1e-12)
    c[25] = ("B", (round(.5 * math.sqrt(25) / math.sqrt(.75), 2), 28 - 3), (2.89, 25))
    c[26] = ("A", (.5 / 2) / (.5 / 20), 10, 1e-12)
    c[27] = ("D", (1 / math.sqrt(25), round(math.tanh(.693 - .392), 2), round(math.tanh(.693 + .392), 2)), (.2, .29, .80), 1e-12)
    Rm = A([[1, r12, r13], [r12, 1, r23], [r13, r23, 1]]); P = np.linalg.inv(Rm)
    c[28] = ("C", round(-P[0, 1] / math.sqrt(P[0, 0] * P[1, 1]), 3), .504)
    c[29] = ("B", F(20 - 3, 3 * 19), F(17, 57))
    T2 = 10 * A([1, 2.]) @ np.linalg.inv([[2, 0], [0, 4]]) @ A([1, 2.])
    c[30] = ("A", (T2, round(8 / 18 * T2, 2)), (15, 6.67), 1e-9)
    c[32] = ("C", (3, 10 + 10 - 3 - 1), (3, 16))
    c[33] = ("B", 10 * 15 / 25 * 2, 12, 1e-12)
    Sp = A([[2, 1], [1, 1.]]); dd = A([2, 1.])
    c[35] = ("D", tuple(np.round(np.linalg.solve(Sp, dd), 9)), (1, 0))
    c[36] = ("A", 3.5 > (4 + 2) / 2, True)
    c[37] = ("C", round(stats.norm.cdf(-1), 4), .1587)
    c[39] = ("D", dd @ np.linalg.solve(Sp, dd), 2, 1e-12)
    Sg = A([[5, 2], [2, 2.]]); lam, vec = np.linalg.eigh(Sg)
    c[40] = ("C", round(100 * lam[1] / lam.sum(), 1), 85.7)
    e = vec[:, 1] * np.sign(vec[0, 1])
    c[41] = ("A", tuple(np.round(e * math.sqrt(5), 9)), (2, 1))
    l2 = np.linalg.eigvalsh([[1, .6], [.6, 1]])
    c[42] = ("B", l2[1] / 2, .8, 1e-12)
    c[44] = ("C", round(e[0] * math.sqrt(lam[1]) / math.sqrt(5), 3), .980)
    l4 = np.linalg.eigvalsh(.5 * np.eye(4) + .5 * np.ones((4, 4)))
    c[45] = ("B", l4[-1] / 4, .625, 1e-12)
    c[46] = ("A", (sum(v > 1 for v in (2.8, 1.2, .6, .3, .1)), (2.8 + 1.2) / 5), (2, .8), 1e-12)
    c[47] = ("D", min(3, 5), 3)
    c[49] = ("B", round(math.sqrt(.36 + .09), 3), .671)
    return c


def p2_unit09():
    c = {}
    A = np.array
    P = A([[.7, .3], [.4, .6]]); pi0 = A([.5, .5])
    c[1] = ("B", (pi0 @ P @ P)[0], .565, 1e-12)
    c[2] = ("D", .5 * P[0, 1] * P[1, 1], .09, 1e-12)
    c[5] = ("B", (P @ P)[0, 1], .39, 1e-12)
    P4 = A([[.5, .5, 0, 0], [.5, .5, 0, 0], [0, 1 / 3, 1 / 3, 1 / 3], [0, 0, 0, 1]])
    Pn = np.linalg.matrix_power(P4, 200)
    c[6] = ("D", tuple(i + 1 for i in range(4) if Pn[i, i] < 1e-9), (3,))
    Q3 = A([[0, 1, 0], [.5, 0, .5], [0, 1, 0]])
    ret = [n for n in range(1, 13) if np.linalg.matrix_power(Q3, n)[0, 0] > 0]
    c[7] = ("A", math.gcd(*ret), 2)
    c[11] = ("D", 1 / .5, 2, 1e-12)
    h = np.linalg.solve([[1, -2 / 3], [-1 / 3, 1]], [0, 2 / 3])
    c[12] = ("C", (F(h[0]).limit_denominator(100), F(h[1]).limit_denominator(100)), (F(4, 7), F(6, 7)))
    B = A([[0, 1], [.5, .5]])
    c[13] = ("B", np.linalg.matrix_power(B, 3)[0, 0], .25, 1e-12)
    c[15] = ("D", tuple(np.linalg.matrix_power(P, 200)[1]), (4 / 7, 3 / 7), 1e-12)
    S = A([[0, 1], [1, 0.]])
    c[16] = ("C", tuple(sum(np.linalg.matrix_power(S, k) for k in range(1, 2001))[0] / 2000), (.5, .5), 1e-9)
    c[17] = ("A", (sorted(np.linalg.eigvals(P).real)[0], np.linalg.matrix_power(P, 2)[0, 0] - 4 / 7 - 3 / 7 * .09), (.3, 0), 1e-12)
    P3 = A([[.5, .5, 0], [.25, .5, .25], [0, .5, .5]])
    c[19] = ("C", tuple(np.linalg.matrix_power(P3, 500)[0]), (.25, .5, .25), 1e-9)
    c[21] = ("D", .2 / (.2 + .4), 1 / 3, 1e-12)
    st3 = A([.25, .5, .25])
    c[22] = ("B", tuple(st3 @ Q3), (.25, .5, .25), 1e-12)
    c[24] = ("A", 1 - 3 / 10, .7, 1e-12)
    c[25] = ("D", F(1 - 2, 1 - 8), F(1, 7))
    c[26] = ("B", 3 * 7, 21)
    c[27] = ("C", F(2, 3) ** 2, F(4, 9))
    c[28] = ("A", F(math.comb(4, 2), 16), F(3, 8))
    c[29] = ("D", (100 * .2, 100 * 4 * .6 * .4), (20, 96), 1e-9)
    c[30] = ("B", 1 - abs(.6 - .4), .8, 1e-12)
    import itertools
    fr = sum(1 for s in itertools.product([1, -1], repeat=4)
             if sum(s) == 0 and all(sum(s[:k]) != 0 for k in (1, 2, 3)))
    c[31] = ("C", F(fr, 16), F(1, 8))
    c[32] = ("A", round(stats.poisson(4).pmf(3), 3), .195)
    c[33] = ("D", stats.binom(2, 1 / 3).pmf(1), 4 / 9, 1e-12)
    c[34] = ("B", 2 / 5, .4, 1e-12)
    c[35] = ("C", round(math.exp(-2), 3), .135)
    c[36] = ("A", 2 * min(3, 5), 6)
    c[37] = ("D", (3 * 2 * 2, 3 * 2 * (1 + 4)), (12, 30))
    g = stats.gamma(3, scale=1 / 2)
    c[39] = ("C", (g.mean(), g.var()), (1.5, .75), 1e-12)
    c[40] = ("A", 10 * stats.beta(1, 4).mean(), 2, 1e-12)
    c[41] = ("B", round(stats.expon(scale=.5).sf(1) / stats.expon(scale=.5).sf(.5), 3), .368)
    c[42] = ("D", round(stats.poisson(1).sf(1), 3), .264)
    c[43] = ("C", (stats.geom(.5).mean(), math.exp(-math.log(2))), (2, .5), 1e-12)
    c[44] = ("A", 10 * math.exp(-math.log(2)), 5, 1e-12)
    c[45] = ("B", 1 / 2, .5, 1e-12)
    c[46] = ("D", round(stats.poisson(2).pmf(0), 3), .135)
    rho = .8
    c[47] = ("A", (rho / (1 - rho), 1 / (5 - 4) - 1 / 5, 4 * (1 / (5 - 4) - 1 / 5)), (4, .8, 3.2), 1e-9)
    c[48] = ("C", (rho ** 3, round(.2 * rho ** 3, 3)), (.512, .102), 1e-9)
    c[49] = ("B", round(math.exp(-(5 - 4) * 2), 3), .135)
    return c


def p2_unit10():
    # R is not run here: each R result is reproduced with the Python or numpy operation of the same definition.
    c = {}
    c[12] = ("A", (450 / 1000, round(50 / 450, 3)), (.45, .111))
    c[21] = ("C", (-7 // 2, -7 % 2), (-4, 1))
    c[22] = ("B", bool(np.isnan(np.float64(0) / np.float64(1) * np.nan)), True)
    c[23] = ("D", tuple(np.array([1, 2, 3, 4]) + np.tile([10, 20], 2)), (11, 22, 13, 24))
    c[24] = ("A", sum([2, 4, 6, 8][1:]), 18)
    m = np.arange(1, 7).reshape((2, 3), order="F")
    c[25] = ("B", (int(m[1, 2]), int(np.arange(1, 7).reshape(2, 3)[1, 0])), (6, 4))
    A = np.array([2, 1, 1, 3]).reshape((2, 2), order="F")
    c[26] = ("D", (int((A @ A)[0, 0]), int((A * A)[0, 0])), (5, 4))
    c[27] = ("A", (tuple(m.sum(1)), tuple(m.sum(0))), ((9, 12), (3, 7, 11)))
    c[28] = ("C", (bool(np.isnan(np.mean([1, 2, np.nan, 5]))), round(float(np.nanmean([1, 2, np.nan, 5])), 3)), (True, 2.667))
    c[29] = ("B", float(np.var([2, 4, 6], ddof=1)), 4.0)
    x = np.array([1, 5, 8, 3])
    c[30] = ("D", (int((x > 2).sum()), int(x[x > 2].sum())), (3, 16))
    s = 0
    for i in range(1, 6):
        if i % 2 == 0:
            continue
        s += i
    c[32] = ("C", s, 9)
    xx, n = 100, 0
    while xx > 1:
        xx /= 2; n += 1
    c[33] = ("B", n, 7)
    c[34] = ("D", tuple("H" if v > 2 else "L" for v in (1, 5, 3)), ("L", "H", "H"))
    c[35] = ("A", (tuple(range(2, 11, 3)), tuple(np.linspace(2, 10, 3))), ((2, 5, 8), (2, 6, 10)))
    c[36] = ("C", (tuple(np.repeat(["a", "b"], 2)), tuple(np.tile(["a", "b"], 2))), (("a", "a", "b", "b"), ("a", "b", "a", "b")))
    v = np.array([30, 10, 20])
    c[37] = ("B", (tuple(np.argsort(v) + 1), tuple(int(r) for r in stats.rankdata(v))), ((2, 3, 1), (3, 1, 2)))
    c[38] = ("D", ("statistics"[2:6], len("statistics")), ("atis", 10))
    lev = sorted(set("babc"))
    c[39] = ("A", tuple(lev.index(ch) + 1 for ch in "babc"), (2, 1, 2, 3))
    c[41] = ("B", (round(2.5), round(3.5)), (2, 4))
    c[43] = ("C", ((10 + 30) / 2, (20 + 40) / 2), (20, 30))
    f = lambda x, y=2: x ** y
    c[45] = ("A", (f(3), f(y=3, x=2)), (9, 8))
    c[47] = ("B", tuple(i ** 2 for i in (1, 2, 3)), (1, 4, 9))
    return c


def p1_unit01():
    c = {}
    c[47] = ("B", ((4 * 9 + 3 * 7 + 3 * 10) / 10, round((9 + 7 + 10) / 3, 2)), (8.7, 8.67), 1e-12)
    c[48] = ("A", (20 * 7.5 + 30 * 8.5) / 50, 8.1, 1e-12)
    c[49] = ("D", 3 * 1 + 4 / 2, 5, 1e-12)
    return c


def p1_unit05():
    c = {}
    A = lambda ch: ord(ch) - 64
    L = lambda k: chr(64 + k)
    c[7] = ("D", 79 * 2 + 1, 159)
    c[8] = ("C", 6 ** 2 + 1, 37)
    c[9] = ("A", 13 + 21, 34)
    c[10] = ("B", 360 * 6, 2160)
    c[11] = ("D", 16 - 2, 14)
    c[12] = ("C", [k * (k + 1) for k in range(1, 8)], [2, 6, 12, 20, 30, 42, 56])
    c[13] = ("A", 6 ** 3 - 1, 215)
    c[14] = ("B", 13 ** 2, 169)
    c[15] = ("D", L(15 + 6), "U")
    c[16] = ("A", L(A("G") + 2) + L(A("T") - 2), "IR")
    c[17] = ("C", L(11 + 5) + str(11 + 5), "P16")
    c[18] = ("B", L(14 - 6), "H")
    c[19] = ("D", ("".join(L(A(x) + 1) for x in "MIND"), "".join(L(A(x) + 1) for x in "BOOK")), ("NJOE", "CPPL"))
    c[20] = ("A", ("".join(L(27 - A(x)) for x in "RAT"), "".join(L(27 - A(x)) for x in "DOG")), ("IZG", "WLT"))
    c[21] = ("C", (sum(map(A, "BAD")), sum(map(A, "FACE"))), (7, 15))
    c[23] = ("D", 8 * 6 / 3 - 4 + 2, 14, 1e-12)
    c[27] = ("D", (10 - 2, 6, math.hypot(8, 6)), (8, 6, 10))
    c[30] = ("B", 40 - 15 + 1, 26)
    fr = [F(3, 5), F(5, 8), F(7, 11), F(2, 3)]
    c[31] = ("D", sorted(fr), fr)
    c[32] = ("A", (200 + 300) / (90 * 5 / 18), 20, 1e-12)
    c[33] = ("C", 2 * 30 * 60 / 90, 40, 1e-12)
    c[34] = ("B", 300 / ((54 + 36) * 5 / 18), 12, 1e-12)
    c[35] = ("D", (F(9, 12), F(12, 14)), (F(3, 4), F(6, 7)))
    c[36] = ("A", 1.25 * .8, 1.0, 1e-12)
    c[37] = ("C", 60 / 160 * 100, 37.5, 1e-12)
    c[38] = ("B", 20000 * 1.1 * 1.2, 26400, 1e-6)
    c[39] = ("D", (500 * 1.4 * .9 - 500) / 500 * 100, 26, 1e-9)
    c[40] = ("A", (15 / 12 - 1) * 100, 25, 1e-9)
    c[41] = ("C", 60 / .15, 400, 1e-9)
    c[42] = ("B", 100 / 8, 12.5, 1e-12)
    c[43] = ("D", (12000 * (1.05 ** 2 - 1) - 12000 * .05 * 2, 12000 * .05 ** 2), (30, 30), 1e-9)
    c[44] = ("A", 5000 * 1.1 ** 3 - 5000, 1655, 1e-9)
    c[45] = ("C", (12100 / 1.1 ** 2, 12100 - 12100 / 1.1 ** 2), (10000, 2100), 1e-9)
    c[46] = ("B", (150 - 24 + 14) / 10, 14, 1e-12)
    c[47] = ("D", (40 * 50 + 60 * 60) / 100, 56, 1e-12)
    c[48] = ("A", (150 + 6) / 6, 26, 1e-12)
    c[49] = ("C", 6 * 10 / 4, 15, 1e-12)
    c[50] = ("B", (120 + 20) / .35, 400, 1e-9)
    return c


UNITS = {(k[:2], int(k[-2:])): v for k, v in sorted(globals().items()) if re.fullmatch(r"p[12]_unit\d\d", k)}


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
