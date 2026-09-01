"""Experiment 4 — Data visualization techniques.

A plot cannot be asserted, but the numbers behind it can, and the point of a
plot is nearly always a number you could have missed. Each function here
computes what its chart shows and checks it; the images are written to output/.

The centrepiece is Anscombe's quartet, which is the single best argument for
plotting before modelling.
"""
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from fixtures import STUDY, churn, iris_frame

OUT = pathlib.Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

# Anscombe's quartet: four datasets, identical summary statistics.
ANSCOMBE = {
    "I":   ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
            [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    "II":  ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
            [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    "III": ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
            [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    "IV":  ([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8],
            [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]),
}


def anscombes_quartet():
    """Four datasets. Same mean, variance, correlation and regression line."""
    stats = {}
    for name, (xs, ys) in ANSCOMBE.items():
        x, y = np.array(xs, dtype=float), np.array(ys, dtype=float)
        slope, intercept = np.polyfit(x, y, 1)
        stats[name] = (x.mean(), y.mean(), y.var(ddof=1),
                       np.corrcoef(x, y)[0, 1], slope, intercept)

    # The agreement is close but not exact, and the precision differs per
    # statistic. Assert exactly what is true, not the folklore:
    #   mean x   exact       9.0000 in all four
    #   slope    3 decimals  0.50009, 0.50000, 0.49973, 0.49991
    #   mean y   2 decimals  7.5009, 7.5009, 7.5000, 7.5009
    #   icept    2 decimals  3.00009, 3.00091, 3.00245, 3.00173
    #   r        2 decimals  0.81642, 0.81624, 0.81629, 0.81652
    #   var y    1 decimal   4.1273, 4.1276, 4.1226, 4.1232
    for name, s in stats.items():
        assert round(s[0], 4) == 9.0000, (name, s[0])        # mean x -- exact
        assert round(s[4], 3) == 0.500, (name, s[4])         # slope
        assert round(s[1], 2) == 7.50, (name, s[1])          # mean y
        assert round(s[5], 2) == 3.00, (name, s[5])          # intercept
        assert round(s[3], 2) == 0.82, (name, s[3])          # correlation
        assert round(s[2], 1) == 4.1, (name, s[2])           # var y

    fig, axes = plt.subplots(2, 2, figsize=(7, 6))
    for ax, (name, (xs, ys)) in zip(axes.ravel(), ANSCOMBE.items()):
        ax.scatter(xs, ys, color="#0f4c81")
        xx = np.linspace(3, 20, 2)
        ax.plot(xx, 3.0 + 0.5 * xx, color="#dc2626", linewidth=1)
        ax.set_title(f"Anscombe {name}")
        ax.set_xlim(2, 20); ax.set_ylim(2, 14)
    fig.suptitle("Identical statistics, four different datasets")
    fig.tight_layout()
    fig.savefig(OUT / "04_anscombe.png", dpi=110)
    plt.close(fig)

    print("  set  mean x  mean y   var y     r    slope  intercept")
    for name, s in stats.items():
        print(f"   {name:3s} {s[0]:7.2f} {s[1]:7.2f} {s[2]:7.2f} {s[3]:6.3f} "
              f"{s[4]:7.3f} {s[5]:9.2f}")
    print("       mean x is IDENTICAL, the slope agrees to three decimals, and")
    print("       mean y, intercept and r to two -- yet the four")
    print("       datasets look nothing alike: I is a genuine linear")
    print("       relationship, II is a parabola, III is a line plus one")
    print("       outlier, IV is a vertical stack plus one leverage point.")
    print("       PLOT BEFORE YOU MODEL. Summary statistics cannot see shape")


def histogram_and_the_bin_count():
    """The same data, four bin counts, four different impressions."""
    rng = np.random.default_rng(0)
    data = np.concatenate([rng.normal(20, 3, 200), rng.normal(35, 3, 200)])

    def interior_peaks(bins):
        hist, _ = np.histogram(data, bins=bins)
        return sum(1 for i in range(1, len(hist) - 1)
                   if hist[i] > hist[i - 1] and hist[i] > hist[i + 1])

    found = {bins: interior_peaks(bins) for bins in (2, 5, 15, 30, 60)}

    assert len(data) == 400
    assert found[2] == 0, "two bins cannot show ANY interior structure"
    assert found[5] == 2 and found[15] == 2, "the two real modes"
    assert found[30] == 4 and found[60] == 15, found
    assert found[60] > 7 * found[15], "60 bins invents peaks that are not there"

    fig, axes = plt.subplots(1, 4, figsize=(12, 3))
    for ax, bins in zip(axes, (2, 5, 15, 60)):
        ax.hist(data, bins=bins, color="#0f4c81")
        ax.set_title(f"{bins} bins")
    fig.tight_layout()
    fig.savefig(OUT / "04_histogram_bins.png", dpi=110)
    plt.close(fig)

    print("  a genuinely BIMODAL sample (peaks at 20 and 35), by bin count:")
    for bins, peaks in found.items():
        verdict = ("no structure visible" if peaks == 0 else
                   "correct" if peaks == 2 else "SPURIOUS peaks from noise")
        print(f"    {bins:2d} bins -> {peaks:2d} interior peak(s)   {verdict}")
    print("       2 bins shows nothing; 5 and 15 find both real modes; 60 finds")
    print("       FIFTEEN, which are sampling noise. The bin count is a CHOICE")
    print("       that changes the conclusion in both directions, which is why")
    print("       a histogram should never be the only thing you look at")


def boxplot_finds_outliers():
    """The IQR rule, computed -- Course 4's method, applied."""
    x = pd.Series([10, 12, 11, 13, 12, 11, 14, 12, 250])
    q1, q3 = x.quantile(0.25), x.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = x[(x < lo) | (x > hi)]

    assert q1 == 11.0 and q3 == 13.0 and iqr == 2.0
    assert lo == 8.0 and hi == 16.0
    assert outliers.tolist() == [250]

    # The mean is destroyed by the outlier; the median is not.
    assert round(x.mean(), 4) == 38.3333
    assert x.median() == 12.0

    print(f"  Q1 {q1}, Q3 {q3}, IQR {iqr}  ->  fences [{lo}, {hi}]")
    print(f"  outliers: {outliers.tolist()}")
    print(f"  mean {x.mean():.4f} vs median {x.median():.1f}")
    print("       one value moved the mean by 26 and the median by 0. A box")
    print("       plot shows both the outlier and that robustness at once")


def scatter_matrix_and_correlation():
    """Which iris features are redundant -- the question a pair plot answers."""
    df, data = iris_frame()
    features = list(data.feature_names)
    corr = data.data.corr()

    petal = corr.loc["petal length (cm)", "petal width (cm)"]
    sepal_petal = corr.loc["sepal length (cm)", "petal length (cm)"]
    sepal_w = corr.loc["sepal length (cm)", "sepal width (cm)"]

    assert round(petal, 4) == 0.9629, round(petal, 4)
    assert round(sepal_petal, 4) == 0.8718, round(sepal_petal, 4)
    assert round(sepal_w, 4) == -0.1176, round(sepal_w, 4)
    assert petal > sepal_petal > abs(sepal_w)

    print("  iris feature correlations:")
    print(f"    petal length ~ petal width  {petal:+.4f}   <- nearly redundant")
    print(f"    sepal length ~ petal length {sepal_petal:+.4f}")
    print(f"    sepal length ~ sepal width  {sepal_w:+.4f}   <- almost none")
    print("       petal length and width carry nearly the same information,")
    print("       which is exactly why PCA compressed four columns to two")


def class_balance_should_be_plotted_first():
    """The first plot to make on any classification problem."""
    df = churn()
    counts = df["churned"].value_counts().sort_index()
    rate = df["churned"].mean()

    assert counts.tolist() == [340, 60]
    assert round(rate, 4) == 0.15
    assert round(counts[0] / len(df), 4) == 0.85, "the majority-class baseline"

    print(f"  class balance: {counts[0]} negative, {counts[1]} positive "
          f"({rate * 100:.0f}% positive)")
    print(f"  a model predicting 'never' scores {counts[0] / len(df) * 100:.0f}% accuracy")
    print("       plot this FIRST. It tells you what accuracy will mean before")
    print("       you fit anything, and it is one line of code")


def line_plot_needs_ordered_x():
    df = STUDY.sort_values("hours")
    assert df["hours"].is_monotonic_increasing
    assert df["score"].is_monotonic_increasing

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.scatter(df["hours"], df["score"], color="#0f4c81")
    m, c = np.polyfit(df["hours"], df["score"], 1)
    ax.plot(df["hours"], m * df["hours"] + c, color="#dc2626")
    ax.set_xlabel("hours studied"); ax.set_ylabel("exam score")
    ax.set_title(f"score = {c:.2f} + {m:.2f} x hours")
    fig.tight_layout()
    fig.savefig(OUT / "04_scatter_fit.png", dpi=110)
    plt.close(fig)

    assert round(m, 4) == 4.3030 and round(c, 4) == 43.0303

    print(f"  study data: fitted line score = {c:.4f} + {m:.4f} x hours")
    print("       scatter plot for a RELATIONSHIP, with the fit drawn over it.")
    print("       Points only -- never join scattered points with lines")


def main():
    print("Experiment 4 -- Data visualization techniques")
    anscombes_quartet()
    histogram_and_the_bin_count()
    boxplot_finds_outliers()
    scatter_matrix_and_correlation()
    class_balance_should_be_plotted_first()
    line_plot_needs_ordered_x()
    print(f"  charts written to {OUT.name}/")


if __name__ == "__main__":
    main()
