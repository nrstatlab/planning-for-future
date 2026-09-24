"""Experiment 8 — Decision tree classification.

Course 8 traced ID3's entropy and information gain by hand. This experiment
asks the machine-learning question instead: is the tree overfitting, and how
would you know? unit-2.md section 2.3's max_depth table is reproduced here.
"""
import numpy as np
from sklearn.model_selection import (StratifiedKFold, cross_val_score,
                                     train_test_split)
from sklearn.tree import DecisionTreeClassifier, export_text

from fixtures import RANDOM_STATE, churn, iris_frame

DF = churn()
FEATURES = ["tenure_months", "support_calls", "irrelevant"]
X = DF[FEATURES].to_numpy()
Y = DF["churned"].to_numpy()
XTR, XTE, YTR, YTE = train_test_split(
    X, Y, test_size=0.25, random_state=RANDOM_STATE, stratify=Y)


def entropy_and_gain_by_hand():
    """Course 8's arithmetic, verified -- so the two courses agree."""
    def entropy(counts):
        total = sum(counts)
        return -sum((c / total) * np.log2(c / total) for c in counts if c)

    # A 9-yes / 5-no parent, the classic worked example.
    parent = entropy([9, 5])
    assert round(parent, 4) == 0.9403, round(parent, 4)

    # Split into (2 yes, 3 no), (4 yes, 0 no), (3 yes, 2 no).
    children = [([2, 3], 5), ([4, 0], 4), ([3, 2], 5)]
    weighted = sum(n / 14 * entropy(c) for c, n in children)
    gain = parent - weighted

    assert round(entropy([4, 0]), 10) == 0.0, "a pure node has ZERO entropy"
    assert round(weighted, 4) == 0.6935, round(weighted, 4)
    assert round(gain, 4) == 0.2467, round(gain, 4)

    print(f"  parent entropy (9 yes, 5 no)      {parent:.4f}")
    print(f"  weighted child entropy            {weighted:.4f}")
    print(f"  information gain                  {gain:.4f}")
    print("       0.2467 is exactly Course 8's Outlook gain. A PURE node has")
    print("       entropy 0, which is what the tree is driving toward")


def depth_controls_overfitting():
    """unit-2.md 2.3's table, reproduced exactly."""
    rows = []
    for depth in (1, 2, 3, 5, 10, None):
        tree = DecisionTreeClassifier(max_depth=depth,
                                      random_state=RANDOM_STATE).fit(XTR, YTR)
        rows.append((depth, tree.score(XTR, YTR), tree.score(XTE, YTE),
                     tree.get_depth(), tree.get_n_leaves()))

    by_depth = {d: (tr, te) for d, tr, te, _, _ in rows}
    assert round(by_depth[1][0], 4) == 0.9533 and round(by_depth[1][1], 4) == 0.9200
    assert round(by_depth[3][0], 4) == 0.9800 and round(by_depth[3][1], 4) == 0.9400
    assert round(by_depth[5][0], 4) == 0.9967 and round(by_depth[5][1], 4) == 0.9500
    assert by_depth[10][0] == 1.0 and by_depth[None][0] == 1.0
    assert round(by_depth[10][1], 4) == 0.9400
    assert by_depth[None][1] < by_depth[5][1], \
        "the unrestricted tree generalises WORSE than the depth-5 tree"

    print(f"    {'max_depth':>10} {'train':>8} {'test':>8} {'gap':>8} "
          f"{'depth':>6} {'leaves':>7}")
    for depth, tr, te, actual, leaves in rows:
        mark = "  <- best test" if te == max(r[2] for r in rows) else ""
        print(f"    {str(depth):>10} {tr:8.4f} {te:8.4f} {tr - te:+8.4f} "
              f"{actual:6d} {leaves:7d}{mark}")
    print("       training accuracy reaches a PERFECT 1.0000 and test accuracy")
    print("       FALLS. The tree memorised the training set including its")
    print("       noise. A training accuracy of 1.0 is a warning, not a result")


def a_shallow_tree_is_readable():
    """The reason to use trees at all: you can read the rules."""
    tree = DecisionTreeClassifier(max_depth=2,
                                  random_state=RANDOM_STATE).fit(XTR, YTR)
    rules = export_text(tree, feature_names=FEATURES)

    assert "support_calls" in rules
    assert rules.count("class:") >= 3
    assert tree.get_n_leaves() <= 4

    print("  a depth-2 tree, as rules:")
    for line in rules.strip().splitlines():
        print(f"    {line}")
    print("       this is why a shallow tree is chosen when a decision must be")
    print("       EXPLAINED. No other model in the course reads like this")


def feature_importance_and_the_noise_column():
    """The irrelevant feature should score near zero -- and mostly does."""
    tree = DecisionTreeClassifier(max_depth=3,
                                  random_state=RANDOM_STATE).fit(XTR, YTR)
    importance = dict(zip(FEATURES, tree.feature_importances_))

    assert round(sum(importance.values()), 10) == 1.0, "importances sum to 1"
    assert importance["support_calls"] > importance["irrelevant"]
    assert importance["support_calls"] > 0.5, importance

    print("  feature importances (depth-3 tree):")
    for name, value in sorted(importance.items(), key=lambda kv: -kv[1]):
        print(f"    {name:16s} {value:.4f}  {'#' * int(value * 40)}")
    print("       the two real features dominate. Impurity importance is biased")
    print("       toward continuous and high-cardinality features, so prefer")
    print("       PERMUTATION importance when the ranking matters")


def cross_validation_beats_one_split():
    """unit-2.md 2.2: a single split could report anything in a wide range."""
    cv = StratifiedKFold(5, shuffle=True, random_state=RANDOM_STATE)
    scores = cross_val_score(
        DecisionTreeClassifier(max_depth=3, random_state=RANDOM_STATE),
        X, Y, cv=cv)

    assert len(scores) == 5
    assert [round(s, 4) for s in scores] == [0.975, 0.9625, 0.925, 0.9, 0.95]
    assert round(scores.mean(), 4) == 0.9425
    assert round(scores.std(), 4) == 0.0269
    assert scores.max() - scores.min() > 0.07

    print(f"  5-fold CV, depth 3: {[round(s, 4) for s in scores]}")
    print(f"    mean {scores.mean():.4f}   sd {scores.std():.4f}   "
          f"range {scores.min():.4f} to {scores.max():.4f}")
    print("       a single train/test split could have reported anything from")
    print("       0.90 to 0.975. That spread is why one split is not evidence")
    print("       and why you quote mean +/- sd")


def iris_tree():
    """The other standard dataset, for comparison with experiment 11."""
    _, data = iris_frame()
    Xi, yi = data.data.to_numpy(), data.target
    xtr, xte, ytr, yte = train_test_split(
        Xi, yi, test_size=0.3, random_state=RANDOM_STATE, stratify=yi)
    tree = DecisionTreeClassifier(max_depth=3,
                                  random_state=RANDOM_STATE).fit(xtr, ytr)

    assert round(tree.score(xte, yte), 4) == 0.9778, tree.score(xte, yte)
    assert tree.get_n_leaves() <= 5

    print(f"  iris, depth-3 tree: test accuracy {tree.score(xte, yte):.4f} "
          f"with {tree.get_n_leaves()} leaves")
    print("       three species separated by at most three questions")


def main():
    print("Experiment 8 -- Decision tree classification")
    entropy_and_gain_by_hand()
    print("  max_depth against overfitting:")
    depth_controls_overfitting()
    a_shallow_tree_is_readable()
    feature_importance_and_the_noise_column()
    cross_validation_beats_one_split()
    iris_tree()


if __name__ == "__main__":
    main()
