"""Course 4 Lab, experiments 8-11: random variables, expectation and variance,
and the discrete and continuous probability distributions.

Excel equivalents are named against each section, since the prescribed lab is
a spreadsheet lab (see ../excel-walkthroughs.md).
"""

import random
import statlib as S

random.seed(42)          # reproducible output

print("=" * 66)
print("EXPERIMENT 8: Simulating discrete and continuous random variables")
print("=" * 66)

print("\nDISCRETE -- rolling a fair die 1000 times")
rolls = [random.randint(1, 6) for _ in range(1000)]
print(f"{'Face':<8}{'Observed':<12}{'Expected':<12}Frequency")
for face in range(1, 7):
    observed = rolls.count(face)
    print(f"{face:<8}{observed:<12}{1000/6:<12.1f}{'#' * (observed // 10)}")
print(f"  Excel: =RANDBETWEEN(1,6), then COUNTIF to tally")

print("\nCONTINUOUS -- 1000 draws from Normal(mean 100, sd 15)")
sample = [random.gauss(100, 15) for _ in range(1000)]
sample_mean = sum(sample) / len(sample)
sample_var = sum((x - sample_mean) ** 2 for x in sample) / (len(sample) - 1)
print(f"  sample mean = {sample_mean:.2f}   (population mean 100)")
print(f"  sample sd   = {sample_var ** 0.5:.2f}   (population sd 15)")
print("  Excel: =NORM.INV(RAND(), 100, 15)")

print("\n" + "=" * 66)
print("EXPERIMENT 9: Expectation and variance from a probability distribution")
print("=" * 66)

# A discrete random variable given by its PMF.
values = [0, 1, 2, 3, 4]
probs = [0.10, 0.25, 0.30, 0.25, 0.10]

print(f"\n{'x':<8}{'P(x)':<10}{'x.P(x)':<12}{'x^2.P(x)':<12}")
print("-" * 42)
expectation = 0.0
second_moment = 0.0
for x, p in zip(values, probs):
    expectation += x * p
    second_moment += x * x * p
    print(f"{x:<8}{p:<10.2f}{x * p:<12.3f}{x * x * p:<12.3f}")
print("-" * 42)
print(f"{'Sum':<8}{sum(probs):<10.2f}{expectation:<12.3f}{second_moment:<12.3f}")

variance = second_moment - expectation ** 2
print(f"\n  E(X)   = sum of x.P(x)          = {expectation:.3f}")
print(f"  E(X^2) = sum of x^2.P(x)        = {second_moment:.3f}")
print(f"  Var(X) = E(X^2) - [E(X)]^2      = {second_moment:.3f} - "
      f"{expectation:.3f}^2 = {variance:.3f}")
print(f"  SD(X)  = sqrt(Var(X))           = {variance ** 0.5:.3f}")
print("\n  The shortcut Var(X) = E(X^2) - [E(X)]^2 is quicker in an exam than")
print("  computing E[(X - mu)^2] term by term, and gives the same answer.")
print("  Check that the probabilities sum to 1 first -- if they do not, the")
print("  question is misread or mistyped.")

print("\n" + "=" * 66)
print("EXPERIMENT 10: Discrete distributions -- Binomial and Poisson")
print("=" * 66)

n, p = 10, 0.3
print(f"\nBINOMIAL(n={n}, p={p})")
print("  Use when: a fixed number of independent trials, each success or")
print("  failure, with a constant probability of success.")
print(f"\n{'k':<6}{'P(X=k)':<12}{'P(X<=k)':<12}Distribution")
for k in range(n + 1):
    pmf = S.binomial_pmf(k, n, p)
    cdf = S.binomial_cdf(k, n, p)
    print(f"{k:<6}{pmf:<12.5f}{cdf:<12.5f}{'#' * int(pmf * 150)}")
print(f"\n  Mean     = n.p        = {n} x {p} = {n * p:.2f}")
print(f"  Variance = n.p.(1-p)  = {n} x {p} x {1-p} = {n * p * (1 - p):.2f}")
print(f"  Excel: =BINOM.DIST(k, {n}, {p}, FALSE) for the PMF, TRUE for the CDF")

