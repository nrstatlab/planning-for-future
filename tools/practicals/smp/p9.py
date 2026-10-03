# Practical 9 -- fit Normal, Exponential and Cauchy to the same grouped data
import math
from tails import chi2_upper

# Step 1: Enter the grouped data; the mean and the sd
edges = [10, 20, 30, 40, 50, 60, 70, 80]
obs = [9, 15, 37, 55, 36, 17, 6]
n = sum(obs)
mids = [(edges[i] + edges[i + 1]) / 2 for i in range(len(obs))]

mean = sum(m * f for m, f in zip(mids, obs)) / n
var = sum(f * (m - mean) ** 2 for m, f in zip(mids, obs)) / n
sd = math.sqrt(var)
print(f"n = {n}   mean = {mean:.6f}   sd = {sd:.6f}")

# Step 2: Quartiles by interpolation, for the Cauchy
def quantile(q):
    """The q-quantile of the grouped distribution, by linear interpolation."""
    target, cum = q * n, 0
    for i, f in enumerate(obs):
        if cum + f >= target:
            return edges[i] + (target - cum) / f * (edges[i + 1] - edges[i])
        cum += f

med = quantile(0.5)
q1, q3 = quantile(0.25), quantile(0.75)
gamma = (q3 - q1) / 2
print(f"median = {med:.6f}   Q1 = {q1:.6f}   Q3 = {q3:.6f}   half-IQR = {gamma:.6f}")

# Step 3: The three distribution functions
def normal_cdf(x, mu, s):
    return 0.5 * (1 + math.erf((x - mu) / (s * math.sqrt(2))))

def expon_cdf(x, lam):
    return 0.0 if x <= 0 else 1 - math.exp(-lam * x)

def cauchy_cdf(x, x0, g):
    return 0.5 + math.atan((x - x0) / g) / math.pi

# Step 4: The estimates
lam = 1 / mean
print(f"Normal    mu = {mean:.6f}, sigma = {sd:.6f}   (moment estimates)")
print(f"Exponent  lambda = 1/mean = {lam:.6f}")
print(f"Cauchy    x0 = median = {med:.6f}, gamma = half-IQR = {gamma:.6f}")
print("  -- the Cauchy has no mean or variance, so it cannot be fitted by moments;")
print("     the median and the half-interquartile range are the natural substitutes.")

# Step 5: Expected frequencies from the distribution function
def expected(cdf, *args):
    """Expected frequencies, with the two outer classes opened to +-infinity
    so that the probabilities sum to exactly 1."""
    e = []
    for i in range(len(obs)):
        lo = 0.0 if i == 0 else cdf(edges[i], *args)
        hi = 1.0 if i == len(obs) - 1 else cdf(edges[i + 1], *args)
        e.append(n * (hi - lo))
    return e

fits = {
    "Normal": expected(normal_cdf, mean, sd),
    "Exponential": expected(expon_cdf, lam),
    "Cauchy": expected(cauchy_cdf, med, gamma),
}

print()
print("  class      observed    Normal   Exponential    Cauchy")
for i in range(len(obs)):
    print(f"  {edges[i]:2d} - {edges[i+1]:2d}   {obs[i]:8d}  {fits['Normal'][i]:9.2f}  "
          f"{fits['Exponential'][i]:11.2f}  {fits['Cauchy'][i]:8.2f}")

print()
# Step 6: Chi-square for each fit
for name, params in (("Normal", 2), ("Exponential", 1), ("Cauchy", 2)):
    e = fits[name]
    chi2 = sum((o - ei) ** 2 / ei for o, ei in zip(obs, e))
    df = len(obs) - 1 - params
    print(f"{name:12s} chi-square {chi2:10.4f} on {df} df   p = {chi2_upper(chi2, df):.4g}")
