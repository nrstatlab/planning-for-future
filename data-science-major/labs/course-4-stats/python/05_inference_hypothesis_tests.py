"""Course 4 Lab, experiments 14-15: confidence intervals and the four
hypothesis tests named in Unit 5 -- z, t, chi-square and F.
"""

import statlib as S

print("=" * 68)
print("EXPERIMENT 14: Estimation and confidence intervals")
print("=" * 68)

sample = [68, 72, 75, 71, 69, 74, 73, 70, 76, 72,
          71, 73, 69, 75, 74, 72, 70, 73, 71, 74]
n = len(sample)
mean = sum(sample) / n
var = sum((x - mean) ** 2 for x in sample) / (n - 1)
sd = var ** 0.5
se = sd / n ** 0.5

print(f"\n  Sample of n = {n} heights (cm)")
print(f"  mean = {mean:.3f}   sample sd = {sd:.3f}   standard error = "
      f"sd/sqrt(n) = {se:.4f}")
print("\n  POINT ESTIMATE vs INTERVAL ESTIMATE")
print(f"    A point estimate is the single number {mean:.2f}. It is almost")
print("    certainly not exactly right. An interval estimate admits that.")

print("\n  CONFIDENCE INTERVALS -- population sd unknown, so use t")
for level, alpha in ((0.90, 0.10), (0.95, 0.05), (0.99, 0.01)):
    # Critical t by bisection on the CDF.
    low, high = 0.0, 100.0
    for _ in range(200):
        mid = (low + high) / 2
        if S.t_cdf(mid, n - 1) < 1 - alpha / 2:
            low = mid
        else:
            high = mid
    t_crit = (low + high) / 2
    margin = t_crit * se
    print(f"    {level * 100:.0f}%: t({alpha/2:.3f}, {n-1}) = {t_crit:.4f}, "
          f"margin = {margin:.4f}  ->  ({mean - margin:.3f}, {mean + margin:.3f})")

print("\n  WHAT 95% CONFIDENCE ACTUALLY MEANS")
print("    If we repeated this sampling many times and built an interval each")
print("    time, about 95% of those intervals would contain the true")
print("    population mean. It does NOT mean there is a 95% probability that")
print("    the true mean lies in THIS interval -- the true mean is a fixed")
print("    number, not a random one. Saying otherwise loses marks.")
print("\n    Notice the interval widens as confidence rises: more certainty")
print("    costs precision. It narrows as n grows, in proportion to 1/sqrt(n)")
print("    -- to halve the width you need four times the data.")

print("\n" + "=" * 68)
print("EXPERIMENT 15: Hypothesis testing")
print("=" * 68)

print("""
  THE PROCEDURE, every time:
    1. State H0 (no effect) and H1 (the claim being tested)
    2. Choose the significance level alpha, usually 0.05
    3. Compute the test statistic
    4. Find the p-value, or compare against the critical value
    5. Decide: p < alpha means reject H0
    6. State the conclusion in the words of the original problem
""")

# ---------------------------------------------------------------------
print("-" * 68)
print("1. ONE-SAMPLE z-TEST -- population sd KNOWN, large sample")
print("-" * 68)
mu0, sigma_known, n_z = 70, 3.0, 40
xbar = 71.2
z = (xbar - mu0) / (sigma_known / n_z ** 0.5)
p_two = 2 * (1 - S.normal_cdf(abs(z)))
print(f"""
  A machine should fill packets to a mean of {mu0} g, with a known population
  sd of {sigma_known} g. A sample of {n_z} packets averages {xbar} g.

  H0: mu = {mu0}        H1: mu != {mu0}       alpha = 0.05
  z = (xbar - mu0) / (sigma / sqrt(n))
    = ({xbar} - {mu0}) / ({sigma_known} / sqrt({n_z}))
    = {xbar - mu0:.2f} / {sigma_known / n_z ** 0.5:.4f} = {z:.4f}
  critical value: +/- 1.96      p-value = {p_two:.4f}
  Decision: {'reject H0' if p_two < 0.05 else 'fail to reject H0'}""")