lam = 3
print(f"\nPOISSON(lambda={lam})")
print("  Use when: counting events in a fixed interval of time or space,")
print("  occurring independently at a constant average rate.")
print(f"\n{'k':<6}{'P(X=k)':<12}{'P(X<=k)':<12}Distribution")
for k in range(11):
    pmf = S.poisson_pmf(k, lam)
    cdf = S.poisson_cdf(k, lam)
    print(f"{k:<6}{pmf:<12.5f}{cdf:<12.5f}{'#' * int(pmf * 150)}")
print(f"\n  Mean = Variance = lambda = {lam}")
print("  That mean and variance are equal is the signature of a Poisson.")
print(f"  Excel: =POISSON.DIST(k, {lam}, FALSE)")

print("\n  POISSON AS A LIMIT OF THE BINOMIAL (n large, p small, np = lambda):")
print(f"  {'k':<6}{'Binomial(1000, 0.003)':<24}{'Poisson(3)':<14}difference")
for k in range(6):
    b = S.binomial_pmf(k, 1000, 0.003)
    po = S.poisson_pmf(k, 3)
    print(f"  {k:<6}{b:<24.6f}{po:<14.6f}{abs(b - po):.6f}")

print("\n" + "=" * 66)
print("EXPERIMENT 11: Continuous distributions -- Normal and Exponential")
print("=" * 66)

mu, sigma = 100, 15
print(f"\nNORMAL(mu={mu}, sigma={sigma})  -- IQ scores, a standard example")
print("\n  THE EMPIRICAL RULE (68-95-99.7)")
for k in (1, 2, 3):
    low, high = mu - k * sigma, mu + k * sigma
    prob = S.normal_cdf(high, mu, sigma) - S.normal_cdf(low, mu, sigma)
    print(f"    within {k} sd  [{low:6.1f}, {high:6.1f}] -> {prob * 100:6.2f}%")

print("\n  SPECIFIC PROBABILITIES")
print(f"    P(X <= 115)      = {S.normal_cdf(115, mu, sigma):.4f}"
      f"   Excel =NORM.DIST(115,100,15,TRUE)")
print(f"    P(X > 130)       = {1 - S.normal_cdf(130, mu, sigma):.4f}"
      f"   Excel =1-NORM.DIST(130,100,15,TRUE)")
print(f"    P(85 <= X <= 115) = "
      f"{S.normal_cdf(115, mu, sigma) - S.normal_cdf(85, mu, sigma):.4f}")

print("\n  STANDARDISING -- z = (x - mu) / sigma")
for x in (85, 100, 115, 130):
    z = (x - mu) / sigma
    print(f"    x = {x:3d}  ->  z = {z:+.2f}  ->  P(X <= x) = "
          f"{S.normal_cdf(z):.4f}")

print("\n  PERCENTILES (inverse -- Excel's NORM.INV)")
for pct in (0.90, 0.95, 0.99):
    print(f"    {pct * 100:.0f}th percentile = {S.normal_ppf(pct, mu, sigma):.2f}")

rate = 0.5
print(f"\nEXPONENTIAL(lambda={rate})  -- waiting time until the next event")
print(f"  Mean = 1/lambda = {1 / rate:.2f}, Variance = 1/lambda^2 = "
      f"{1 / rate ** 2:.2f}")
print(f"\n{'x':<8}{'PDF f(x)':<14}{'CDF P(X<=x)':<16}P(X>x)")
for x in (0, 1, 2, 3, 4, 5):
    print(f"{x:<8}{S.exponential_pdf(x, rate):<14.5f}"
          f"{S.exponential_cdf(x, rate):<16.5f}"
          f"{1 - S.exponential_cdf(x, rate):.5f}")
print(f"\n  Excel: =EXPON.DIST(x, {rate}, TRUE) for the CDF")
print("\n  MEMORYLESSNESS -- P(X > s+t | X > s) = P(X > t)")
s, t = 2, 3
joint = 1 - S.exponential_cdf(s + t, rate)
given = 1 - S.exponential_cdf(s, rate)
print(f"    P(X > {s+t} | X > {s}) = {joint:.5f} / {given:.5f} = {joint / given:.5f}")
print(f"    P(X > {t})           = {1 - S.exponential_cdf(t, rate):.5f}")
print("    Equal -- having waited 2 minutes tells you nothing about the next 3.")
print("    The exponential is the only continuous distribution with this property.")
