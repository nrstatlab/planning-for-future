"""Experiment 7 — Logistic regression.

Reproduces unit-2.md section 2.5's baseline argument and unit-3.md section
3.6's odds-ratio interpretation. The headline result is the one worth
remembering: a model that predicts nobody churns scores 0.85 accuracy and
0.00 recall.
"""
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score,
                             roc_curve)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from fixtures import RANDOM_STATE, churn

DF = churn()
FEATURES = ["tenure_months", "support_calls", "irrelevant"]
X = DF[FEATURES].to_numpy()
Y = DF["churned"].to_numpy()
XTR, XTE, YTR, YTE = train_test_split(
    X, Y, test_size=0.25, random_state=RANDOM_STATE, stratify=Y)


def the_baseline_first():
    """unit-2.md 2.5: fit a DummyClassifier before anything else."""
    dummy = DummyClassifier(strategy="most_frequent").fit(XTR, YTR)
    pred = dummy.predict(XTE)

    acc = accuracy_score(YTE, pred)
    rec = recall_score(YTE, pred, zero_division=0)

    assert round(DF["churned"].mean(), 4) == 0.15
    assert len(YTE) == 100 and int(YTE.sum()) == 15
    assert round(acc, 4) == 0.85, acc
    assert rec == 0.0
    assert set(pred) == {0}, "it predicts the majority class and nothing else"

    print(f"  base rate: {DF['churned'].mean() * 100:.0f}% positive "
          f"({int(YTE.sum())} of {len(YTE)} in the test set)")
    print(f"  DummyClassifier('most_frequent'):")
    print(f"    accuracy {acc:.4f}   recall {rec:.4f}")
    print("       85% accurate, and it identifies NOT ONE churner. Any accuracy")
    print("       you report from here must be compared against this number")
    return acc


def logistic_regression_fitted(dummy_accuracy):
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(random_state=RANDOM_STATE)).fit(XTR, YTR)
    pred = model.predict(XTE)
    proba = model.predict_proba(XTE)[:, 1]

    acc = accuracy_score(YTE, pred)
    prec = precision_score(YTE, pred, zero_division=0)
    rec = recall_score(YTE, pred)
    f1 = f1_score(YTE, pred)
    auc = roc_auc_score(YTE, proba)
    tn, fp, fn, tp = confusion_matrix(YTE, pred).ravel()

    assert round(acc, 4) == 0.94
    assert round(prec, 4) == 0.8462
    assert round(rec, 4) == 0.7333
    assert round(f1, 4) == 0.7857
    assert round(auc, 4) == 0.9882
    assert (tn, fp, fn, tp) == (83, 2, 4, 11), (tn, fp, fn, tp)
    assert tp + fn == 15 and tn + fp == 85

    # The metrics, recomputed by hand from the four counts.
    assert round(tp / (tp + fp), 4) == round(prec, 4)
    assert round(tp / (tp + fn), 4) == round(rec, 4)
    assert round((tp + tn) / len(YTE), 4) == round(acc, 4)

    print(f"  confusion matrix: TP {tp}  FP {fp}  FN {fn}  TN {tn}")
    print(f"    accuracy  {acc:.4f}   ({tp}+{tn})/{len(YTE)}")
    print(f"    precision {prec:.4f}   {tp}/{tp + fp}")
    print(f"    recall    {rec:.4f}   {tp}/{tp + fn}")
    print(f"    F1        {f1:.4f}")
    print(f"    AUC       {auc:.4f}")
    print(f"  against the baseline: accuracy {dummy_accuracy:.4f} -> {acc:.4f}, "
          f"a gain of {acc - dummy_accuracy:+.4f}")
    print(f"                        AUC      0.5000 -> {auc:.4f}")
    print("       accuracy COMPRESSES the difference into 9 points. AUC shows")
    print("       it properly, which is why AUC survives imbalance better")
    return model, proba


