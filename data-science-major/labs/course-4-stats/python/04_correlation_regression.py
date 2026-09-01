"""Course 4 Lab, experiments 7, 12 and 13: covariance, Pearson and Spearman
correlation, and simple linear regression with ANOVA.
"""

import statlib as S

# The classic paired dataset: hours studied against exam score.
hours = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
scores = [52, 55, 61, 64, 70, 72, 78, 82, 85, 91]
n = len(hours)

print("=" * 66)
print("EXPERIMENT 7 and 12: Covariance and correlation")
print("=" * 66)

mean_x = sum(hours) / n
mean_y = sum(scores) / n

print(f"\n{'Hours (x)':<12}{'Score (y)':<12}{'x-mx':<10}{'y-my':<10}"
      f"{'(x-mx)(y-my)':<15}{'(x-mx)^2':<12}{'(y-my)^2'}")
print("-" * 82)
sum_xy = sum_xx = sum_yy = 0.0
for x, y in zip(hours, scores):
    dx, dy = x - mean_x, y - mean_y
    sum_xy += dx * dy
    sum_xx += dx * dx
    sum_yy += dy * dy
    print(f"{x:<12}{y:<12}{dx:<10.2f}{dy:<10.2f}{dx * dy:<15.2f}"
          f"{dx * dx:<12.2f}{dy * dy:.2f}")
print("-" * 82)
print(f"{'Mean':<12}{mean_x:<12.2f}{'':<10}{'':<10}"
      f"{sum_xy:<15.2f}{sum_xx:<12.2f}{sum_yy:.2f}")
print(f"  mean of y = {mean_y:.2f}")

cov_sample = sum_xy / (n - 1)
cov_pop = sum_xy / n
print(f"\nCOVARIANCE")
print(f"  sample     (divide by n-1) = {sum_xy:.2f} / {n-1} = {cov_sample:.3f}")
print(f"  population (divide by n)   = {sum_xy:.2f} / {n} = {cov_pop:.3f}")
print("  Sign tells direction, magnitude is meaningless -- it depends on the")
print("  units. Change hours to minutes and the covariance multiplies by 60.")

r = sum_xy / (sum_xx * sum_yy) ** 0.5
print(f"\nPEARSON CORRELATION r")
print(f"  r = sum((x-mx)(y-my)) / sqrt(sum(x-mx)^2 x sum(y-my)^2)")
print(f"    = {sum_xy:.2f} / sqrt({sum_xx:.2f} x {sum_yy:.2f})")
print(f"    = {sum_xy:.2f} / {(sum_xx * sum_yy) ** 0.5:.2f}")
print(f"    = {r:.4f}")
print("  r is unit-free and always lies between -1 and +1. Excel: =CORREL(x,y)")

strength = ("very strong" if abs(r) >= 0.9 else "strong" if abs(r) >= 0.7
            else "moderate" if abs(r) >= 0.4 else "weak")
direction = "positive" if r > 0 else "negative"
print(f"  Interpretation: a {strength} {direction} linear relationship.")


def rank(values):
    """Ranks with ties averaged -- what Spearman requires."""
    ordered = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(ordered):
        j = i
        while j + 1 < len(ordered) and values[ordered[j + 1]] == values[ordered[i]]:
            j += 1
        average_rank = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[ordered[k]] = average_rank
        i = j + 1
    return ranks


rx, ry = rank(hours), rank(scores)
d_squared = sum((a - b) ** 2 for a, b in zip(rx, ry))
rho = 1 - (6 * d_squared) / (n * (n * n - 1))

print(f"\nSPEARMAN RANK CORRELATION rho")
print(f"  {'x':<8}{'y':<8}{'rank x':<10}{'rank y':<10}{'d':<8}{'d^2'}")
for x, y, a, b in zip(hours, scores, rx, ry):
    print(f"  {x:<8}{y:<8}{a:<10.1f}{b:<10.1f}{a - b:<8.1f}{(a - b) ** 2:.2f}")
print(f"  sum of d^2 = {d_squared:.2f}")
print(f"  rho = 1 - 6.sum(d^2) / n(n^2-1) = 1 - 6({d_squared:.0f}) / "
      f"{n}({n * n - 1}) = {rho:.4f}")
