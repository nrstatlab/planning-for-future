"""Experiment 3 (Python equivalent) -- t-test and chi-square test.

R version: ../03_hypothesis_tests.R  (t.test() and chisq.test())
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "course-4-stats" / "python"))
import statlib as S     # noqa: E402

GROUP_A = [78, 82, 75, 88, 79, 84, 80, 86, 77, 83]
GROUP_B = [72, 75, 70, 78, 74, 71, 76, 73, 69, 77]

OBSERVED = [[30, 70], [45, 55], [25, 75]]      # region x purchase type


def describe(v):
    m = sum(v) / len(v)
    return m, sum((x - m) ** 2 for x in v) / (len(v) - 1)


def two_sample_t(a, b):
    ma, va = describe(a)
    mb, vb = describe(b)
    na, nb = len(a), len(b)
    pooled = ((na - 1) * va + (nb - 1) * vb) / (na + nb - 2)
    se = (pooled * (1 / na + 1 / nb)) ** 0.5
    t = (ma - mb) / se
    df = na + nb - 2
    return t, df, S.t_sf_two_tailed(t, df), pooled, se


def chi_square(observed):
    rows = [sum(r) for r in observed]
    cols = [sum(observed[i][j] for i in range(len(observed)))
            for j in range(len(observed[0]))]
    total = sum(rows)
    chi2 = 0.0
    expected = []
    for i, row in enumerate(observed):
        exp_row = []
        for j, o in enumerate(row):
            e = rows[i] * cols[j] / total
            exp_row.append(e)
            chi2 += (o - e) ** 2 / e
        expected.append(exp_row)
    df = (len(observed) - 1) * (len(observed[0]) - 1)
    return chi2, df, S.chi2_sf(chi2, df), expected


if __name__ == "__main__":
    t, df, p, pooled, se = two_sample_t(GROUP_A, GROUP_B)
    print("TWO-SAMPLE t-TEST        R: t.test(a, b, var.equal = TRUE)")
    print(f"  mean A   = {sum(GROUP_A)/len(GROUP_A):.4f}")
    print(f"  mean B   = {sum(GROUP_B)/len(GROUP_B):.4f}")
    print(f"  pooled var = {pooled:.4f}    se = {se:.4f}")
    print(f"  t = {t:.4f}   df = {df}   p = {p:.6f}")
    print(f"  -> {'reject' if p < 0.05 else 'fail to reject'} H0 at alpha = 0.05")

    chi2, cdf, cp, expected = chi_square(OBSERVED)
    print("\nCHI-SQUARE TEST          R: chisq.test(matrix)")
    print("  expected frequencies:")
    for row in expected:
        print("   ", "  ".join(f"{e:7.3f}" for e in row))
    print(f"  chi-square = {chi2:.4f}   df = {cdf}   p = {cp:.6f}")
    print(f"  -> {'reject' if cp < 0.05 else 'fail to reject'} H0")
    print(f"  smallest expected = {min(min(r) for r in expected):.2f} (must be >= 5)")

    # These must agree with Course 4 Unit 5, which uses the same data.
    assert abs(t - 4.754053) < 1e-5, t
    assert abs(chi2 - 9.75) < 1e-9
    print("\n  matches Course 4 Unit 5's worked examples ✓")
