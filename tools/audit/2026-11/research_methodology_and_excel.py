"""Content check, November 2026: Statistical Techniques for Research Methodology and
Statistical Data Analysis using MS-Excel. Excel is not run; each function's value is reproduced."""
import math
import numpy as np
from scipy import stats

def close(a, b, tol): assert abs(a - b) <= tol, (a, b)
def skew(x):
    x = np.array(x, float); n = len(x); s = x.std(ddof=1)
    return n / ((n - 1) * (n - 2)) * (((x - x.mean()) / s) ** 3).sum()
def kurt(x):
    x = np.array(x, float); n = len(x); s = x.std(ddof=1)
    return n * (n + 1) / ((n - 1) * (n - 2) * (n - 3)) * (((x - x.mean()) / s) ** 4).sum() - 3 * (n - 1) ** 2 / ((n - 2) * (n - 3))

# ---- Research Methodology ----
close(3200 / 20 * math.sqrt(0.96), 156.77, 0.005)                     # Unit 2, standard error
close(0.45 * (12.5 - 16.2), -1.665, 1e-9)                             # Unit 2, non-response bias
close(2 * 225 / 105 + 2 * 225 / 95, 9.022, 0.001)                     # Unit 3, 2 x 2 chi-square
y = [42, 38, 45, 50, 35, 48, 52, 40]
close(np.var(y, ddof=1), 36.21, 0.005); close(skew(y), -0.03, 0.005)
sp = math.sqrt((29 * 8.3 ** 2 + 27 * 9.1 ** 2) / 56); t = 4.7 / (sp * math.sqrt(1 / 30 + 1 / 28))
close(t, 2.057, 0.001); close(stats.t.ppf(0.975, 56), 2.003, 0.0005)
O = np.array([[40, 30, 30], [25, 45, 30], [15, 25, 60]])
close(stats.chi2_contingency(O)[0], 33.38, 0.01)
r = stats.linregress([1000, 1200, 1500, 1800, 2000, 2500], [25, 32, 38, 45, 52, 60])
close(r.slope, 0.02339, 5e-6); close(r.intercept, 3.01, 0.005); close(r.rvalue ** 2, 0.988, 0.0005)
close((0.82 / 2) / (0.18 / 27), 61.5, 1e-9); close(0.025 * math.sqrt(19000), 3.45, 0.005)
close(10 / 9 * (1 - 11.0 / 85.5), 0.968, 0.0005)                      # Unit 4, Cronbach's alpha
close(5.7 / math.sqrt(1.2349), 5.13, 0.005); close(5.7 / math.sqrt((8.2 ** 2 + 7.5 ** 2) / 2), 0.725, 0.0005)
close(16.4 / math.sqrt((96.04 + 26.01) / 150), 18.18, 0.005)
close((0.78 / 4) / (0.22 / 115), 101.9, 0.05)                         # Unit 5, abstract
close(stats.norm.cdf(0.5 * math.sqrt(50) - stats.t.ppf(0.975, 198)), 0.94, 0.005)
# practical
close(4 / (math.sqrt(30.5) * 0.2), 3.62, 0.005); close(5 / math.sqrt(41 / 50), 5.52, 0.005)
close(0.62 * math.sqrt(48) / math.sqrt(1 - 0.62 ** 2), 5.47, 0.005)
close(15 / math.sqrt(208 / 75), 9.01, 0.005); close(300 / math.sqrt(17000), 2.30, 0.005)
close(10 / 9 * (1 - 12 / 45), 0.815, 0.0005)
close(stats.chi2_contingency([[45, 5], [40, 10], [30, 20], [15, 35]])[0], 46.15, 0.005)
close(0.68 * math.sqrt(78) / math.sqrt(1 - 0.68 ** 2), 8.19, 0.005)
close(1.1 / math.sqrt((2.25 + 3.24) / 75), 4.07, 0.005); close(160 / (1891.5 / 117), 9.90, 0.005)

# ---- MS-Excel ----
a = np.array([45, 52, 38, 71, 64, 49, 58, 33, 67, 72.])
close(a.mean(), 54.9, 1e-9); close(np.median(a), 55, 1e-9); close(a.var(ddof=1), 188.54, 0.005)
assert np.allclose(np.percentile(a, [25, 75]), [46.0, 66.25])
close(stats.gmean([1.1, 1.2, 1.3]), 1.197, 0.0005); close(stats.hmean([40, 60]), 48, 1e-9)
d1 = [5, 6, 7, 7, 8, 8, 8, 9, 9, 10]; d2 = [20, 22, 25, 28, 30, 35, 50, 80, 120]
close(skew(d1), -0.36, 0.005); close(kurt(d1), -0.15, 0.005); close(skew(d2), 1.71, 0.005); close(kurt(d2), 2.39, 0.005)
close(stats.t.ppf(0.975, 29) * 2.45, 5.01, 0.005)
close(stats.norm.sf(10 / 3), 0.00043, 5e-6); close(2 * stats.t.sf(3.06, 9), 0.013, 0.001)
close(stats.f.ppf(0.95, 10, 15), 2.54, 0.005); close(stats.f.ppf(0.975, 10, 15), 3.06, 0.005)
close(stats.chi2.sf(100 / 3, 1), 7.8e-9, 1e-10); close(stats.chi2.sf(1, 5), 0.96, 0.005)
# practical
b = np.append(a, [55, 49])
close(b.mean(), 54.42, 0.005); close(np.median(b), 53.5, 1e-9); close(stats.gmean(b), 53.01, 0.005); close(stats.hmean(b), 51.54, 0.005)
close(b.var(ddof=1), 157.17, 0.005); assert np.allclose(np.percentile(b, [25, 75]), [48.0, 64.75])
close(skew(b), -0.14, 0.005); close(kurt(b), -0.86, 0.005)
R = np.corrcoef([[150, 152, 155, 158, 160, 163, 165, 168, 170, 175], [50, 52, 54, 58, 59, 62, 64, 67, 70, 74], [22, 25, 21, 28, 24, 30, 26, 27, 32, 29]])
close(R[0, 1], 0.998, 0.0005); close(R[0, 2], 0.735, 0.0005); close(R[1, 2], 0.760, 0.0005)
r = stats.linregress(np.arange(2, 12), [50, 55, 62, 66, 72, 75, 80, 85, 90, 95])
close(r.slope, 4.909, 0.0005); close(r.intercept, 41.09, 0.005); close(r.intercept + 8.5 * r.slope, 82.82, 0.005)
A = [62, 65, 58, 70, 66, 61, 68, 64, 59, 67]; B = [58, 60, 55, 63, 57, 61, 54, 59, 62, 56, 60, 58]
tt = stats.ttest_ind(A, B); close(tt.statistic, 3.77, 0.005); close(tt.pvalue, 0.0012, 5e-5)
tp = stats.ttest_rel([72, 78, 69, 80, 85, 76, 82, 74], [70, 76, 67, 78, 83, 74, 79, 72]); close(tp.statistic, 17.0, 0.005)
f = stats.f_oneway([22, 26, 24, 28], [30, 34, 32, 36], [20, 22, 24, 22]); close(f.statistic, 24.25, 0.005)
close(stats.t.ppf(0.975, 9) * math.sqrt(2 * 48 / 9 / 4), 3.69, 0.005)
print("research_methodology_and_excel: all checks pass")