print("  Spearman works on ranks, so it detects any MONOTONIC relationship,")
print("  not only a straight-line one, and is unaffected by outliers.")

print("\n" + "=" * 66)
print("EXPERIMENT 13: Simple linear regression")
print("=" * 66)

b1 = sum_xy / sum_xx                 # slope
b0 = mean_y - b1 * mean_x            # intercept

print(f"\n  Model: y = b0 + b1.x")
print(f"  b1 (slope)     = sum((x-mx)(y-my)) / sum((x-mx)^2)")
print(f"                 = {sum_xy:.2f} / {sum_xx:.2f} = {b1:.4f}")
print(f"  b0 (intercept) = my - b1.mx = {mean_y:.2f} - {b1:.4f} x {mean_x:.2f}"
      f" = {b0:.4f}")
print(f"\n  FITTED LINE:  y = {b0:.4f} + {b1:.4f}x")
print(f"  Meaning: each extra hour of study is associated with about "
      f"{b1:.2f} more marks.")
print(f"  The intercept {b0:.2f} is the predicted score at zero hours -- treat")
print("  it cautiously, since x = 0 lies outside the observed range.")

print(f"\n  RESIDUALS")
print(f"  {'x':<8}{'observed y':<14}{'fitted y':<14}{'residual':<12}{'residual^2'}")
ss_res = ss_tot = 0.0
for x, y in zip(hours, scores):
    fitted = b0 + b1 * x
    residual = y - fitted
    ss_res += residual ** 2
    ss_tot += (y - mean_y) ** 2
    print(f"  {x:<8}{y:<14}{fitted:<14.3f}{residual:<12.3f}{residual ** 2:.4f}")

ss_reg = ss_tot - ss_res
r_squared = ss_reg / ss_tot

print(f"\n  ANALYSIS OF VARIANCE")
print(f"  {'Source':<14}{'SS':<14}{'df':<8}{'MS':<14}{'F'}")
print("  " + "-" * 58)
df_reg, df_res = 1, n - 2
ms_reg, ms_res = ss_reg / df_reg, ss_res / df_res
f_stat = ms_reg / ms_res
print(f"  {'Regression':<14}{ss_reg:<14.4f}{df_reg:<8}{ms_reg:<14.4f}{f_stat:.4f}")
print(f"  {'Residual':<14}{ss_res:<14.4f}{df_res:<8}{ms_res:<14.4f}")
print(f"  {'Total':<14}{ss_tot:<14.4f}{n - 1:<8}")

p_value = S.f_sf(f_stat, df_reg, df_res)
print(f"\n  F = {f_stat:.4f} on ({df_reg}, {df_res}) df,  p = {p_value:.3e}")
print(f"  R^2 = SS_regression / SS_total = {ss_reg:.4f} / {ss_tot:.4f} = "
      f"{r_squared:.4f}")
print(f"  So {r_squared * 100:.2f}% of the variation in scores is explained by hours.")
print(f"  Note that R^2 = r^2: {r:.4f}^2 = {r ** 2:.4f}  -- true for SIMPLE")
print("  regression only, not for multiple regression.")

se_slope = (ms_res / sum_xx) ** 0.5
t_stat = b1 / se_slope
print(f"\n  TESTING THE SLOPE   H0: b1 = 0   H1: b1 != 0")
print(f"  standard error of b1 = sqrt(MS_res / sum(x-mx)^2) = {se_slope:.4f}")
print(f"  t = b1 / se = {b1:.4f} / {se_slope:.4f} = {t_stat:.4f} on {df_res} df")
print(f"  two-tailed p = {S.t_sf_two_tailed(t_stat, df_res):.3e}")
print(f"  p < 0.05, so reject H0 -- the slope is significantly different from 0.")
print(f"  For simple regression t^2 = F: {t_stat:.4f}^2 = {t_stat ** 2:.4f}"
      f" = {f_stat:.4f}")

print(f"\n  PREDICTION")
for x in (7.5, 12):
    note = "" if min(hours) <= x <= max(hours) else "   <- EXTRAPOLATION, unsafe"
    print(f"    x = {x:<5} -> predicted score {b0 + b1 * x:.2f}{note}")

print("\n  CORRELATION IS NOT CAUSATION. This data cannot show that studying")
print("  causes higher scores -- only that they move together. A confounder")
print("  (prior ability, motivation) could drive both.")
