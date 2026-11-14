"""Content check, November 2026: Statistical Analysis using SPSS and the two Computational
Statistics and R Programming courses. SPSS and R are not run; the printed figures that do not
need R's built-in data sets are reproduced here."""
import itertools, math
from math import comb
import numpy as np
from scipy import stats, optimize

def close(a, b, tol): assert abs(a - b) <= tol, (a, b)

# ---- SPSS practical: the twenty cases ----
age = np.array([23,45,31,58,27,39,52,34,29,48,36,41,25,55,33,44,30,50,28,38.])
inc = np.array([40,57,37,69,36,38,63,32,35,57,42,49,26,39,48,49,23,57,27,33.])
vis = np.array([7,5,8,10,6,5,7,9,3,5,6,7,4,2,6,5,10,5,9,5.])
sc = np.array([54,55,64,77,69,60,85,57,65,59,64,60,51,57,60,60,55,67,40,56.])
buy = np.array([0,1,0,1,1,0,1,0,0,1,0,0,0,0,1,1,0,1,0,0.])
g = np.array(['M', 'F'] * 10)
for v, mean, sd, g1, G1 in ((age, 38.3, 10.4534, 0.3507, 0.379812), (inc, 42.85, 12.8279, 0.3874, 0.419544),
                            (sc, 60.75, 9.4361, 0.5613, 0.607924)):
    close(v.mean(), mean, 1e-9); close(v.std(ddof=1), sd, 5e-5)
    close(stats.skew(v), g1, 5e-5); close(stats.skew(v, bias=False), G1, 5e-7)
M, F = sc[g == 'M'], sc[g == 'F']
lev = stats.levene(M, F, center='mean'); close(lev.statistic, 2.1833, 5e-5); close(lev.pvalue, 0.1568, 5e-5)
tt = stats.ttest_ind(M, F); close(tt.statistic, -0.0231, 5e-5); close(tt.pvalue, 0.9819, 5e-5)
gr = np.where(sc < 57, 0, np.where(sc < 65, 1, 2))
assert [int((gr == i).sum()) for i in range(3)] == [6, 9, 5]
close(stats.f_oneway(*[sc[gr == i] for i in range(3)]).statistic, 19.756, 0.001)
tab = np.array([[((g == s) & (gr == i)).sum() for i in range(3)] for s in 'FM'])
chi = stats.chi2_contingency(tab); close(chi[0], 1.867, 0.001); close(chi[1], 0.393, 0.001)
tot = comb(20, 10); obs = comb(6, 2) * comb(9, 6) * comb(5, 2) / tot; p = 0
for a in range(7):
    for b in range(10):
        c = 10 - a - b
        if 0 <= c <= 5:
            q = comb(6, a) * comb(9, b) * comb(5, c) / tot
            if q <= obs + 1e-12: p += q
close(p, 0.523, 0.001)                                    # Fisher's exact test
n = 20; X = {'age': age, 'income': inc, 'visits': vis}
def rss(names):
    A = np.column_stack([np.ones(n)] + [X[k] for k in names]); b = np.linalg.lstsq(A, sc, rcond=None)[0]
    r = sc - A @ b; return r @ r, b, A
s2 = rss(list(X))[0] / 16; tss = rss([])[0]
page = {(): (0, 10.109, 90.756), ('age',): (0.2583, 4.849, 86.780), ('income',): (0.4272, 0.100, 81.610),
        ('visits',): (0.0029, 12.029, 92.698), ('age', 'income'): (0.4272, 2.100, 83.610),
        ('age', 'visits'): (0.2733, 6.427, 88.370), ('income', 'visits'): (0.4307, 2.003, 83.489),
        ('age', 'income', 'visits'): (0.4308, 4.000, 85.485)}
for c, (r2, cp, aic) in page.items():
    r = rss(list(c))[0]; k = len(c) + 1
    close(1 - r / tss, r2, 5e-5); close(r / s2 - n + 2 * k, cp, 0.001); close(n * math.log(r / n) + 2 * k, aic, 0.001)