def odds_ratios(model):
    """unit-3.md 3.6: the model is linear in the LOG-ODDS."""
    logistic = model[-1]
    coefs = logistic.coef_[0]
    odds_ratio = np.exp(coefs)

    # Features were standardised, so a coefficient is 'per 1 sd'.
    named = dict(zip(FEATURES, zip(coefs, odds_ratio)))

    assert named["support_calls"][0] > 0, "more calls -> MORE likely to churn"
    assert named["tenure_months"][0] < 0, "longer tenure -> LESS likely"
    assert named["support_calls"][1] > 1.0 and named["tenure_months"][1] < 1.0
    assert abs(named["irrelevant"][0]) < 0.5, \
        "the noise feature got a coefficient near zero, as it should"

    print(f"  {'feature':16s} {'coefficient':>12s} {'odds ratio':>12s}  reading")
    for name, (b, orr) in named.items():
        direction = ("x{:.2f} odds per +1 sd".format(orr) if orr > 1
                     else "x{:.2f} odds per +1 sd".format(orr))
        print(f"  {name:16s} {b:12.4f} {orr:12.4f}  {direction}")
    print("       coefficients are in LOG-ODDS; exponentiate for an odds ratio.")
    print(f"       support_calls: e^{named['support_calls'][0]:.4f} = "
          f"{named['support_calls'][1]:.4f}, so one extra standard deviation of")
    print(f"       calls multiplies the ODDS of churning by "
          f"{named['support_calls'][1]:.2f}")
    print("       ODDS ARE NOT PROBABILITY: odds of 2.0 means p = 2/3")


def the_threshold_is_a_choice(proba):
    """Moving the cut-off trades precision against recall."""
    rows = []
    for t in (0.10, 0.30, 0.50, 0.70, 0.90):
        pred = (proba >= t).astype(int)
        rows.append((t,
                     accuracy_score(YTE, pred),
                     precision_score(YTE, pred, zero_division=0),
                     recall_score(YTE, pred),
                     f1_score(YTE, pred, zero_division=0)))

    at_50 = [r for r in rows if r[0] == 0.50][0]
    at_10 = [r for r in rows if r[0] == 0.10][0]
    at_90 = [r for r in rows if r[0] == 0.90][0]

    assert round(at_50[1], 4) == 0.94
    assert at_10[3] > at_50[3], "a lower threshold catches MORE churners"
    assert at_10[2] < at_50[2], "at the cost of precision"
    assert at_90[2] >= at_50[2], "a higher threshold is more precise"
    assert at_90[3] <= at_50[3], "and catches fewer"

    print(f"    {'threshold':>10} {'accuracy':>9} {'precision':>10} "
          f"{'recall':>8} {'F1':>7}")
    for t, a, p, r, f in rows:
        mark = "  <- the default" if t == 0.50 else ""
        print(f"    {t:10.2f} {a:9.4f} {p:10.4f} {r:8.4f} {f:7.4f}{mark}")
    print("       ONE model, five different classifiers. The 0.5 cut-off is a")
    print("       convention, not part of the model. Lower it to catch more")
    print("       churners; raise it to be surer of the ones you flag.")
    print("       Choose it from the COST of each error, not from habit")


def roc_curve_endpoints(proba):
    """The curve every threshold traces out."""
    fpr, tpr, thresholds = roc_curve(YTE, proba)
    auc = roc_auc_score(YTE, proba)

    assert round(fpr[0], 6) == 0.0 and round(tpr[0], 6) == 0.0
    assert round(fpr[-1], 6) == 1.0 and round(tpr[-1], 6) == 1.0
    assert round(auc, 4) == 0.9882
    assert auc > 0.5, "0.5 would be a coin flip"

    print(f"  ROC runs from (0,0) to (1,1) through {len(thresholds)} thresholds")
    print(f"  AUC {auc:.4f}   (0.5 = random, 1.0 = perfect or leaking)")
    print("       AUC is THRESHOLD-INDEPENDENT, which is exactly why it is")
    print("       reported on imbalanced problems where accuracy is not")


def main():
    print("Experiment 7 -- Logistic regression")
    dummy_accuracy = the_baseline_first()
    model, proba = logistic_regression_fitted(dummy_accuracy)
    odds_ratios(model)
    print("  moving the decision threshold:")
    the_threshold_is_a_choice(proba)
    roc_curve_endpoints(proba)


if __name__ == "__main__":
    main()
