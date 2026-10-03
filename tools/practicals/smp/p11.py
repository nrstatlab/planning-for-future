# Practical 11 -- tests for means, variances and correlations,
# with every tail area taken from tails.py rather than from a table
import math
from tails import t_two_sided, F_upper, chi2_upper, normal_two_sided

# Step 1: Size, mean and variance (n - 1 divisor)
def stats(a):
    n = len(a)
    m = sum(a) / n
    s2 = sum((v - m) ** 2 for v in a) / (n - 1)
    return n, m, s2

# Step 2: One-sample t
sample = [48, 52, 55, 49, 53, 51, 47, 54, 50, 52, 56, 50]
n1, m1, s21 = stats(sample)
mu0 = 50
t1 = (m1 - mu0) / math.sqrt(s21 / n1)
print(f"one-sample t : n {n1}  mean {m1:.6f}  s^2 {s21:.6f}")
print(f"   H0: mu = {mu0}    t = {t1:.6f} on {n1-1} df   p = {t_two_sided(t1, n1-1):.6f}")

# Step 3: Two independent samples, pooled variance
A = [23, 27, 25, 29, 24, 26, 28]
B = [31, 28, 33, 30, 35, 29]
na, ma, s2a = stats(A)
nb, mb, s2b = stats(B)
sp2 = ((na - 1) * s2a + (nb - 1) * s2b) / (na + nb - 2)
t2 = (ma - mb) / math.sqrt(sp2 * (1 / na + 1 / nb))
print(f"two-sample t : means {ma:.6f} and {mb:.6f}   pooled s^2 {sp2:.6f}")
print(f"   t = {t2:.6f} on {na+nb-2} df   p = {t_two_sided(t2, na+nb-2):.6f}")

# Step 4: Paired t
before = [72, 68, 75, 70, 66, 74, 69, 71]
after = [70, 65, 71, 68, 65, 70, 67, 69]
d = [b - a for b, a in zip(before, after)]
nd, md, s2d = stats(d)
t3 = md / math.sqrt(s2d / nd)
print(f"paired t     : differences {d}")
print(f"   mean d {md:.6f}   t = {t3:.6f} on {nd-1} df   p = {t_two_sided(t3, nd-1):.8f}")

# Step 5: One variance against a stated value
sigma0_sq = 6.0
chi = (n1 - 1) * s21 / sigma0_sq
p_lo, p_hi = 1 - chi2_upper(chi, n1 - 1), chi2_upper(chi, n1 - 1)
print(f"one variance : H0 sigma^2 = {sigma0_sq}   chi-square = {chi:.6f} on {n1-1} df")
print(f"   two-sided p = {2*min(p_lo, p_hi):.6f}")

# Step 6: Two variances
F = max(s2a, s2b) / min(s2a, s2b)
df1, df2 = (na - 1, nb - 1) if s2a > s2b else (nb - 1, na - 1)
print(f"two variances: s^2 {s2a:.6f} and {s2b:.6f}   F = {F:.6f} on ({df1}, {df2}) df")
print(f"   two-sided p = {2*F_upper(F, df1, df2):.6f}  -- pooling was justified")

# Step 7: A correlation against zero
x = [65, 63, 67, 64, 68, 62, 70, 66, 68, 67]
y = [68, 66, 68, 65, 69, 66, 68, 65, 71, 67]
nx = len(x)
xb, yb = sum(x) / nx, sum(y) / nx
Sxx = sum((v - xb) ** 2 for v in x)
Syy = sum((v - yb) ** 2 for v in y)
Sxy = sum((u - xb) * (v - yb) for u, v in zip(x, y))
r = Sxy / math.sqrt(Sxx * Syy)
tr = r * math.sqrt((nx - 2) / (1 - r * r))
print(f"correlation  : r = {r:.6f}   t = {tr:.6f} on {nx-2} df   "
      f"p = {t_two_sided(tr, nx-2):.6f}")

# Step 8: A correlation against a stated non-zero value, by Fisher's z
rho0 = 0.8
z = 0.5 * math.log((1 + r) / (1 - r))
z0 = 0.5 * math.log((1 + rho0) / (1 - rho0))
zstat = (z - z0) * math.sqrt(nx - 3)
print(f"   Fisher z = {z:.6f}, z0 = {z0:.6f}   test statistic {zstat:.6f}   "
      f"p = {normal_two_sided(zstat):.6f}")
