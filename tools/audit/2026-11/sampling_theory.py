#!/usr/bin/env python3
"""Recompute the worked numbers of Sampling Theory (content check, November 2026)."""
from fractions import Fraction as Fr
from itertools import combinations
import math

ok = lambda a, b, tol=6e-7: abs(float(a) - b) <= tol

# Unit 1, Example 1.1
X = [10, 20, 30, 25, 15]; Y = [12, 26, 33, 30, 19]; p = [Fr(x, 100) for x in X]
V = sum(pi * (y / pi - 120) ** 2 for pi, y in zip(p, Y)); assert V / 2 == Fr(85, 3)
assert ok(725 / (V / 2), 25.588235)
# Example 1.3
p = [Fr(1, 10), Fr(2, 10), Fr(3, 10), Fr(4, 10)]; Y = [3, 6, 9, 12]
pij = {(i, j): p[i] * p[j] / (1 - p[i]) + p[j] * p[i] / (1 - p[j]) for i, j in combinations(range(4), 2)}
pi_ = [sum(v for k, v in pij.items() if i in k) for i in range(4)]
assert pi_ == [Fr(197, 840), Fr(139, 315), Fr(73, 120), Fr(451, 630)] and sum(pij.values()) == 1
assert pij[0, 1] == Fr(17, 360) and pij[2, 3] == Fr(13, 35)
yg = sum((pi_[i] * pi_[j] - pij[i, j]) * (Y[i] / pi_[i] - Y[j] / pi_[j]) ** 2 for i, j in pij)
est = {k: Y[k[0]] / pi_[k[0]] + Y[k[1]] / pi_[k[1]] for k in pij}
E = sum(pij[k] * est[k] for k in pij); Var = sum(pij[k] * est[k] ** 2 for k in pij) - E ** 2
assert E == 30 and Var == yg and ok(yg, 2.428334) and ok(est[1, 3], 30.3599, 6e-5)
# Unit 2, Example 2.1
x = [10, 12, 15, 9, 14]; y = [9, 11, 14, 8, 13]
ests = [Fr(y[i] + y[j], x[i] + x[j]) * 12 for i, j in combinations(range(5), 2)]
E = sum(ests) / 10; assert ok(E, 10.986005) and ok(E - 11, -0.013995)
R = Fr(11, 12); S = Fr(13, 2)
assert ok(Fr(3, 5) / 24 * (R * S - S), -0.013542) and ok(math.sqrt(Fr(3, 10) * (S + R * R * S - 2 * R * S)), 0.116369)
# Example 2.2
assert Fr(1, 3) * Fr(12, 5) * Fr(11, 2) + Fr(2, 3) * Fr(26, 16) * 17 == Fr(1369, 60)
assert Fr(64, 37) * Fr(79, 6) == Fr(2528, 111)
# Unit 3, Example 3.1
cl = [[4, 6, 5], [10, 12, 11], [7, 9, 8], [13, 15, 14]]; allv = [v for c in cl for v in c]; g = Fr(sum(allv), 12)
S2 = sum((v - g) ** 2 for v in allv) / 11
num = sum((c[j] - g) * (c[k] - g) for c in cl for j in range(3) for k in range(3) if j != k)
rho = num / (2 * 11 * S2); assert S2 == 13 and rho == Fr(131, 143)
assert (1 + 2 * rho) * Fr(11, 9) == Fr(45, 13)
assert ok(math.sqrt(8 * (1 - rho) / rho), 0.856, 6e-4)
# Unit 4: unequal first-stage units, enumeration
psu = [[4, 6], [5, 7, 9], [8, 10, 12, 14]]; M = [2, 3, 4]; M0 = 9
samples = []  # (probability, expansion estimate of the mean, ratio-to-size estimate)
for a, b in combinations(range(3), 2):
    sa = list(combinations(psu[a], 2)); sb = list(combinations(psu[b], 2))
    for u in sa:
        for w in sb:
            pr = Fr(1, 3) / (len(sa) * len(sb))
            ta = M[a] * Fr(sum(u), 2); tb = M[b] * Fr(sum(w), 2)
            samples.append((pr, Fr(3, 2) * (ta + tb) / M0, (ta + tb) / (M[a] + M[b])))
assert len(samples) == 27 and sum(s[0] for s in samples) == 1
E = sum(s[0] * s[1] for s in samples); Var = sum(s[0] * s[1] ** 2 for s in samples) - E ** 2
assert E == Fr(75, 9) and Var == Fr(1001, 162)
Er = sum(s[0] * s[2] for s in samples); print("ratio-to-size mean", Er, float(Er), float(Er - Fr(75, 9)))
# Example 4.2 to 4.4
assert ok(math.sqrt(.37 * .63 / 64), 0.060351) and ok(math.sqrt(.175 * .825 / 400), 0.018998)
for P, se in ((.6, 0.123939), (.8, 0.038367), (.9, 0.026693)):
    lam = P * .175 + (1 - P) * .825; assert ok(math.sqrt(lam * (1 - lam) / (400 * (2 * P - 1) ** 2)), se)
w = .13 / 1.255; assert ok(w, 0.103586) and ok(w * w * 1.125 + (1 - w) ** 2 * .13, 0.116534)
print("sampling-theory units: all recomputed values agree")
