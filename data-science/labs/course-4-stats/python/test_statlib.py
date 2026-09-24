"""Check statlib against published statistical-table values.

Run this before trusting any p-value the labs print:
    python3 test_statlib.py
"""

import statlib as S

CASES = []


def check(label, got, expected, tol):
    ok = abs(got - expected) <= tol
    CASES.append(ok)
    status = "ok  " if ok else "FAIL"
    print(f"  [{status}] {label:<48} got {got:.5f}  expected {expected:.5f}")


print("NORMAL distribution")
check("normal_cdf(0)", S.normal_cdf(0), 0.5, 1e-12)
check("normal_cdf(1.96)  -- the 97.5th percentile", S.normal_cdf(1.96), 0.9750, 1e-4)
check("normal_cdf(1.645) -- the 95th percentile", S.normal_cdf(1.645), 0.9500, 1e-4)
check("normal_cdf(-1.96)", S.normal_cdf(-1.96), 0.0250, 1e-4)
check("normal_cdf(2.58)", S.normal_cdf(2.58), 0.99506, 1e-4)
check("normal_ppf(0.975) -- inverse gives 1.96 back", S.normal_ppf(0.975), 1.95996, 1e-4)

print("\nSTUDENT'S t distribution (two-tailed critical values from tables)")
# t(0.025, df) critical values: the CDF at those points must be 0.975.
check("t_cdf(2.086, df=20)  table t(0.025,20)=2.086", S.t_cdf(2.086, 20), 0.975, 5e-4)
check("t_cdf(2.228, df=10)  table t(0.025,10)=2.228", S.t_cdf(2.228, 10), 0.975, 5e-4)
check("t_cdf(1.812, df=10)  table t(0.05,10)=1.812", S.t_cdf(1.812, 10), 0.950, 5e-4)
check("t_cdf(0, df=5) is exactly one half", S.t_cdf(0, 5), 0.5, 1e-10)
check("t_cdf(1.96, df=100000) approaches the normal", S.t_cdf(1.96, 100000), 0.9750, 1e-3)

print("\nCHI-SQUARE distribution (critical values from tables)")
check("chi2_cdf(3.841, df=1)  table x2(0.05,1)=3.841", S.chi2_cdf(3.841, 1), 0.95, 5e-4)
check("chi2_cdf(5.991, df=2)  table x2(0.05,2)=5.991", S.chi2_cdf(5.991, 2), 0.95, 5e-4)
check("chi2_cdf(11.070, df=5) table x2(0.05,5)=11.070", S.chi2_cdf(11.070, 5), 0.95, 5e-4)
check("chi2_cdf(18.307, df=10) table x2(0.05,10)=18.307", S.chi2_cdf(18.307, 10), 0.95, 5e-4)

print("\nF distribution (critical values from tables)")
check("f_cdf(4.26, df=3,9)   table F(0.05,3,9)=3.86", S.f_cdf(3.86, 3, 9), 0.95, 5e-3)
check("f_cdf(4.96, df=1,10)  table F(0.05,1,10)=4.96", S.f_cdf(4.96, 1, 10), 0.95, 5e-3)
check("f_cdf(19.0, df=2,2)   table F(0.05,2,2)=19.00", S.f_cdf(19.00, 2, 2), 0.95, 5e-3)

print("\nDISCRETE distributions")
check("binomial_pmf(k=2,n=5,p=0.5) = 10/32", S.binomial_pmf(2, 5, 0.5), 0.3125, 1e-12)
check("binomial_cdf(k=5,n=5,p=0.3) sums to 1", S.binomial_cdf(5, 5, 0.3), 1.0, 1e-12)
check("poisson_pmf(k=0,lam=2) = e^-2", S.poisson_pmf(0, 2), 0.135335, 1e-6)
check("poisson_pmf(k=3,lam=3)", S.poisson_pmf(3, 3), 0.224042, 1e-6)
check("exponential_cdf(x=1,lam=1) = 1-1/e", S.exponential_cdf(1, 1), 0.632121, 1e-6)

failed = CASES.count(False)
print(f"\n{len(CASES) - failed}/{len(CASES)} checks passed")
raise SystemExit(1 if failed else 0)
