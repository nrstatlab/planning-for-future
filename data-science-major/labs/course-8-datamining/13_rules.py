"""Experiment 13 — Rule-based classification.

WEKA: rules/JRip (RIPPER), rules/PART, rules/ZeroR, rules/OneR.

Extracts the five weather rules of Unit 4 section 4.10 from a decision tree,
computes each rule's coverage and accuracy, and shows why ZeroR must always be
run first.
"""
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris, load_breast_cancer
from sklearn.model_selection import cross_val_score, StratifiedKFold
from weather import weather_frame

RULES = [
    ({"Outlook": "Overcast"},                      "Yes"),
    ({"Outlook": "Sunny", "Humidity": "Normal"},   "Yes"),
    ({"Outlook": "Sunny", "Humidity": "High"},     "No"),
    ({"Outlook": "Rain", "Wind": "Weak"},          "Yes"),
    ({"Outlook": "Rain", "Wind": "Strong"},        "No"),
]


def matches(row, antecedent):
    return all(row[k] == v for k, v in antecedent.items())


def rule_quality(df, antecedent, consequent, target="Play"):
    """Coverage = fraction of records the antecedent fires on.
       Accuracy = of those, the fraction with the right class."""
    covered = df[df.apply(lambda r: matches(r, antecedent), axis=1)]
    coverage = len(covered) / len(df)
    accuracy = (covered[target] == consequent).mean() if len(covered) else float("nan")
    return coverage, accuracy, len(covered)


def unit4_rules():
    df = weather_frame()
    print("  the five tree paths as rules (Unit 4 section 4.10)")

    total_covered = 0
    for ant, con in RULES:
        cov, acc, n = rule_quality(df, ant, con)
        conds = " AND ".join(f"{k}={v}" for k, v in ant.items())
        print(f"    IF {conds:38s} THEN {con:3s}  "
              f"coverage {cov:.4f} ({n:2d}/14)  accuracy {acc:.4f}")
        assert acc == 1.0, f"every tree-derived rule must be 100% accurate here"
        total_covered += n

    assert total_covered == 14, "the rules must be EXHAUSTIVE -- 14 records covered"

    # And MUTUALLY EXCLUSIVE: no record fires two rules.
    for _, row in df.iterrows():
        fired = [i for i, (a, _) in enumerate(RULES) if matches(row, a)]
        assert len(fired) == 1, f"record fired {len(fired)} rules, expected 1"

    print("       exhaustive (14/14 covered) and mutually exclusive (1 rule each)")
    print("       -- automatic, because tree paths PARTITION the space")


def rules_predict_correctly():
    df = weather_frame()

    def classify(row, default="Yes"):
        for ant, con in RULES:
            if matches(row, ant):
                return con
        return default                      # needed only if rules are not exhaustive

    predictions = df.apply(classify, axis=1)
    assert (predictions == df.Play).all(), "the rule set reproduces every label"
    print(f"  rule-set accuracy on the training data: "
          f"{(predictions == df.Play).mean():.4f}")


def zeror_baseline():
    """ALWAYS run ZeroR first. On imbalanced data it alone can look excellent."""
    print("\n  ZeroR baseline (WEKA: rules/ZeroR)")

    df = weather_frame()
    majority = df.Play.value_counts().idxmax()
    zeror = (df.Play == majority).mean()
    assert majority == "Yes" and round(zeror, 4) == round(9 / 14, 4)
    print(f"    weather: always predict '{majority}' -> {zeror:.4f}")

    for name, load in [("iris", load_iris), ("breast cancer", load_breast_cancer)]:
        X, y = load(return_X_y=True)
        cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=0)
        base = cross_val_score(DummyClassifier(strategy="most_frequent"), X, y, cv=cv).mean()
        tree = cross_val_score(DecisionTreeClassifier(random_state=0), X, y, cv=cv).mean()
        print(f"    {name:14s} ZeroR {base:.4f}   tree {tree:.4f}   "
              f"(+{tree - base:.4f})")
        assert tree > base, f"a classifier must beat the baseline on {name}"


def accuracy_paradox_in_one_click():
    """A 95/5 imbalance: ZeroR alone scores 95% and finds nothing."""
    rng = np.random.default_rng(0)
    n = 2000
    y = np.r_[np.zeros(1900), np.ones(100)].astype(int)
    X = rng.normal(0, 1, (n, 4))
    X[y == 1] += 0.3                       # a WEAK signal

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    base = cross_val_score(DummyClassifier(strategy="most_frequent"), X, y, cv=cv).mean()
    assert round(base, 4) == 0.95, base

    from sklearn.metrics import recall_score
    from sklearn.model_selection import cross_val_predict
    pred = cross_val_predict(DummyClassifier(strategy="most_frequent"), X, y, cv=cv)
    assert recall_score(y, pred) == 0.0, "95% accurate and it catches NOTHING"

    print(f"\n  accuracy paradox: ZeroR scores {base:.4f} accuracy "
          f"with {recall_score(y, pred):.4f} recall")
    print(f"       95% accuracy, zero minority-class detections -- which is why")
    print(f"       accuracy alone is worse than useless on imbalanced data")


def rule_ordering_matters():
    """When rules are NOT mutually exclusive, conflict resolution decides."""
    overlapping = [
        ({"Outlook": "Sunny"},                     "No"),    # general
        ({"Outlook": "Sunny", "Humidity": "Normal"}, "Yes"),  # specific
    ]
    row = {"Outlook": "Sunny", "Temperature": "Cool",
           "Humidity": "Normal", "Wind": "Weak", "Play": "Yes"}

    fired = [(a, c) for a, c in overlapping if matches(row, a)]
    assert len(fired) == 2, "this record fires BOTH rules"

    first_match = fired[0][1]                          # rule ordering
    most_specific = max(fired, key=lambda p: len(p[0]))[1]   # size ordering

    assert first_match == "No" and most_specific == "Yes"
    assert row["Play"] == "Yes", "size ordering gets it right here"

    print(f"\n  conflict: a record fires both rules")
    print(f"       rule ordering (first match) -> {first_match}")
    print(f"       size ordering (most specific) -> {most_specific}   <- correct")


def main():
    print("Experiment 13 -- Rule-based classification")
    unit4_rules()
    rules_predict_correctly()
    zeror_baseline()
    accuracy_paradox_in_one_click()
    rule_ordering_matters()
    print("\n  rule-based classification verified")


if __name__ == "__main__":
    main()
