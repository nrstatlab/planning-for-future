"""Experiment 2 (Python equivalent) -- binomial, normal and Poisson.

R version: ../02_distributions.R
Uses the statlib module written for Course 4, so the two courses' distribution
numbers are guaranteed consistent.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]
                       / "course-4-stats" / "python"))
import statlib as S     # noqa: E402


def binomial_table(n, p):
    return [(k, S.binomial_pmf(k, n, p), S.binomial_cdf(k, n, p))
            for k in range(n + 1)]


def poisson_table(lam, upto):
    return [(k, S.poisson_pmf(k, lam), S.poisson_cdf(k, lam))
            for k in range(upto + 1)]


if __name__ == "__main__":
    # Step 1: Tabulate Binomial(10, 0.3)
    n, p = 10, 0.3
    print(f"BINOMIAL(n={n}, p={p})           R: dbinom(k, {n}, {p})")
    print(f"  {'k':<4}{'P(X=k)':<12}{'P(X<=k)':<12}")
    for k, pmf, cdf in binomial_table(n, p):
        print(f"  {k:<4}{pmf:<12.6f}{cdf:<12.6f}")
    print(f"  mean = np = {n * p:.2f}    variance = np(1-p) = {n * p * (1 - p):.2f}")

    # Step 2: Tabulate Poisson(3)
    lam = 3
    print(f"\nPOISSON(lambda={lam})            R: dpois(k, {lam})")
    print(f"  {'k':<4}{'P(X=k)':<12}{'P(X<=k)':<12}")
    for k, pmf, cdf in poisson_table(lam, 8):
        print(f"  {k:<4}{pmf:<12.6f}{cdf:<12.6f}")
    print(f"  mean = variance = lambda = {lam}")

    # Step 3: Find the normal's areas within 1, 2 and 3 SD
    mu, sigma = 100, 15
    print(f"\nNORMAL(mu={mu}, sigma={sigma})       R: pnorm(x, {mu}, {sigma})")
    for k in (1, 2, 3):
        lo, hi = mu - k * sigma, mu + k * sigma
        prob = S.normal_cdf(hi, mu, sigma) - S.normal_cdf(lo, mu, sigma)
        print(f"  within {k} sd [{lo:6.1f},{hi:6.1f}] = {prob * 100:6.3f}%")

    # Step 4: Check the figures the R comments quote
    # The empirical rule, to four decimals -- these are the numbers the R
    # script's comments quote.
    assert abs((S.normal_cdf(115, mu, sigma) - S.normal_cdf(85, mu, sigma))
               - 0.682689) < 1e-5
    assert abs(S.binomial_pmf(3, 10, 0.3) - 0.266828) < 1e-5
    assert abs(S.poisson_pmf(3, 3) - 0.224042) < 1e-5
    print("\n  all values cross-checked against Course 4's statlib ✓")
