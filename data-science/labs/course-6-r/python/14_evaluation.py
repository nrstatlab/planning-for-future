"""Experiment 14 (Python equivalent) -- confusion matrix, accuracy, ROC.

R version: ../14_evaluation.R  (caret::confusionMatrix, pROC::roc)
Reproduces the worked example from Course 6 Unit 4 practice problem 1, so the
notes and the code agree.
"""
import numpy as np
from sklearn.metrics import (confusion_matrix, accuracy_score, precision_score,
                             recall_score, f1_score, roc_auc_score, roc_curve)

# The exact counts from Unit 4 Problem 1: TP=80, FP=20, FN=40, TN=860
y_true = np.array([1] * 120 + [0] * 880)
y_pred = np.array([1] * 80 + [0] * 40 + [1] * 20 + [0] * 860)


def metrics(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return dict(
        tp=tp, fp=fp, fn=fn, tn=tn,
        accuracy=(tp + tn) / (tp + tn + fp + fn),
        precision=tp / (tp + fp),
        recall=tp / (tp + fn),
        specificity=tn / (tn + fp),
        f1=2 * tp / (2 * tp + fp + fn),
    )


if __name__ == "__main__":
    m = metrics(y_true, y_pred)
    print("CONFUSION MATRIX               R: caret::confusionMatrix()")
    print(f"                  Predicted +   Predicted -")
    print(f"    Actual +      {m['tp']:>10}   {m['fn']:>11}")
    print(f"    Actual -      {m['fp']:>10}   {m['tn']:>11}")

    print("\nMETRICS")
    for k in ("accuracy", "precision", "recall", "specificity", "f1"):
        print(f"    {k:<12} {m[k]:.4f}")

    print(f"\n    sklearn cross-check:")
    print(f"      accuracy  {accuracy_score(y_true, y_pred):.4f}")
    print(f"      precision {precision_score(y_true, y_pred):.4f}")
    print(f"      recall    {recall_score(y_true, y_pred):.4f}")
    print(f"      f1        {f1_score(y_true, y_pred):.4f}")

    baseline = (y_true == 0).mean()
    print(f"\n  THE ACCURACY PARADOX")
    print(f"    accuracy of this model            = {m['accuracy']:.4f}")
    print(f"    accuracy of 'always predict 0'    = {baseline:.4f}")
    print(f"    the model beats the trivial baseline by only "
          f"{m['accuracy'] - baseline:.4f}")
    print(f"    but recall is {m['recall']:.3f} -- it MISSES "
          f"{m['fn']} of {m['tp']+m['fn']} real cases")

    # ROC needs scores, not hard labels.
    rng = np.random.default_rng(42)
    scores = np.where(y_true == 1,
                      rng.beta(5, 2, size=len(y_true)),
                      rng.beta(2, 5, size=len(y_true)))
    auc = roc_auc_score(y_true, scores)
    fpr, tpr, _ = roc_curve(y_true, scores)
    print(f"\nROC / AUC                      R: pROC::roc(); auc()")
    print(f"    AUC = {auc:.4f}")
    print("    (AUC is the probability the model ranks a random positive")
    print("     above a random negative -- 0.5 would be random guessing)")

    assert abs(m["accuracy"] - 0.940) < 1e-9
    assert abs(m["precision"] - 0.800) < 1e-9
    assert abs(m["recall"] - 2/3) < 1e-9
    assert abs(m["f1"] - 0.727) < 1e-3
    print("\n  matches Unit 4 Problem 1 exactly ✓")
