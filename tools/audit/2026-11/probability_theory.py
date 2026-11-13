#!/usr/bin/env python3
"""Recompute the worked numbers of Probability Theory (content check, November 2026)."""
from fractions import Fraction as Fr
import math
from scipy import stats

ok = lambda a, b, tol=6e-7: abs(a - b) <= tol

# Unit 2, Example 2.1
p = {(0, 0): Fr(10, 100), (1, 0): Fr(10, 100), (2, 0): Fr(5, 100),
     (0, 1): Fr(15, 100), (1, 1): Fr(20, 100), (2, 1): Fr(10, 100),
     (0, 2): Fr(5, 100), (1, 2): Fr(15, 100), (2, 2): Fr(10, 100)}
py = {y: sum(p[x, y] for x in range(3)) for y in range(3)}
EX = sum(x * v for (x, y), v in p.items()); EX2 = sum(x * x * v for (x, y), v in p.items())
m = {y: sum(x * p[x, y] for x in range(3)) / py[y] for y in range(3)}
v = {y: sum(x * x * p[x, y] for x in range(3)) / py[y] - m[y] ** 2 for y in range(3)}
assert (m[0], m[1], m[2]) == (Fr(4, 5), Fr(8, 9), Fr(7, 6)) and (v[1], v[2]) == (Fr(44, 81), Fr(17, 36))
within = sum(v[y] * py[y] for y in range(3)); between = sum((m[y] - EX) ** 2 * py[y] for y in range(3))
assert within == Fr(947, 1800) and between == Fr(77, 3600) and within + between == EX2 - EX ** 2 == Fr(219, 400)
# Example 2.4
assert ok(math.exp(-4), 0.0183156, 6e-8) and ok(stats.poisson.sf(7, 4), 0.0511336, 6e-8)
assert ok(0.25 / (math.exp(-4) + stats.poisson.sf(7, 4)), 3.600, 6e-4)
# Example 2.5
for r, val in ((1, 2.166667), (2, 2.798809), (3, 3.396035), (4, 3.859284)):
    assert ok(float(Fr(1, 2) + Fr(2 ** r, 3) + Fr(6 ** r, 6)) ** (1 / r), val)
assert Fr(1, 2) + Fr(1, 6) + Fr(1, 36) == Fr(25, 36)
# Unit 3
assert ok(2 * stats.norm.sf(0.5), 0.617075)
tail = lambda m_: math.pi ** 2 / 6 - sum(1 / n ** 2 for n in range(1, m_))
assert ok(tail(10), 0.10517, 6e-6) and ok(tail(100), 0.01005, 6e-6) and ok(tail(1000), 0.00100, 6e-6)
assert ok(sum(1 / n ** 2 for n in range(1, 4001)), 1.644684)
assert ok(sum(1 / n for n in range(1, 4001)), 8.871390) and ok(sum(1 / n for n in range(1, 40001)), 11.173863)
# Unit 4
for n, val in ((100, 0.0671463), (10 ** 4, 0.0066672), (10 ** 6, 0.0006667)):
    assert ok(sum(math.sqrt(k) for k in range(1, n + 1)) / n ** 2, val, 6e-8)
ex = stats.binom.sf(59, 100, 0.5)
assert ok(ex, 0.0284440, 6e-8) and ok(stats.norm.sf(2), 0.0227501, 6e-8) and ok(stats.norm.sf(1.9), 0.0287166, 6e-8)
assert ok(stats.norm.cdf(2) - stats.norm.cdf(-1.5), 0.910443)
print("probability-theory: all recomputed values agree")
