"""Experiment 4 (Python equivalent) -- correlation and simple linear regression.

R version: ../04_regression.R  (cor() and lm())
Uses the same hours/scores pair as Course 4 Unit 4, so the coefficients here
must reproduce that unit's worked example exactly.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "course-4-stats" / "python"))
import statlib as S     # noqa: E402
from _shared import HOURS, SCORES


def regress(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)

    r = sxy / (sxx * syy) ** 0.5
    b1 = sxy / sxx
    b0 = my - b1 * mx

    ss_res = sum((b - (b0 + b1 * a)) ** 2 for a, b in zip(x, y))
    ss_reg = syy - ss_res
    r2 = ss_reg / syy
    ms_res = ss_res / (n - 2)
    se_b1 = (ms_res / sxx) ** 0.5
    t = b1 / se_b1
    f = ss_reg / ms_res
    return dict(n=n, r=r, b0=b0, b1=b1, r2=r2, ss_tot=syy, ss_res=ss_res,
                ss_reg=ss_reg, ms_res=ms_res, se_b1=se_b1, t=t, f=f,
                p=S.t_sf_two_tailed(t, n - 2))


if __name__ == "__main__":
    m = regress(HOURS, SCORES)
    print("CORRELATION AND REGRESSION      R: cor(x,y) ; lm(y ~ x)")
    print(f"  Pearson r      = {m['r']:.6f}")
    print(f"  intercept b0   = {m['b0']:.4f}")
    print(f"  slope     b1   = {m['b1']:.4f}")
    print(f"  fitted line: y = {m['b0']:.4f} + {m['b1']:.4f} x")
    print(f"\n  R-squared      = {m['r2']:.6f}   (= r^2 = {m['r']**2:.6f})")
    print(f"  SE(b1)         = {m['se_b1']:.4f}")
    print(f"  t              = {m['t']:.4f}  on {m['n']-2} df,  p = {m['p']:.3e}")
    print(f"  F              = {m['f']:.4f}   (= t^2 = {m['t']**2:.4f})")
    print("\n  ANOVA")
    print(f"    Regression  SS={m['ss_reg']:10.4f}  df=1")
    print(f"    Residual    SS={m['ss_res']:10.4f}  df={m['n']-2}  MS={m['ms_res']:.4f}")
    print(f"    Total       SS={m['ss_tot']:10.4f}  df={m['n']-1}")
    print(f"\n  predict at x=7.5 -> {m['b0'] + m['b1']*7.5:.2f}")

    assert abs(m["r2"] - m["r"] ** 2) < 1e-12,  "R2 must equal r squared"
    assert abs(m["f"] - m["t"] ** 2) < 1e-6,    "F must equal t squared"
    assert abs(m["b1"] - 4.3030) < 1e-3
    print("\n  R2 = r^2 and F = t^2 both hold; matches Course 4 Unit 4 ✓")
