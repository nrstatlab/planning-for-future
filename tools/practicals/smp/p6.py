# Practical 6 -- the first four raw and central moments, skewness and kurtosis
import math

# Step 1: Raw moments
def raw_moments(x, k=4):
    n = len(x)
    return [sum(v ** r for v in x) / n for r in range(1, k + 1)]

# Step 2: Central moments from the raw moments
def central_from_raw(m):
    m1, m2, m3, m4 = m
    mu2 = m2 - m1 ** 2
    mu3 = m3 - 3 * m1 * m2 + 2 * m1 ** 3
    mu4 = m4 - 4 * m1 * m3 + 6 * m1 ** 2 * m2 - 3 * m1 ** 4
    return [0.0, mu2, mu3, mu4]

# Step 3: Central moments directly, as a check
def central_direct(x):
    n = len(x)
    xb = sum(x) / n
    return [0.0] + [sum((v - xb) ** r for v in x) / n for r in (2, 3, 4)]

# Step 4: Compute both ways and compare
x = [12, 15, 11, 18, 22, 14, 16, 19, 13, 25, 17, 20, 14, 16, 21]
m = raw_moments(x)
print("raw moments      m1..m4 :", "  ".join(f"{v:.4f}" for v in m))
c = central_from_raw(m)
d = central_direct(x)
print("central, from raw moments:", "  ".join(f"{v:.4f}" for v in c[1:]))
print("central, computed direct :", "  ".join(f"{v:.4f}" for v in d[1:]))
print("agree to within 1e-8      :", max(abs(a - b) for a, b in zip(c, d)) < 1e-8)

# Step 5: Skewness and kurtosis
mu2, mu3, mu4 = c[1], c[2], c[3]
b1 = mu3 ** 2 / mu2 ** 3
g1 = mu3 / mu2 ** 1.5
b2 = mu4 / mu2 ** 2
g2 = b2 - 3
print(f"beta1 {b1:.6f}   gamma1 {g1:+.6f}   beta2 {b2:.6f}   gamma2 {g2:+.6f}")
print("skew  :", "positive -- the long tail is to the right" if g1 > 0 else "negative")
print("kurt  :", "platykurtic -- flatter than normal" if g2 < 0 else "leptokurtic")
print("sd    :", f"{math.sqrt(mu2):.6f}")
