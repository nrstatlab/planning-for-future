"""Practical 18 — Basic visualizations with matplotlib (and Seaborn, Plotly).

Runs under the Agg backend: it opens no window and writes PNG files to a
temporary directory, so it works on a server and in CI.

Seaborn and Plotly are imported CONDITIONALLY -- if either is absent the script
says so and skips that section rather than failing.
"""
import pathlib
import tempfile
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")               # MUST come before importing pyplot
import matplotlib.pyplot as plt

from fixtures import students


def four_plot_types(tmp):
    df = students()
    ds = df.loc[df.dept == "DS", "maths"]
    st = df.loc[df.dept == "Stats", "maths"]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # A HISTOGRAM shows the distribution of ONE CONTINUOUS variable.
    # The bars are bins and they TOUCH, because the axis is continuous.
    axes[0, 0].hist(df.maths, bins=5, color="#2b4c7e", edgecolor="white")
    axes[0, 0].set_title("Distribution of maths marks")
    axes[0, 0].set_xlabel("Marks")
    axes[0, 0].set_ylabel("Number of students")

    # A BAR CHART compares CATEGORIES. The bars have GAPS, because there is
    # nothing between 'DS' and 'Stats'.
    means = df.groupby("dept").maths.mean()
    axes[0, 1].bar(means.index, means.to_numpy(), color="#2b8a3e")
    axes[0, 1].set_title("Mean maths mark by department")
    axes[0, 1].set_xlabel("Department")
    axes[0, 1].set_ylabel("Mean marks")
    axes[0, 1].set_ylim(0, 100)          # bar charts START AT ZERO

    axes[1, 0].scatter(df.maths, df.stats, s=80, color="#c92a2a")
    axes[1, 0].set_title("Maths vs Statistics")
    axes[1, 0].set_xlabel("Maths marks")
    axes[1, 0].set_ylabel("Statistics marks")
    axes[1, 0].axhline(float(df.stats.mean()), color="grey", linestyle=":",
                       label="mean stats")
    axes[1, 0].legend()

    axes[1, 1].boxplot([ds.to_numpy(), st.to_numpy()],
                       tick_labels=["DS", "Stats"])
    axes[1, 1].set_title("Marks by department")
    axes[1, 1].set_xlabel("Department")
    axes[1, 1].set_ylabel("Marks")

    fig.tight_layout()
    out = tmp / "overview.png"
    fig.savefig(out, dpi=100, bbox_inches="tight")

    # Every axes must carry a title and BOTH labels -- an unlabelled axis
    # makes a chart unreadable, and this asserts it rather than saying it.
    for ax in axes.ravel():
        assert ax.get_title(), "every plot needs a title"
        assert ax.get_xlabel(), "every plot needs an x label"
        assert ax.get_ylabel(), "every plot needs a y label"

    assert axes[0, 1].get_ylim()[0] == 0, "a bar chart's y-axis starts at zero"

    plt.close(fig)
    assert out.exists() and out.stat().st_size > 1000

    print(f"  matplotlib: 4 subplots written to {out.name} "
          f"({out.stat().st_size // 1024} KB), all axes labelled")


