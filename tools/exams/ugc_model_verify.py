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


UNITS = {("p2", 1): p2_unit01}


def same(a, b, tol):
    if isinstance(a, tuple):
        return len(a) == len(b) and all(same(x, y, tol) for x, y in zip(a, b))
    if tol is None or isinstance(a, (bool, np.bool_)):
        return a == b
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
