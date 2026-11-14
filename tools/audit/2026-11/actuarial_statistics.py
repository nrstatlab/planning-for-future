#!/usr/bin/env python3
"""Recompute the worked numbers of Actuarial Statistics (content check, November 2026)."""
import math
from scipy import stats

ok = lambda a, b, tol=6e-4: abs(a - b) <= tol * max(1, abs(b))
# Unit 1
assert ok(math.log(.1 * math.exp(.05) + .9) / 1e-6, 5114) and ok(1e5 * (1 - .6 ** .25), 11989)
# Unit 2
assert ok(math.log(.9 + .1 * math.e) / 1e-4, 1586) and ok(math.sqrt(1.996e10), 141280, 1e-4)
assert ok(stats.binom.sf(3, 1000, .002), 0.143, 2e-3) and ok(math.sqrt(2.82e8), 16793, 1e-4)
k = 15000 / 16793; assert ok(16793 * stats.norm.pdf(k) - 15000 * stats.norm.sf(k), 1710, 3e-3)
# Unit 3
assert ok(1.1 ** 50, 117.4, 1e-3) and ok(1.1 ** 70, 789.7, 1e-3) and ok(.995 ** .5, 0.99749, 1e-5)
# Unit 4
assert ok(1 / 6 - (2 / 7) ** 2, 0.0850, 1e-3) and ok((.001 + .999 * .105) / 1.05, 0.1009, 1e-3)
t = (2 / 7) * (1 - math.exp(-1.4)); assert ok(t, 0.2153, 1e-3) and ok(t + math.exp(-1.4), 0.4619, 1e-3)
# Unit 5
i = math.exp(.05) - 1; d = 1 - math.exp(-.05); assert ok((1 - (.05 / i) * (2 / 7)) / d, 14.79, 1e-3)
assert ok(.15 / 17.85, 0.008403, 1e-4) and ok(.15 / (17.85 - 11 / 24), 0.008625, 1e-4)
A = 1 - (.06 / 1.06) * 11.9; assert ok(A, 0.3264, 1e-3) and ok(5e5 * A / 11.9, 13715, 1e-3)
# Practical
assert ok(2e5 * (1 - .75 ** .2), 11183, 1e-4) and ok(math.log(.8 + .2 * math.e) / 2e-5, 14770, 1e-4)
assert ok(stats.norm.sf(50000 / math.sqrt(4e9)), 0.215, 2e-3) and ok(stats.norm.sf(1e5 / math.sqrt(5e9)), 0.079, 5e-3)
assert ok(2e5 + 1.645 * math.sqrt(1.98e10), 431472, 1e-5) and ok(stats.binom.cdf(4, 200, .01), 0.948, 1e-3) and ok(stats.binom.cdf(5, 200, .01), 0.984, 1e-3)
assert ok(math.exp(-1) / 1.2, 0.307, 1e-3) and ok(math.exp(-10 / 3) / 1.2, 0.030, 1e-2)
assert ok((1 - 1.06 ** -20) / .06, 11.4699, 1e-5) and ok(6 ** .05, 1.0937, 1e-4) and ok(.005 / 6 ** 2.5, 5.67e-5, 1e-3)
for f, a, p in ((.105, 18.8, 5585), (.029, 12.93, 2243), (.384, 12.93, 29698), (.105, 7.87, 13342)):
    assert ok(1e6 * f / a, p, 1e-4)
print("actuarial-statistics: all recomputed values agree")
