"""Shared data for the Course 12 A practicals.

Three datasets, each chosen for a reason:

  STUDY     the ten (hours, score) pairs from COURSE 4's regression worked
            example, reused deliberately. Unit 3 refits them with
            scikit-learn and must reproduce Course 4's hand-computed slope
            4.3030, intercept 43.0303 and R^2 0.9958. If the two courses ever
            disagree, one of them is wrong and the lab suite says so.

  iris      loaded from scikit-learn. Small, clean, famous, and the same
            dataset Course 8 used for its WEKA experiments.

  CHURN     a deliberately IMBALANCED binary dataset -- 85% negative. It
            exists so accuracy can be shown to be misleading, which is the
            single most important idea in Unit 2.

Everything is seeded. Every figure in the notes is reproducible.
"""
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

RANDOM_STATE = 42

# --- Course 4's regression dataset, reused ---------------------------------
STUDY_HOURS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
STUDY_SCORES = [52, 55, 61, 64, 70, 72, 78, 82, 85, 91]

STUDY = pd.DataFrame({"hours": STUDY_HOURS, "score": STUDY_SCORES})


def study_xy():
    """X as a 2-D column vector, y as 1-D -- scikit-learn's expected shapes."""
    return STUDY[["hours"]].to_numpy(dtype=float), STUDY["score"].to_numpy(dtype=float)


# --- iris -------------------------------------------------------------------
def iris_frame():
    data = load_iris(as_frame=True)
    df = data.frame.copy()
    df["species"] = pd.Categorical.from_codes(data.target, data.target_names)
    return df, data


# --- an imbalanced dataset, for the accuracy argument -----------------------
def churn(n=400, positive_rate=0.15, seed=RANDOM_STATE):
    """Customers, 15% of whom churn. Two informative features and one noise.

    Built rather than loaded so the base rate is EXACTLY known -- the whole
    point of Unit 2 section 2.5 is comparing a model against that base rate.
    """
    rng = np.random.default_rng(seed)
    n_pos = int(round(n * positive_rate))
    n_neg = n - n_pos

    # Churners: fewer months, more support calls. Overlapping, not separable.
    tenure = np.concatenate([rng.normal(8, 4, n_pos), rng.normal(24, 10, n_neg)])
    calls = np.concatenate([rng.normal(6, 2, n_pos), rng.normal(2, 1.5, n_neg)])
    noise = rng.normal(0, 1, n)
    y = np.concatenate([np.ones(n_pos, dtype=int), np.zeros(n_neg, dtype=int)])

    df = pd.DataFrame({"tenure_months": np.clip(tenure, 0, None),
                       "support_calls": np.clip(calls, 0, None),
                       "irrelevant": noise,
                       "churned": y})
    return df.sample(frac=1.0, random_state=seed).reset_index(drop=True)


# --- a tiny hand-checkable classification example ---------------------------
# Used in Unit 2 for the confusion matrix. Twenty cases, six of them positive,
# and deliberately arranged so PRECISION AND RECALL DIFFER -- TP 4, FP 4, FN 2,
# TN 10. A matrix where they come out equal teaches nothing, because the whole
# reason both metrics exist is that they can disagree.
CONFUSION_TRUTH = [1] * 6 + [0] * 14
CONFUSION_PRED = ([1, 1, 1, 1, 0, 0]        # 4 true positives, 2 false negatives
                  + [1, 1, 1, 1]            # 4 false positives
                  + [0] * 10)               # 10 true negatives
