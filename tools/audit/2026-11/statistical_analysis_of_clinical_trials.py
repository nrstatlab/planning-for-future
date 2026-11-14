"""Content check, November 2026: Statistical Analysis of Clinical Trials.
Recomputes the practical page (Experiments 1, 3, 4, 5) and the Unit 4 Cox table p-value."""
import math
import numpy as np
from scipy import stats

def close(a, b, tol): assert abs(a - b) <= tol, (a, b)

# Experiment 1: sample size for two proportions, then for two means
pb = 0.55
n = (1.96 * math.sqrt(2 * pb * 0.45) + 0.842 * math.sqrt(0.65 * 0.35 + 0.45 * 0.55)) ** 2 / 0.04
close(n, 95.9, 0.1)
close(288 * 3.242 ** 2 / 25, 121.1, 0.05)

# Experiment 3: crossover, period differences of the two sequences
a = np.array([2.4, 2.8, 1.5, 3.1, 1.1, 3.3, 2.2, 1.8, 1.6, 2.5])
b = np.array([-2.3, -1.8, -2.3, -2.1, -2.3, -2.1, -1.8, -2.3, -2.3, -2.3])
close(a.mean(), 2.23, 1e-9); close(b.mean(), -2.16, 1e-9)
close(a.std(ddof=1), 0.72, 0.005); close(b.std(ddof=1), 0.21, 0.005)
close(stats.ttest_ind(a, b).statistic, 18.43, 0.005)

# Experiment 4: two-sample t and the 2 x 2 chi-square
sp = math.sqrt((0.9025 + 1.0404) / 2); t = -0.58 / (sp * 0.2)
close(sp, 0.9856, 5e-5); close(t, -2.94, 0.005)
h = stats.t.ppf(0.975, 98) * sp * 0.2
close(-0.58 - h, -0.971, 0.001); close(-0.58 + h, -0.189, 0.001)
close(100 * (32 * 29 - 18 * 21) ** 2 / (50 * 50 * 53 * 47), 4.86, 0.005)
close(32 * 29 / (18 * 21), 2.45, 0.006)

# Experiment 5: fixed-effect meta-analysis of six trials, Q and Egger's test
E = np.array([148, 109, 183, 209, 298, 265]); N = np.array([3171, 2035, 2530, 3402, 5139, 4401])
C = np.array([186, 142, 212, 251, 347, 302]); M = np.array([3168, 2037, 2540, 3395, 5127, 4405])
lo = np.log(E * (M - C) / ((N - E) * C)); se = np.sqrt(1 / E + 1 / (N - E) + 1 / C + 1 / (M - C)); w = 1 / se ** 2
assert np.allclose(np.exp(lo), [0.785, 0.755, 0.856, 0.820, 0.848, 0.870], atol=0.0006)
p = (w * lo).sum() / w.sum(); s = 1 / math.sqrt(w.sum())
close(math.exp(p), 0.832, 0.0005); close(math.exp(p - 1.96 * s), 0.768, 0.0006); close(math.exp(p + 1.96 * s), 0.900, 0.0006)
close((w * (lo - p) ** 2).sum(), 1.23, 0.005)
r = stats.linregress(1 / se, lo / se)
close(r.intercept, -2.43, 0.005); close(2 * stats.t.sf(abs(r.intercept / r.intercept_stderr), 4), 0.04, 0.005)

# Unit 4, Cox table: eGFR row, z = -0.10 / 0.040
close(2 * stats.norm.sf(2.5), 0.012, 0.0005)
print("statistical_analysis_of_clinical_trials: all checks pass")
