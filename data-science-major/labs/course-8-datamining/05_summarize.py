"""Experiment 5 — Summarize and visualize with class-wise comparison.

WEKA: the Preprocess attribute panel, Visualize All, and the Visualize tab's
scatter-plot matrix coloured by class.

This prints the numbers behind those pictures, and asserts the separation that
makes petal length the most informative attribute.
"""
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris


def load():
    d = load_iris(as_frame=True)
    df = d.frame.drop(columns="target")          # the numeric label is not an attribute
    df["species"] = pd.Categorical.from_codes(d.target, d.target_names)
    return df


def attribute_panel(df):
    """What WEKA shows when you click each attribute."""
    print("  attribute summary (WEKA Preprocess panel)")
    for col in df.columns[:-1]:
        s = df[col]
        print(f"    {col:20s} min={s.min():5.2f} max={s.max():5.2f} "
              f"mean={s.mean():6.4f} sd={s.std():6.4f} missing={int(s.isna().sum())}")
    counts = df.species.value_counts().to_dict()
    assert counts == {"setosa": 50, "versicolor": 50, "virginica": 50}, counts
    print(f"    species              {counts}")


def class_wise_comparison(df):
    """The numeric form of 'colour the histogram by class'."""
    stats = df.groupby("species", observed=True).agg(["mean", "std"])
    print("\n  class-wise means")
    for col in df.columns[:-1]:
        means = [f"{stats[(col, 'mean')][s]:.3f}" for s in ["setosa", "versicolor", "virginica"]]
        print(f"    {col:20s} setosa {means[0]}  versicolor {means[1]}  virginica {means[2]}")
    return stats


def separation(df):
    """Petal length separates setosa COMPLETELY -- which is why it has the
    highest information gain in Experiment 4."""
    setosa = df[df.species == "setosa"]["petal length (cm)"]
    others = df[df.species != "setosa"]["petal length (cm)"]

    assert setosa.max() < others.min(), "setosa's petals do not overlap the others at all"
    gap = others.min() - setosa.max()
    assert round(float(gap), 2) == 1.10, gap

    # Sepal width, by contrast, overlaps heavily.
    sw_setosa = df[df.species == "setosa"]["sepal width (cm)"]
    sw_others = df[df.species != "setosa"]["sepal width (cm)"]
    assert sw_setosa.min() < sw_others.max() and sw_others.min() < sw_setosa.max(), \
        "sepal width overlaps -- which is why it ranks last"

    print(f"\n  separation: setosa petal length max {setosa.max():.1f} < "
          f"others min {others.min():.1f} -- a clean gap of {gap:.2f} cm")
    print(f"       a single threshold at 2.5 cm classifies setosa perfectly")

    threshold = 2.45
    predicted_setosa = df["petal length (cm)"] < threshold
    assert (predicted_setosa == (df.species == "setosa")).all(), \
        "one rule, 100% accurate for setosa"


def correlations(df):
    c = df[df.columns[:-1]].corr()
    petal = c.loc["petal length (cm)", "petal width (cm)"]
    assert petal > 0.95, "petal length and width are nearly redundant"
    print(f"\n  correlation: petal length vs width = {petal:.4f}")
    print(f"       nearly redundant -- feature SELECTION would drop one")


def main():
    print("Experiment 5 -- Summarize and visualize")
    df = load()
    attribute_panel(df)
    class_wise_comparison(df)
    separation(df)
    correlations(df)
    print("\n  summary statistics verified")


if __name__ == "__main__":
    main()
