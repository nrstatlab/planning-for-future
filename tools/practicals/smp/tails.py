# tails.py -- the four tail areas every test below needs, written out because
# no statistical package may be used.  Save this file once and import from it.
import math

# Step 1: The continued fraction for the incomplete beta
def betacf(a, b, x):
    """Continued fraction for the incomplete beta function, by Lentz's method."""
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (tiny if abs(d) < tiny else d)
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        c = 1 + aa / c
        d = 1 / (tiny if abs(d) < tiny else d)
        h *= d * (tiny if abs(c) < tiny else c)
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        c = 1 + aa / c
        d = 1 / (tiny if abs(d) < tiny else d)
        de = d * c
        h *= de
        if abs(de - 1) < 3e-16:
            break
    return h

# Step 2: The regularised incomplete beta
def betainc(a, b, x):
    """The regularised incomplete beta function I_x(a, b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lf = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lf + a * math.log(x) + b * math.log(1 - x)) * betacf(a, b, x) / a
    return 1 - math.exp(lf + b * math.log(1 - x) + a * math.log(x)) * betacf(b, a, 1 - x) / b

# Step 3: The t and F tails from it
def t_two_sided(t, df):
    """P(|T_df| > |t|)."""
    return betainc(df / 2, 0.5, df / (df + t * t))

def F_upper(f, d1, d2):
    """P(F_{d1,d2} > f)."""
    return 1.0 if f <= 0 else betainc(d2 / 2, d1 / 2, d2 / (d2 + d1 * f))

# Step 4: The chi-square tail from the incomplete gamma
def chi2_upper(q, df):
    """P(chi^2_df > q): the series for the lower gamma when q is small, and the
    continued fraction for the upper gamma when it is large, so that a tiny tail
    is computed directly instead of as 1 minus a number close to 1."""
    a, xq = df / 2, q / 2
    if xq <= 0:
        return 1.0
    front = math.exp(-xq + a * math.log(xq) - math.lgamma(a))
    if xq < a + 1:
        term, s, k = 1.0 / a, 1.0 / a, 1
        while abs(term) > 1e-15 * abs(s) and k < 10000:
            term *= xq / (a + k)
            s += term
            k += 1
        return 1 - s * front
    tiny = 1e-300                          # Lentz's method, as in betacf
    b = xq + 1 - a
    c, d = 1 / tiny, 1 / b
    h = d
    for i in range(1, 10000):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        d = 1 / (tiny if abs(d) < tiny else d)
        c = b + an / c
        c = tiny if abs(c) < tiny else c
        de = d * c
        h *= de
        if abs(de - 1) < 3e-16:
            break
    return front * h

# Step 5: The normal tail
def normal_two_sided(z):
    """P(|Z| > |z|) for the standard normal."""
    return math.erfc(abs(z) / math.sqrt(2))

# Step 6: Check all four against the tables
if __name__ == "__main__":
    # three published values, as a check that the functions are right
    print(f"P(|t_10| > 2.228)      = {t_two_sided(2.228, 10):.4f}   (table: 0.0500)")
    print(f"P(F_(5,10) > 3.326)    = {F_upper(3.326, 5, 10):.4f}   (table: 0.0500)")
    print(f"P(chi^2_8 > 15.507)    = {chi2_upper(15.507, 8):.4f}   (table: 0.0500)")
    print(f"P(|Z| > 1.959964)      = {normal_two_sided(1.959964):.4f}   (table: 0.0500)")
