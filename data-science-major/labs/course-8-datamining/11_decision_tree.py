"""Experiment 11 — Decision tree (WEKA's J48 is C4.5).

Reproduces Unit 4 section 4.5's hand-traced ID3 calculation EXACTLY, then shows
overfitting on iris.

The entropies and gains asserted here are the numbers written out in the notes.
If either changes, this fails.
"""
import math
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from weather import weather_frame


def entropy(*counts):
    """Shannon entropy in BITS. Note 0 log 0 is taken as 0."""
    n = sum(counts)
    return -sum((c / n) * math.log2(c / n) for c in counts if c > 0)


def info_gain(df, attribute, target="Play"):
    """Gain(D, A) = Entropy(D) - sum_v (|Dv|/|D|) Entropy(Dv)."""
    total = len(df)
    before = entropy(*df[target].value_counts().tolist())
    after = sum(
        len(sub) / total * entropy(*sub[target].value_counts().tolist())
        for _, sub in df.groupby(attribute)
    )
    return before - after


def split_info(df, attribute):
    """Entropy of the PARTITION SIZES -- C4.5's normaliser."""
    total = len(df)
    return entropy(*[len(sub) for _, sub in df.groupby(attribute)])


def unit4_id3_trace():
    df = weather_frame()
    assert (df.Play == "Yes").sum() == 9 and (df.Play == "No").sum() == 5

    root_entropy = entropy(9, 5)
    assert round(root_entropy, 4) == 0.9403, root_entropy

    gains = {a: round(info_gain(df, a), 4) for a in df.columns[:-1]}
    assert gains == {"Outlook": 0.2467, "Temperature": 0.0292,
                     "Humidity": 0.1518, "Wind": 0.0481}, gains
    assert max(gains, key=gains.get) == "Outlook", "Outlook must be the root"

    # Overcast is already pure -- a leaf with no further splitting.
    overcast = df[df.Outlook == "Overcast"]
    assert set(overcast.Play) == {"Yes"} and len(overcast) == 4

    # Sunny branch: Humidity splits it perfectly (gain == the branch entropy).
    sunny = df[df.Outlook == "Sunny"]
    assert round(entropy(2, 3), 4) == 0.9710
    sg = {a: round(info_gain(sunny, a), 4) for a in ["Temperature", "Humidity", "Wind"]}
    assert sg == {"Temperature": 0.5710, "Humidity": 0.9710, "Wind": 0.0200}, sg

    # Rain branch: Wind splits it perfectly.
    rain = df[df.Outlook == "Rain"]
    rg = {a: round(info_gain(rain, a), 4) for a in ["Temperature", "Humidity", "Wind"]}
    assert rg == {"Temperature": 0.0200, "Humidity": 0.0200, "Wind": 0.9710}, rg

    print(f"  ID3: root entropy {root_entropy:.4f}; gains {gains}")
    print(f"       root = Outlook (0.2467); Sunny -> Humidity; Rain -> Wind")


def unit4_gain_ratio():
    """Section 4.6: C4.5's gain ratio, and the many-valued-attribute bias."""
    df = weather_frame()

    ratios = {}
    for a in df.columns[:-1]:
        ratios[a] = round(info_gain(df, a) / split_info(df, a), 4)
    assert ratios == {"Outlook": 0.1564, "Temperature": 0.0188,
                      "Humidity": 0.1518, "Wind": 0.0488}, ratios
    assert max(ratios, key=ratios.get) == "Outlook"

    # Add a unique identifier: 14 pure singleton branches, the MAXIMUM gain.
    df2 = df.copy()
    df2["Day"] = range(1, 15)
    day_gain = info_gain(df2, "Day")
    assert round(day_gain, 4) == 0.9403, "an identifier achieves the maximum gain"
    assert round(split_info(df2, "Day"), 4) == round(math.log2(14), 4) == 3.8074

    day_ratio = day_gain / split_info(df2, "Day")
    assert round(day_ratio, 4) == 0.2470

    # The honest point from the notes: gain ratio REDUCES but does not
    # ELIMINATE the bias -- Day still outranks Outlook.
    assert day_ratio > ratios["Outlook"], \
        "the notes state gain ratio does not fully fix the bias"

    print(f"  Gain ratio: Outlook {ratios['Outlook']}, but a Day identifier "
          f"still scores {day_ratio:.4f} -- reduced, not eliminated")


def sklearn_tree_agrees():
    """scikit-learn with criterion='entropy' must pick the same root."""
    df = weather_frame()
    X = pd.get_dummies(df.drop(columns="Play"))
    y = (df.Play == "Yes").astype(int)

    clf = DecisionTreeClassifier(criterion="entropy", random_state=0).fit(X, y)
    text = export_text(clf, feature_names=list(X.columns))
    root = text.splitlines()[0]
    assert "Outlook_Overcast" in root or "Outlook" in root, \
        f"the first split should involve Outlook, got: {root}"

    assert clf.score(X, y) == 1.0, "an unpruned tree memorises the training set"
    print(f"  sklearn tree: first split {root.strip()}; training accuracy 1.00")
    print("       (perfect training accuracy is the SIGNAL of overfitting)")


def overfitting_curve():
    """Section 4.8: training accuracy rises with depth while test accuracy does not."""
    X, y = load_iris(return_X_y=True)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.4, random_state=42,
                                          stratify=y)
    rows = []
    for depth in range(1, 11):
        t = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(Xtr, ytr)
        rows.append((depth, t.score(Xtr, ytr), t.score(Xte, yte)))

    train = [r[1] for r in rows]
    assert train == sorted(train), "training accuracy must be non-decreasing with depth"
    assert train[-1] == 1.0, "a deep enough tree memorises the training set"

    best = max(rows, key=lambda r: r[2])
    gap = train[-1] - rows[-1][2]
    assert gap > 0, "the train/test gap IS the overfitting"

    print("  depth  train   test")
    for d, tr, te in rows:
        print(f"    {d:2d}   {tr:.3f}  {te:.3f}" + ("   <- best test" if (d, tr, te) == best else ""))
    print(f"       final train/test gap {gap:.3f} -- deeper is not better")


def main():
    print("Experiment 11 -- Decision trees")
    unit4_id3_trace()
    unit4_gain_ratio()
    sklearn_tree_agrees()
    overfitting_curve()
    print("  all Unit 4 tree calculations reproduced")


if __name__ == "__main__":
    main()
