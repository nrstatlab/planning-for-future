# Practical 8 -- fit Binomial, Poisson and Negative Binomial to ONE data set
# and let the goodness-of-fit test choose between them
import math
from tails import chi2_upper

# Step 1: Enter the data; the mean, the variance and their ratio
x = [0, 1, 2, 3, 4, 5]
f = [447, 132, 42, 21, 3, 2]
n = sum(f)
mean = sum(xi * fi for xi, fi in zip(x, f)) / n
var = sum(fi * (xi - mean) ** 2 for xi, fi in zip(x, f)) / n
print(f"n = {n}   mean = {mean:.6f}   variance = {var:.6f}   var/mean = {var/mean:.6f}")

# Step 2: The three probability functions
def C(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

def binomial_pmf(N, p, k):
    return C(N, k) * p ** k * (1 - p) ** (N - k)

def poisson_pmf(lam, k):
    return math.exp(-lam) * lam ** k / math.factorial(k)

def nbinom_pmf(r, p, k):
    # P(X = k) = Gamma(r+k)/(k! Gamma(r)) p^r (1-p)^k
    coef = 1.0
    for i in range(k):
        coef *= (r + i) / (i + 1)
    return coef * p ** r * (1 - p) ** k

# Step 3: Estimate the parameters
N = 5
p_bin = mean / N
lam = mean
p_nb = mean / var
r_nb = mean ** 2 / (var - mean)
print(f"Binomial  N = {N}, p = {p_bin:.6f}     (p estimated by the method of moments)")
print(f"Poisson   lambda = {lam:.6f}")
print(f"NegBin    r = {r_nb:.6f}, p = {p_nb:.6f}")

# Step 4: Expected frequencies
fits = {
    "Binomial": [n * binomial_pmf(N, p_bin, k) for k in x],
    "Poisson": [n * poisson_pmf(lam, k) for k in x],
    "NegBin": [n * nbinom_pmf(r_nb, p_nb, k) for k in x],
}
# the tail beyond k = 5 belongs to the last class for the two unbounded fits
for name in ("Poisson", "NegBin"):
    fits[name][-1] = n - sum(fits[name][:-1])

print()
print("  k   observed   Binomial    Poisson     NegBin")
for i, k in enumerate(x):
    print(f"  {k}   {f[i]:8d}   {fits['Binomial'][i]:8.2f}   "
          f"{fits['Poisson'][i]:8.2f}   {fits['NegBin'][i]:8.2f}")

# Step 5: Pool the tail, then chi-square
def pooled_chi2(obs, exp, params):
    """Pool the upper tail until every expected frequency is at least 5."""
    o, e = list(obs), list(exp)
    while len(e) > 2 and e[-1] < 5:
        last_e, last_o = e.pop(), o.pop()
        e[-1] += last_e
        o[-1] += last_o
    chi2 = sum((oi - ei) ** 2 / ei for oi, ei in zip(o, e))
    df = len(e) - 1 - params
    return chi2, df, len(e)

print()
# Step 6: The test for each fit
for name, params in (("Binomial", 1), ("Poisson", 1), ("NegBin", 2)):
    chi2, df, k = pooled_chi2(f, fits[name], params)
    print(f"{name:9s} chi-square {chi2:9.4f} on {df} df "
          f"({k} classes after pooling, {params} parameter(s) estimated)")

for name, params in (("Binomial", 1), ("Poisson", 1), ("NegBin", 2)):
    chi2, df, _ = pooled_chi2(f, fits[name], params)
    print(f"{name:9s} p-value {chi2_upper(chi2, df):.4g}")

# Step 7: Draw the comparison with characters
# the "curve plot", drawn with characters since no plotting package is allowed
print()
print("observed (#) against the negative binomial fit (o), one column per count")
scale = 460 / 46
for i, k in enumerate(x):
    bar = "#" * max(1, round(f[i] / scale))
    fit = round(fits["NegBin"][i] / scale)
    print(f"  {k}  {bar:<48s}| fit {'o' * max(1, fit)}")
