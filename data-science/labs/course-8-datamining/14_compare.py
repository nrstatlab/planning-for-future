"""Experiment 14 — Compare classifiers: confusion matrix, accuracy, ROC/AUC.

WEKA: run each classifier under the same cross-validation, then use the
Experimenter's Paired T-Tester. Visualize threshold curve gives the ROC.

Reproduces Unit 4 section 4.9's spam matrix and Practice Problem 2's medical
screening example -- the base rate fallacy -- exactly.
"""
import numpy as np
from scipy import stats
from sklearn.datasets import load_breast_cancer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, roc_auc_score, roc_curve)
from sklearn.model_selection import (StratifiedKFold, cross_val_score,
                                     cross_val_predict)
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


def metrics_from_counts(tp, fp, fn, tn):
    total = tp + fp + fn + tn
    precision = tp / (tp + fp) if tp + fp else float("nan")
    recall = tp / (tp + fn) if tp + fn else float("nan")
    return {
        "accuracy": (tp + tn) / total,
        "precision": precision,
        "recall": recall,
        "specificity": tn / (tn + fp) if tn + fp else float("nan"),
        "f1": 2 * precision * recall / (precision + recall)
              if precision + recall else 0.0,
        "fpr": fp / (fp + tn) if fp + tn else float("nan"),
    }


def unit4_spam_matrix():
    """Section 4.9: 1000 emails, 200 spam, 180 flagged, 150 correctly."""
    tp, fp, fn, tn = 150, 30, 50, 770
    assert tp + fn == 200 and fp + tn == 800 and tp + fp == 180

    m = metrics_from_counts(tp, fp, fn, tn)
    assert round(m["accuracy"], 4) == 0.92
    assert round(m["precision"], 4) == 0.8333
    assert round(m["recall"], 4) == 0.75
    assert round(m["specificity"], 4) == 0.9625
    assert round(m["f1"], 4) == 0.7895
    assert round(m["fpr"], 4) == 0.0375

    print(f"  4.9 spam: accuracy {m['accuracy']:.4f} looks fine, but recall "
          f"{m['recall']:.4f}")
    print(f"       means 1 spam in 4 reaches the inbox, and precision "
          f"{m['precision']:.4f}")
    print(f"       means 17% of the spam folder is REAL email")


def practice_2_base_rate():
    """Practice Problem 2: 1% prevalence, 95% sensitivity, 90% specificity."""
    diseased, healthy = 100, 9900
    tp = round(0.95 * diseased)
    fn = diseased - tp
    tn = round(0.90 * healthy)
    fp = healthy - tn
    assert (tp, fn, tn, fp) == (95, 5, 8910, 990)

    m = metrics_from_counts(tp, fp, fn, tn)
    assert round(m["accuracy"], 4) == 0.9005
    assert round(m["precision"], 4) == 0.0876
    assert round(m["recall"], 4) == 0.95
    # 0.1603 from exact counts. The notes show 0.1604 because they combine the
    # 4-decimal rounded precision and recall, which is what you do by hand.
    assert round(m["f1"], 4) == 0.1603, m["f1"]

    print(f"\n  Practice 2 base rate fallacy:")
    print(f"       accuracy {m['accuracy']:.4f}, recall {m['recall']:.4f} -- "
          f"both excellent")
    print(f"       precision {m['precision']:.4f} -- fewer than 1 positive in 11")
    print(f"       is real, because 10% of 9900 healthy people is {fp} false alarms")
    print(f"       F1 {m['f1']:.4f} reflects what accuracy conceals")


def compare_five():
    """Five classifiers, one stratified 10-fold split, one table."""
    X, y = load_breast_cancer(return_X_y=True)
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

    models = {
        "ZeroR":      DummyClassifier(strategy="most_frequent"),
        "NaiveBayes": GaussianNB(),
        "J48 (tree)": DecisionTreeClassifier(random_state=0),
        "IBk (k-NN)": make_pipeline(StandardScaler(), KNeighborsClassifier(5)),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=0),
    }

    print("\n  classifier comparison, stratified 10-fold CV")
    print("    model          acc     prec    recall   F1      AUC")
    results = {}
    for name, model in models.items():
        pred = cross_val_predict(model, X, y, cv=cv)
        scores = cross_val_score(model, X, y, cv=cv)
        try:
            proba = cross_val_predict(model, X, y, cv=cv, method="predict_proba")[:, 1]
            auc = roc_auc_score(y, proba)
        except Exception:
            auc = float("nan")
        results[name] = scores
        print(f"    {name:14s} {accuracy_score(y, pred):.4f}  "
              f"{precision_score(y, pred, zero_division=0):.4f}  "
              f"{recall_score(y, pred):.4f}  {f1_score(y, pred):.4f}  {auc:.4f}")

    for name, scores in results.items():
        if name != "ZeroR":
            assert scores.mean() > results["ZeroR"].mean(), \
                f"{name} must beat the ZeroR baseline"

    return results


def paired_significance(results):
    """A 2% difference on one split is noise. Test it properly."""
    print("\n  paired t-tests against RandomForest (WEKA: Paired T-Tester)")
    best = results["RandomForest"]
    for name, scores in results.items():
        if name == "RandomForest":
            continue
        t, p = stats.ttest_rel(best, scores)
        verdict = "significantly better" if p < 0.05 else "NOT significantly different"
        print(f"    vs {name:14s} diff {best.mean() - scores.mean():+.4f}  "
              f"p = {p:.4f}  -> {verdict}")


def roc_is_threshold_independent():
    """AUC measures RANKING, separately from where you cut."""
    X, y = load_breast_cancer(return_X_y=True)
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    proba = cross_val_predict(LogisticRegression(max_iter=5000), X, y, cv=cv,
                              method="predict_proba")[:, 1]

    auc = roc_auc_score(y, proba)
    assert auc > 0.98, auc

    print(f"\n  ROC/AUC: {auc:.4f} -- one number, every threshold")
    print("    threshold  precision  recall")
    for t in (0.10, 0.30, 0.50, 0.70, 0.90):
        pred = (proba >= t).astype(int)
        print(f"      {t:.2f}      {precision_score(y, pred, zero_division=0):.4f}    "
              f"{recall_score(y, pred):.4f}")

    lo = (proba >= 0.10).astype(int)
    hi = (proba >= 0.90).astype(int)
    assert recall_score(y, lo) > recall_score(y, hi), "lower threshold, higher recall"
    assert precision_score(y, hi) > precision_score(y, lo), "higher threshold, higher precision"

    print("       the precision/recall trade-off, made concrete: the AUC is")
    print("       unchanged by the threshold, which is exactly its value")


def main():
    print("Experiment 14 -- Comparing classifiers")
    unit4_spam_matrix()
    practice_2_base_rate()
    results = compare_five()
    paired_significance(results)
    roc_is_threshold_independent()
    print("\n  all Unit 4 evaluation calculations reproduced")


if __name__ == "__main__":
    main()