def object_oriented_not_pyplot(tmp):
    """pyplot's hidden 'current figure' breaks the moment you have two."""
    figs = []
    for i, colour in enumerate(["#2b4c7e", "#2b8a3e"]):
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.plot([1, 2, 3], [i + 1, i + 2, i + 3], color=colour)
        ax.set_title(f"Chart {i}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        figs.append((fig, ax))

    # Each figure is a distinct object -- no hidden state to confuse.
    assert figs[0][0] is not figs[1][0]
    assert figs[0][1].get_title() == "Chart 0"
    assert figs[1][1].get_title() == "Chart 1"

    for i, (fig, _) in enumerate(figs):
        fig.savefig(tmp / f"chart{i}.png", dpi=80)
        plt.close(fig)

    assert (tmp / "chart0.png").exists() and (tmp / "chart1.png").exists()
    print("  the fig/ax interface keeps two charts separate; pyplot's hidden")
    print("       'current figure' does not -- and plt.close() avoids a leak")


def pandas_plotting(tmp):
    df = students()
    ax = df.plot(kind="scatter", x="maths", y="stats", figsize=(5, 4))
    ax.set_title("Pandas .plot returns a matplotlib Axes")
    assert ax.get_title()
    fig = ax.get_figure()
    fig.savefig(tmp / "pandas.png", dpi=80)
    plt.close(fig)

    ax2 = df.groupby("dept").maths.mean().plot(kind="bar", figsize=(4, 3))
    ax2.set_xlabel("Department")
    ax2.set_ylabel("Mean marks")
    plt.close(ax2.get_figure())

    assert (tmp / "pandas.png").exists()
    print("  df.plot() is a thin matplotlib wrapper and RETURNS an Axes, so you")
    print("       can customise it exactly as above")


def seaborn_section(tmp):
    try:
        import seaborn as sns
    except ImportError:
        print("  seaborn: NOT INSTALLED -- section skipped (not a failure)")
        return

    df = students()
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    sns.boxplot(data=df, x="dept", y="maths", ax=axes[0])
    axes[0].set_title("Marks by department")
    axes[0].set_xlabel("Department")
    axes[0].set_ylabel("Marks")

    sns.scatterplot(data=df, x="maths", y="stats", hue="dept", s=100, ax=axes[1])
    axes[1].set_title("Maths vs Statistics, coloured by department")
    axes[1].set_xlabel("Maths")
    axes[1].set_ylabel("Statistics")

    sns.heatmap(df[["maths", "stats"]].corr(), annot=True, cmap="coolwarm",
                center=0, vmin=-1, vmax=1, ax=axes[2])
    axes[2].set_title("Correlation")
    axes[2].set_xlabel("")
    axes[2].set_ylabel("")

    fig.tight_layout()
    out = tmp / "seaborn.png"
    fig.savefig(out, dpi=100, bbox_inches="tight")
    plt.close(fig)

    assert out.exists() and out.stat().st_size > 1000
    print(f"  seaborn {sns.__version__}: hue= groups by colour with no loop;")
    print(f"       heatmap(corr(), center=0) uses a DIVERGING map around a")
    print(f"       meaningful midpoint, which is the correct use of one")


def plotly_section(tmp):
    try:
        import plotly.express as px
    except ImportError:
        print("  plotly: NOT INSTALLED -- section skipped (not a failure)")
        return

    df = students()
    fig = px.scatter(df, x="maths", y="stats", color="dept",
                     hover_data=["name"], title="Maths vs Statistics")
    out = tmp / "interactive.html"
    fig.write_html(out)

    assert out.exists()
    size_kb = out.stat().st_size // 1024
    assert size_kb > 100, "plotly bundles a JavaScript library"

    print(f"  plotly: interactive.html is {size_kb} KB -- it EMBEDS a JS library")
    print(f"       fine on a web page, wrong in an email or a printed report")


def honest_charts():
    """Truncating a bar chart's y-axis exaggerates the difference."""
    a, b = 95.0, 100.0

    real_difference = (b - a) / a             # the honest figure
    truncated_ratio = (b - 90) / (a - 90)     # y-axis starting at 90

    assert round(real_difference, 3) == 0.053, "the real difference is 5.3%"
    assert truncated_ratio == 2.0, "truncated, one bar looks TWICE the other"

    print(f"  honesty: 95 vs 100 is a {real_difference:.1%} difference, but with the")
    print(f"       y-axis starting at 90 one bar is {truncated_ratio:.0f}x the")
    print(f"       other. A bar's LENGTH is the encoding, so it must start at 0.")


def main():
    print("Practical 18 -- Visualization")
    with tempfile.TemporaryDirectory() as d:
        tmp = pathlib.Path(d)
        four_plot_types(tmp)
        object_oriented_not_pyplot(tmp)
        pandas_plotting(tmp)
        seaborn_section(tmp)
        plotly_section(tmp)
    honest_charts()


if __name__ == "__main__":
    main()