print(f"  Conclusion: the mean fill weight {'differs' if p_two < 0.05 else 'does not differ'}"
      f" significantly from {mu0} g.")
print("  Excel: =2*(1-NORM.S.DIST(ABS(z),TRUE))")

# ---------------------------------------------------------------------
print("\n" + "-" * 68)
print("2. TWO-SAMPLE t-TEST -- population sd UNKNOWN")
print("-" * 68)
group_a = [78, 82, 75, 88, 79, 84, 80, 86, 77, 83]
group_b = [72, 75, 70, 78, 74, 71, 76, 73, 69, 77]


def describe(values):
    m = sum(values) / len(values)
    v = sum((x - m) ** 2 for x in values) / (len(values) - 1)
    return m, v


m_a, v_a = describe(group_a)
m_b, v_b = describe(group_b)
n_a, n_b = len(group_a), len(group_b)

pooled_var = ((n_a - 1) * v_a + (n_b - 1) * v_b) / (n_a + n_b - 2)
se_diff = (pooled_var * (1 / n_a + 1 / n_b)) ** 0.5
t = (m_a - m_b) / se_diff
df = n_a + n_b - 2
p_t = S.t_sf_two_tailed(t, df)

print(f"""
  Do two teaching methods give different mean scores?

  Group A: n = {n_a}, mean = {m_a:.2f}, variance = {v_a:.3f}
  Group B: n = {n_b}, mean = {m_b:.2f}, variance = {v_b:.3f}

  H0: mu_A = mu_B      H1: mu_A != mu_B      alpha = 0.05

  pooled variance = [(n_A-1)s_A^2 + (n_B-1)s_B^2] / (n_A + n_B - 2)
                  = [{n_a-1} x {v_a:.3f} + {n_b-1} x {v_b:.3f}] / {df}
                  = {pooled_var:.4f}
  standard error  = sqrt(pooled x (1/n_A + 1/n_B)) = {se_diff:.4f}
  t = (mean_A - mean_B) / se = {m_a - m_b:.2f} / {se_diff:.4f} = {t:.4f}
  df = {df}      two-tailed p = {p_t:.6f}
  Decision: {'reject H0' if p_t < 0.05 else 'fail to reject H0'}""")
print(f"  Conclusion: the two methods {'do' if p_t < 0.05 else 'do not'} differ "
      f"significantly in mean score.")
print("  Excel: =T.TEST(range_A, range_B, 2, 2)")

# ---------------------------------------------------------------------
print("\n" + "-" * 68)
print("3. CHI-SQUARE TEST OF INDEPENDENCE")
print("-" * 68)
observed = [[30, 70], [45, 55], [25, 75]]
row_labels = ["North", "South", "East"]
col_labels = ["Premium", "Standard"]

row_sums = [sum(row) for row in observed]
col_sums = [sum(observed[i][j] for i in range(len(observed)))
            for j in range(len(observed[0]))]
total = sum(row_sums)

print(f"\n  Is region independent of purchase type?")
print(f"  H0: they are independent    H1: they are associated    alpha = 0.05")
print(f"\n  {'':<10}{'Observed':<24}{'Expected':<24}")
print(f"  {'Region':<10}" + "".join(f"{c:>11}" for c in col_labels)
      + "  " + "".join(f"{c:>11}" for c in col_labels))

chi2 = 0.0
for i, row in enumerate(observed):
    expected_row = []
    for j, obs in enumerate(row):
        exp = row_sums[i] * col_sums[j] / total
        expected_row.append(exp)
        chi2 += (obs - exp) ** 2 / exp
    print(f"  {row_labels[i]:<10}" + "".join(f"{v:>11}" for v in row)
          + "  " + "".join(f"{v:>11.2f}" for v in expected_row))

