"""Experiment 5 (Python equivalent) -- exploratory data analysis.

R version: ../05_eda.R  (str, summary, colSums(is.na()), hist, boxplot)
"""
from _shared import STUDENTS

COLS = ["name", "section", "gender", "hours", "marks", "attendance"]


def to_columns(rows):
    return {c: [r[i] for r in rows] for i, c in enumerate(COLS)}


def summarise_numeric(v):
    s = sorted(v)
    n = len(s)
    def q(p):
        pos = (n - 1) * p
        lo = int(pos)
        hi = min(lo + 1, n - 1)
        return s[lo] + (pos - lo) * (s[hi] - s[lo])
    return dict(min=s[0], q1=q(.25), median=q(.5), mean=sum(s)/n,
                q3=q(.75), max=s[-1])


if __name__ == "__main__":
    d = to_columns(STUDENTS)
    print("STRUCTURE                      R: str(df)")
    print(f"  {len(STUDENTS)} observations of {len(COLS)} variables")
    for c in COLS:
        kind = "num" if isinstance(d[c][0], (int, float)) else "chr"
        print(f"    {c:<12} {kind}   e.g. {d[c][0]}")

    print("\nSUMMARY                        R: summary(df)")
    print(f"  {'':<12}{'Min':>8}{'1stQu':>9}{'Median':>9}{'Mean':>9}{'3rdQu':>9}{'Max':>8}")
    for c in ("hours", "marks", "attendance"):
        s = summarise_numeric(d[c])
        print(f"  {c:<12}{s['min']:>8.2f}{s['q1']:>9.2f}{s['median']:>9.2f}"
              f"{s['mean']:>9.2f}{s['q3']:>9.2f}{s['max']:>8.2f}")

    print("\nMISSING VALUES                 R: colSums(is.na(df))")
    for c in COLS:
        print(f"    {c:<12} {sum(1 for x in d[c] if x is None)}")

    print("\nCATEGORICAL COUNTS             R: table(df$section)")
    for c in ("section", "gender"):
        counts = {}
        for v in d[c]:
            counts[v] = counts.get(v, 0) + 1
        print(f"    {c}: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))

    print("\nHISTOGRAM of marks             R: hist(df$marks)")
    for lo in range(40, 100, 10):
        n = sum(1 for m in d["marks"] if lo <= m < lo + 10)
        print(f"    {lo}-{lo+9}  {'#' * n * 3} {n}")

    print("\nOUTLIERS (1.5 x IQR)           R: boxplot(df$marks)$out")
    s = summarise_numeric(d["marks"])
    iqr = s["q3"] - s["q1"]
    lo, hi = s["q1"] - 1.5 * iqr, s["q3"] + 1.5 * iqr
    out = [m for m in d["marks"] if m < lo or m > hi]
    print(f"    IQR = {iqr:.2f}, fences = [{lo:.2f}, {hi:.2f}]")
    print(f"    outliers: {out if out else 'none'}")

    print("\nCORRELATION                    R: cor(df[, c('hours','marks')])")
    x, y = d["hours"], d["marks"]
    n = len(x); mx, my = sum(x)/n, sum(y)/n
    r = (sum((a-mx)*(b-my) for a, b in zip(x, y))
         / (sum((a-mx)**2 for a in x) * sum((b-my)**2 for b in y)) ** .5)
    print(f"    r(hours, marks) = {r:.4f}")