r, b, A = rss(['income']); se = np.sqrt(r / 18 * np.diag(np.linalg.inv(A.T @ A)))
close(b[0], 40.147655, 1e-6); close(b[1], 0.480802, 1e-6); close((tss - r) / (r / 18), 13.4262, 1e-4)
def nll(bb, link):
    eta = bb[0] + bb[1] * inc; pr = 1 / (1 + np.exp(-eta)) if link == 'l' else stats.norm.cdf(eta)
    pr = np.clip(pr, 1e-12, 1 - 1e-12); return -(buy * np.log(pr) + (1 - buy) * np.log(1 - pr)).sum()
for link, x0, dev, slope in (('l', [-11, .25], 11.6415, 0.250124), ('p', [-6, .14], 11.6193, 0.142527)):
    o = optimize.minimize(nll, x0, args=(link,), method='Nelder-Mead', options={'xatol': 1e-10, 'fatol': 1e-12, 'maxiter': 5000})
    close(2 * o.fun, dev, 1e-4); close(o.x[1], slope, 1e-5)

# ---- R programming (current syllabus) ----
m = [45, 52, 38, 71, 64, 49, 58, 33, 67, 72, 55, 49]
close(stats.trim_mean(m, 0.1), 54.8, 1e-9); close(np.var(m, ddof=1), 157.17, 0.005)
for d, sk, ku in (([5,6,7,7,8,8,8,9,9,10], -0.30, 2.37), ([20,22,25,28,30,35,50,80,120], 1.41, 3.66)):
    close(stats.skew(d), sk, 0.005); close(stats.kurtosis(d, fisher=False), ku, 0.005)
close(stats.chi2.sf(sum((o - e) ** 2 / e for o, e in zip([460, 140, 130, 70], [450, 150, 150, 50])), 3), 0.009, 0.0005)
close(stats.norm.pdf(1.5), 0.1295, 5e-5); close(stats.binom.cdf(3, 10, .5), 0.172, 0.0005)
close(stats.poisson.pmf(5, 3), 0.1008, 5e-5); close(stats.poisson.cdf(2, 3), 0.4232, 5e-5)
assert stats.binom.ppf(.95, 10, .5) == 8 and stats.poisson.ppf(.9, 3) == 5
close(stats.norm.sf(80, 60, 15), 0.0912, 5e-5); close(stats.binom.cdf(8, 20, .5), 0.2517, 5e-5)
t1 = stats.ttest_1samp([48, 52, 49, 53, 51, 47, 55, 50, 49, 52], 50); close(t1.statistic, 0.7717, 5e-5); close(t1.pvalue, 0.46, 5e-4)
close(200 * (60 * 80 - 40 * 20 - 100) ** 2 / (100 * 100 * 80 * 120), 31.688, 0.001)
hours = np.arange(2, 12); marks = np.array([50, 55, 62, 66, 72, 75, 80, 85, 90, 95])
lr = stats.linregress(hours, marks)
close(lr.rvalue, 0.9985, 5e-5); close(lr.slope, 4.9091, 5e-5); close(lr.intercept, 41.0909, 5e-5)
close(lr.stderr, 0.0939, 5e-5); close(lr.intercept_stderr, 0.6672, 5e-5)
sres = math.sqrt(((marks - lr.intercept - lr.slope * hours) ** 2).sum() / 8); close(sres, 0.8528, 5e-5)
h = stats.t.ppf(.975, 8) * sres * math.sqrt(0.1 + (5 - 6.5) ** 2 / 82.5); close(65.636 - h, 64.93, 0.006)
close(stats.spearmanr([80, 85, 85, 70, 90], [70, 80, 90, 60, 95])[0], 0.975, 0.0005)
x = np.arange(1, 51); close(np.corrcoef(x, np.exp(x / 15))[0, 1], 0.924, 0.0005)