df_chi = (len(observed) - 1) * (len(observed[0]) - 1)
p_chi = S.chi2_sf(chi2, df_chi)
print(f"""
  Expected = (row total x column total) / grand total
  chi-square = sum (O - E)^2 / E = {chi2:.4f}
  df = (rows - 1)(columns - 1) = ({len(observed)}-1)({len(observed[0])}-1) = {df_chi}
  critical value at 0.05 with {df_chi} df = 5.991      p = {p_chi:.4f}
  Decision: {'reject H0' if p_chi < 0.05 else 'fail to reject H0'}""")
print(f"  Conclusion: region and purchase type are "
      f"{'associated' if p_chi < 0.05 else 'independent'}.")
print("\n  ASSUMPTION: every expected frequency should be at least 5.")
print(f"  Smallest expected here = "
      f"{min(row_sums[i] * col_sums[j] / total for i in range(len(observed)) for j in range(len(col_sums))):.2f} -- satisfied.")
print("  Excel: =CHISQ.TEST(observed_range, expected_range)")

# ---------------------------------------------------------------------
print("\n" + "-" * 68)
print("4. F-TEST FOR EQUALITY OF TWO VARIANCES")
print("-" * 68)
# Convention: put the larger variance on top, giving a right-tailed test.
if v_a >= v_b:
    f_stat, df1, df2, top, bottom = v_a / v_b, n_a - 1, n_b - 1, "A", "B"
else:
    f_stat, df1, df2, top, bottom = v_b / v_a, n_b - 1, n_a - 1, "B", "A"
p_f = 2 * S.f_sf(f_stat, df1, df2)      # doubled for a two-tailed test

print(f"""
  Do the two groups have equal variances? (This is the assumption the pooled
  t-test above relies on, so it is worth checking.)

  H0: sigma_A^2 = sigma_B^2      H1: they differ      alpha = 0.05

  F = larger variance / smaller variance = s_{top}^2 / s_{bottom}^2
    = {max(v_a, v_b):.4f} / {min(v_a, v_b):.4f} = {f_stat:.4f}
  df = ({df1}, {df2})      two-tailed p = {p_f:.4f}
  Decision: {'reject H0' if p_f < 0.05 else 'fail to reject H0'}""")
print(f"  Conclusion: the variances {'differ' if p_f < 0.05 else 'are not significantly different'}"
      f", so the pooled t-test above {'was not appropriate' if p_f < 0.05 else 'was appropriate'}.")
print("  Excel: =F.TEST(range_A, range_B)")

# ---------------------------------------------------------------------
print("\n" + "=" * 68)
print("TYPE I and TYPE II ERRORS, and POWER")
print("=" * 68)
print("""
                        | H0 is actually TRUE    | H0 is actually FALSE
  ----------------------|------------------------|----------------------
  We REJECT H0          | Type I error (alpha)   | Correct  (power)
  We FAIL TO REJECT H0  | Correct                | Type II error (beta)

  alpha = P(Type I)  -- convicting an innocent person. We choose this, 0.05.
  beta  = P(Type II) -- acquitting a guilty one. Follows from the design.
  Power = 1 - beta   -- the chance of detecting a real effect.

  Lowering alpha to 0.01 makes a Type I error rarer but a Type II error more
  likely. The only way to reduce both at once is a larger sample.
""")

# Power of the z-test above against a true mean of 71.5.
mu_true, alpha = 71.5, 0.05
crit = 1.959964
se_z = sigma_known / n_z ** 0.5
shift = (mu_true - mu0) / se_z
power = (1 - S.normal_cdf(crit - shift)) + S.normal_cdf(-crit - shift)
print(f"  Worked example -- power of test 1 if the true mean were {mu_true}:")
print(f"    shift = (mu_true - mu0)/se = ({mu_true} - {mu0})/{se_z:.4f} = {shift:.4f}")
print(f"    power = {power:.4f}, so beta = {1 - power:.4f}")
print(f"    A {power * 100:.0f}% chance of detecting a real shift of "
      f"{mu_true - mu0} g with n = {n_z}.")
