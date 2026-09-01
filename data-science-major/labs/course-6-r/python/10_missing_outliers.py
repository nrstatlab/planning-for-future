"""Experiment 10 (Python equivalent) -- missing data and outlier detection.

R version: ../10_missing_outliers.R  (is.na, na.omit, boxplot$out)
"""
import statistics

RAW = [45, 67, None, 52, 89, 91, None, 64, 58, 82,
       76, 69, 71, 250, 60, 55, 93, 48, 79, None]      # 250 is an outlier


def detect(v):
    missing = [i for i, x in enumerate(v) if x is None]
    return missing, [x for x in v if x is not None]


def iqr_fences(v):
    s = sorted(v); n = len(s)
    def q(p):
        pos = (n - 1) * p; lo = int(pos); hi = min(lo + 1, n - 1)
        return s[lo] + (pos - lo) * (s[hi] - s[lo])
    q1, q3 = q(.25), q(.75)
    iqr = q3 - q1
    return q1, q3, iqr, q1 - 1.5 * iqr, q3 + 1.5 * iqr


def zscore_outliers(v, threshold=3):
    m = statistics.mean(v); sd = statistics.stdev(v)
    return [x for x in v if abs((x - m) / sd) > threshold]


if __name__ == "__main__":
    missing, clean = detect(RAW)
    print("MISSING VALUES                 R: sum(is.na(x)) ; which(is.na(x))")
    print(f"  {len(missing)} of {len(RAW)} missing ({len(missing)/len(RAW):.0%})")
    print(f"  at positions (1-based, as R reports): {[i+1 for i in missing]}")

    print("\nIMPUTATION strategies")
    mean_i = statistics.mean(clean)
    med_i = statistics.median(clean)
    print(f"  mean imputation   -> fill with {mean_i:.2f}")
    print(f"  median imputation -> fill with {med_i:.2f}")
    print(f"  the two differ by {abs(mean_i-med_i):.2f} because the 250 drags the mean")
    print("  -> with an outlier present, MEDIAN imputation is the safer choice")

    print("\nOUTLIERS -- IQR rule           R: boxplot(x)$out")
    q1, q3, iqr, lo, hi = iqr_fences(clean)
    out_iqr = [x for x in clean if x < lo or x > hi]
    print(f"  Q1={q1:.2f}  Q3={q3:.2f}  IQR={iqr:.2f}")
    print(f"  fences = [{lo:.2f}, {hi:.2f}]")
    print(f"  outliers: {out_iqr}")

    print("\nOUTLIERS -- z-score rule (|z| > 3)")
    out_z = zscore_outliers(clean)
    print(f"  outliers: {out_z if out_z else 'none'}")
    m, sd = statistics.mean(clean), statistics.stdev(clean)
    print(f"  z for 250 = {(250-m)/sd:.3f}")

    print("\n  Both rules caught it here. Now MASKING, with a second outlier:")
    masked = clean + [260]
    m2, sd2 = statistics.mean(masked), statistics.stdev(masked)
    z_flagged = [x for x in masked if abs((x - m2) / sd2) > 3]
    q1b, q3b, iqrb, lob, hib = iqr_fences(masked)
    iqr_flagged = [x for x in masked if x < lob or x > hib]
    print(f"    with 250 AND 260 present: sd rises from {sd:.2f} to {sd2:.2f}")
    print(f"    z-score rule flags: {z_flagged if z_flagged else 'NOTHING'}")
    print(f"    IQR rule flags:     {iqr_flagged}")
    print("\n  That is masking: each outlier inflates the sd enough to pull the")
    print("  other back inside 3 standard deviations, so the z-score rule sees")
    print("  neither. Quartiles cannot be moved by extreme values, so the IQR")
    print("  rule still flags both. Prefer the IQR rule when outliers may cluster.")

    assert 250 in out_iqr, "IQR rule must catch the planted outlier"
    assert len(iqr_flagged) == 2, "IQR rule must catch both"
    assert len(z_flagged) < 2, "z-score rule should be masked by the pair"
    print("\n  IQR caught both; the z-score rule was masked ✓")