# ---- R programming (2023 syllabus) ----
close(8_000_000 / 1024 ** 2, 7.63, 0.005); close(math.sqrt(437.5 / 5), 9.354, 0.0005)
lr = stats.linregress([2, 4, 6, 8, 10], [15, 23, 28, 36, 43]); close(lr.slope, 3.45, 1e-9); close(lr.intercept, 8.3, 1e-9); close(lr.rvalue ** 2, 0.996, 0.0005)
t2 = stats.ttest_ind([20, 22, 19, 24, 25], [28, 26, 30, 27, 29]); close(t2.statistic, -4.47, 0.005); close(t2.pvalue, 0.0021, 5e-5)
close(stats.f.sf(6.84, 2, 12), 0.010, 0.0006); close(2 * stats.t.sf(3.2, 5), 0.024, 0.0005)
mk = np.array([32,47,41,51,41,30,39,18,48,53,54,32,31,46,15,37,32,56,42,48,38,26,50,40,38,42,35,22,62,51,44,21,45,31,37,41,44,18,37,47,68,41,30,52,52,60,42,38,38,34.])
m2 = np.array([30,42,41,31,41,38,39,18,28,53,64,32,41,26,25,37,32,56,52,18,48,76,20,10,48,45,39,29,69,52,47,28,47,32,67,51,44,19,27,42,66,21,60,22,52,64,49,33,35,37.])
close(mk.mean(), 40.34, 1e-9); assert np.allclose(np.percentile(mk, [25, 75]), [32.5, 47.75])
close(mk.var(ddof=1), 130.22898, 1e-5); close(mk.var(), 127.6244, 1e-6); close(np.abs(mk - mk.mean()).mean(), 8.7664, 1e-6)
close(mk.std(ddof=1) / mk.mean() * 100, 28.28902, 1e-5); close(np.corrcoef(mk, m2)[0, 1], 0.409, 0.0005)
D = np.array([[6, 5, 3, 1], [3, 6, 3, 2], [3, 4, 3, 1]]); P = np.array([[1.5, 1], [2, 2.5], [5, 4.5], [16, 17]])
assert np.allclose(D @ P, [[50, 49], [63.5, 65.5], [43.5, 43.5]])
print("spss_and_r_programming: all checks pass")

# ---- Data Handling using R (same twenty cases) ----
def cvr(k, d):
    fold = np.arange(1, n + 1) % k; sq = []
    for f in np.unique(fold):
        tr = fold != f; c = np.polyfit(inc[tr], sc[tr], d); sq += list((sc[~tr] - np.polyval(c, inc[~tr])) ** 2)
    return math.sqrt(np.mean(sq))
for d, ins, c5, loo in ((1, 6.9605, 7.3777, 7.9238), (2, 6.9053, 7.5765, 8.1354), (3, 6.3354, 10.8021, 10.7390), (5, 4.7282, 17.7650, 13.0146)):
    close(math.sqrt(np.mean((sc - np.polyval(np.polyfit(inc, sc, d), inc)) ** 2)), ins, 1e-4); close(cvr(5, d), c5, 1e-3); close(cvr(20, d), loo, 1e-3)
res = sc - np.polyval(np.polyfit(inc, sc, 1), inc); s = res > 0
runs = 1 + (s[1:] != s[:-1]).sum(); n1 = s.sum(); n0 = n - n1
mu = 2 * n1 * n0 / n + 1; sg = math.sqrt(2 * n1 * n0 * (2 * n1 * n0 - n) / (n * n * (n - 1)))
assert runs == 7; close((runs - mu) / sg, -1.811043, 1e-6)
for f, v in ((np.log, -0.107543), (np.sqrt, 0.147594), (np.square, 0.822684)): close(stats.skew(f(inc)), v, 1e-6)
fr = M.var(ddof=1) / F.var(ddof=1); close(fr, 3.32, 0.001); close(2 * stats.f.sf(fr, 9, 9), 0.08848, 1e-5)
pr = 1 / (1 + np.exp(11.4011323 - 0.2501235 * inc)); pos = pr[buy == 1]; neg = pr[buy == 0]
close(np.mean([(a > b) + .5 * (a == b) for a in pos for b in neg]), 0.921875, 1e-9)
bf = np.array([68,72,65,70,74,66,71,69,73,67,75,64]); af = np.array([71,74,64,73,77,69,70,72,76,71,74,68])
close(stats.wilcoxon(af, bf, correction=False, method='approx').pvalue, 0.008551, 1e-6)
close(stats.binomtest(9, 12, 0.5).pvalue, 0.1459961, 1e-7); close(2 * math.sin(5 * math.pi / 12), 1.931852, 1e-6)
print("data_handling_using_r: all checks pass")
