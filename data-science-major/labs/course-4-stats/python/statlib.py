"""Minimal distribution functions for the Course 4 labs.

scipy is not installed in the verification environment, so the CDFs the
hypothesis-testing experiments need are implemented here from the standard
library alone. The algorithms are the classic ones: a continued-fraction
incomplete beta for t and F, and a series/continued-fraction incomplete gamma
for chi-square. math.erf gives the normal CDF exactly.

Accuracy is checked against published statistical tables in
test_statlib.py -- run that before trusting a p-value from here.
"""

import math

# ---------------------------------------------------------------------
# Normal distribution
# ---------------------------------------------------------------------


def normal_pdf(x, mu=0.0, sigma=1.0):
    z = (x - mu) / sigma
    return math.exp(-0.5 * z * z) / (sigma * math.sqrt(2 * math.pi))


def normal_cdf(x, mu=0.0, sigma=1.0):
    """P(X <= x). Exact, via the error function."""
    return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))


def normal_ppf(p, mu=0.0, sigma=1.0):
    """Inverse CDF by bisection -- Excel's NORM.INV."""
    if not 0 < p < 1:
        raise ValueError("p must lie strictly between 0 and 1")
    low, high = -40.0, 40.0
    for _ in range(200):
        mid = (low + high) / 2
        if normal_cdf(mid) < p:
            low = mid
        else:
            high = mid
    return mu + sigma * (low + high) / 2


# ---------------------------------------------------------------------
# Incomplete gamma -- underlies the chi-square distribution
# ---------------------------------------------------------------------


def _lower_gamma_regularised(s, x):
    """P(s, x): the regularised lower incomplete gamma function."""
    if x < 0 or s <= 0:
        raise ValueError("require x >= 0 and s > 0")
    if x == 0:
        return 0.0
    if x < s + 1:
        # Series expansion converges quickly here.
        term = 1.0 / s
        total = term
        n = s
        for _ in range(1000):
            n += 1
            term *= x / n
            total += term
            if abs(term) < abs(total) * 1e-15:
                break
        return total * math.exp(-x + s * math.log(x) - math.lgamma(s))
    # Continued fraction for the upper function, then complement it.
    tiny = 1e-300
    b = x + 1 - s
    c = 1 / tiny
    d = 1 / b
    h = d
    for i in range(1, 1000):
        an = -i * (i - s)
        b += 2
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < 1e-15:
            break
    upper = math.exp(-x + s * math.log(x) - math.lgamma(s)) * h
    return 1 - upper


def chi2_cdf(x, df):
    """P(X <= x) for a chi-square distribution with `df` degrees of freedom."""
    if x <= 0:
        return 0.0
    return _lower_gamma_regularised(df / 2.0, x / 2.0)


def chi2_sf(x, df):
    """Upper tail P(X > x) -- the p-value for a chi-square test."""
    return 1.0 - chi2_cdf(x, df)


# ---------------------------------------------------------------------
# Incomplete beta -- underlies the t and F distributions
# ---------------------------------------------------------------------


def _betacf(a, b, x):
    """Continued fraction for the incomplete beta function."""
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1, a - 1
    c = 1.0
    d = 1 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1 / d
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < 1e-15:
            break
    return h


def _betainc(a, b, x):
    """Regularised incomplete beta function I_x(a, b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    front = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                     + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return front * _betacf(a, b, x) / a
    return 1 - math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                        + b * math.log(1 - x) + a * math.log(x)) \
        * _betacf(b, a, 1 - x) / b


def t_cdf(t, df):
    """P(T <= t) for Student's t with `df` degrees of freedom."""
    x = df / (df + t * t)
    prob = 0.5 * _betainc(df / 2.0, 0.5, x)
    return 1 - prob if t > 0 else prob


def t_sf_two_tailed(t, df):
    """Two-tailed p-value for a t statistic."""
    return 2 * (1 - t_cdf(abs(t), df))


def f_cdf(f, df1, df2):
    """P(F <= f) for the F distribution."""
    if f <= 0:
        return 0.0
    return _betainc(df1 / 2.0, df2 / 2.0, df1 * f / (df1 * f + df2))


def f_sf(f, df1, df2):
    """Upper tail P(F > f) -- the p-value for a one-tailed F test."""
    return 1.0 - f_cdf(f, df1, df2)


# ---------------------------------------------------------------------
# Discrete distributions
# ---------------------------------------------------------------------


def binomial_pmf(k, n, p):
    """P(X = k) for X ~ Binomial(n, p)."""
    return math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))


def binomial_cdf(k, n, p):
    return sum(binomial_pmf(i, n, p) for i in range(k + 1))


def poisson_pmf(k, lam):
    """P(X = k) for X ~ Poisson(lambda)."""
    return math.exp(-lam) * (lam ** k) / math.factorial(k)


def poisson_cdf(k, lam):
    return sum(poisson_pmf(i, lam) for i in range(k + 1))


def exponential_pdf(x, lam):
    return lam * math.exp(-lam * x) if x >= 0 else 0.0


def exponential_cdf(x, lam):
    return 1 - math.exp(-lam * x) if x >= 0 else 0.0
