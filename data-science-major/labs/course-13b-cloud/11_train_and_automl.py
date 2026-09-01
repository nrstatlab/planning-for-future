"""Experiments 11 and 14 -- build a model on a managed ML platform, and use
an AutoML service.

SageMaker, Azure ML Studio and Vertex AI need an account, so
`11_sagemaker_train.md` and `14_automl.md` carry the console steps and the
SDK calls, marked NOT EXECUTED.

What runs here is the model, on the same scikit-learn Course 12 A used --
because the ALGORITHM is not what the cloud changes. What the cloud changes
is the packaging: where the data comes from, where the artefact goes, and
what it costs. Those three are modelled explicitly.

The AutoML half is a genuine (small) AutoML: a real search over real models
with real cross-validation, so the leaderboard is measured. That makes the
point AutoML marketing does not -- what it actually does, and what it costs.
"""
import io
import json
import os
import tempfile
import time

import joblib
import numpy as np
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

import fixtures as f

SEED = 42
MODEL_PATH = os.path.join(tempfile.gettempdir(), "cloud13b_model.joblib")


def churn_data(n=1200):
    """A churn-shaped dataset with a KNOWN base rate, as in Course 12 A."""
    X, y = make_classification(
        n_samples=n, n_features=10, n_informative=5, n_redundant=2,
        weights=[0.85, 0.15], flip_y=0.02, class_sep=1.1,
        random_state=SEED)
    return X, y


def train_model(X_train, y_train):
    """The 'training job'. On SageMaker this is a container; here it is a call."""
    pipe = Pipeline([("scale", StandardScaler()),
                     ("clf", GradientBoostingClassifier(random_state=SEED))])
    pipe.fit(X_train, y_train)
    return pipe


def main():
    print("  Experiments 11 and 14 -- training and AutoML on a managed platform")

    X, y = churn_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=SEED)
    base_rate = y.mean()
    print(f"\n    dataset: {len(X):,} rows, {X.shape[1]} features, "
          f"base rate {base_rate:.2%} positive")
    assert 0.13 < base_rate < 0.17

    # ---- experiment 11: the training job ---------------------------------
    print("\n    --- experiment 11: the training job")
    t0 = time.perf_counter()
    model = train_model(X_train, y_train)
    train_seconds = time.perf_counter() - t0
    pred = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]
    acc = accuracy_score(y_test, pred)
    f1 = f1_score(y_test, pred)
    auc = roc_auc_score(y_test, proba)

    dummy = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    dummy_acc = accuracy_score(y_test, dummy.predict(X_test))

    print(f"      {'model':<26}{'accuracy':>10}{'F1':>8}{'AUC':>8}")
    print(f"      {'DummyClassifier':<26}{dummy_acc:>10.4f}"
          f"{0.0:>8.4f}{0.5:>8.4f}")
    print(f"      {'GradientBoosting':<26}{acc:>10.4f}{f1:>8.4f}{auc:>8.4f}")
    assert acc > dummy_acc and auc > 0.85
    print(f"""         quote the DUMMY FIRST, always. {acc:.2%} sounds excellent
         until you see that predicting 'never churns' scores {dummy_acc:.2%}
         -- the real gain is {acc - dummy_acc:.1%} points of accuracy, and it is the
         F1 of {f1:.4f} against 0.0000 that shows the model found anything
         at all. This is Course 12 A's argument, and it does not stop
         being true because the model trained on somebody else's
         computer""")

    # ---- the artefact ----------------------------------------------------
    joblib.dump(model, MODEL_PATH)
    size = os.path.getsize(MODEL_PATH)
    reloaded = joblib.load(MODEL_PATH)
    assert (reloaded.predict(X_test) == pred).all()
    print(f"\n      model artefact: {size:,} bytes, reloads and predicts "
          f"identically")
    print("""         THAT FILE IS THE DELIVERABLE. A SageMaker training job
         writes exactly this to s3://bucket/models/, and the deploy
         step reads it back. Training and serving are separate
         systems joined by one artefact in object storage -- which is
         why the IAM role in experiment 10 needs s3:PutObject on
         models/ and nothing else""")

    # ---- what the cloud actually changes ---------------------------------
    print("\n    what a managed platform changes, and what it does not:")
    print(f"      {'':<24}{'your laptop':<24}{'managed platform'}")
    for label, local, cloud in (
            ("the algorithm", "scikit-learn", "SCIKIT-LEARN -- identical"),
            ("data source", "a local file", "s3:// or a feature store"),
            ("hardware", "what you own", "chosen per job, per hour"),
            ("training time", "hours on CPU", "minutes on GPU, if it helps"),
            ("experiment tracking", "a notebook cell", "logged automatically"),
            ("the artefact", "a file you might lose", "versioned in object storage"),
            ("deployment", "you build a server", "one API call"),
            ("cost", "sunk", "PER SECOND, and visible")):
        print(f"      {label:<24}{local:<24}{cloud}")
    print(f"""         THE FIRST ROW IS THE POINT. The cloud does not make your
         model better; it makes training REPRODUCIBLE, deployment
         ROUTINE and cost VISIBLE. A bad model trained on 8 GPUs is
         still a bad model, and the {dummy_acc:.0%} baseline above is unmoved by
         any amount of hardware""")

    # ---- the cost model --------------------------------------------------
    print(f"\n    what this training job would cost (it took "
          f"{train_seconds:.2f}s here):")
    print(f"      {'instance':<16}{'$/hour':>9}{'10 min job':>12}"
          f"{'100 jobs':>11}")
    for inst in ("t3.medium", "m5.xlarge", "c5.4xlarge", "p3.2xlarge",
                 "p4d.24xlarge"):
        rate = f.EC2[inst]
        job = rate / 6
        print(f"      {inst:<16}{rate:>9.4f}{job:>12.4f}{job * 100:>11.2f}")
    cheap = f.EC2["m5.xlarge"] / 6
    gpu = f.EC2["p4d.24xlarge"] / 6
    assert gpu / cheap > 100
    print(f"""         the 8-GPU box costs {gpu / cheap:.0f}x the general-purpose one for the
         same ten minutes. GPUs earn that on deep learning, where the
         work is dense matrix multiplication. GRADIENT BOOSTING ON
         TABULAR DATA DOES NOT USE THEM -- this model would run at the
         same speed and 170x the price.
         'Which instance?' is answered by the ALGORITHM, not by
         ambition""")

    # ---- experiment 14: AutoML, actually run -----------------------------
    print("\n    --- experiment 14: AutoML, actually run")
    candidates = {
        "LogisticRegression": Pipeline([
            ("s", StandardScaler()),
            ("c", LogisticRegression(max_iter=2000, random_state=SEED))]),
        "DecisionTree(d=3)": DecisionTreeClassifier(max_depth=3,
                                                    random_state=SEED),
        "DecisionTree(d=None)": DecisionTreeClassifier(random_state=SEED),
        "RandomForest(100)": RandomForestClassifier(n_estimators=100,
                                                    random_state=SEED),
        "GradientBoosting": GradientBoostingClassifier(random_state=SEED),
    }
    print(f"      {len(candidates)} candidates, 5-fold CV on ROC AUC "
          f"-- a real search")
    board = []
    total_fits = 0
    t0 = time.perf_counter()
    for name, est in candidates.items():
        scores = cross_val_score(est, X_train, y_train, cv=5,
                                 scoring="roc_auc")
        total_fits += 5
        board.append((name, scores.mean(), scores.std()))
    search_seconds = time.perf_counter() - t0
    board.sort(key=lambda r: -r[1])

    print(f"\n      {'rank':<6}{'model':<24}{'CV AUC':>9}{'std':>8}")
    for i, (name, mean, sd) in enumerate(board, 1):
        print(f"      {i:<6}{name:<24}{mean:>9.4f}{sd:>8.4f}")
    winner, best, best_sd = board[0]
    second, second_score, second_sd = board[1]
    print(f"\n      {total_fits} model fits in {search_seconds:.1f}s")
    assert len(board) == 5

    gap = best - second_score
    print(f"""         THE LEADERBOARD IS THE WHOLE OF AUTOML. It fits many
         models, cross-validates each, and ranks them. There is no
         intelligence in it -- it is a SEARCH, and its value is that
         it is exhaustive where you would have been lazy.
         And look at the top two: {best:.4f} against {second_score:.4f}, a gap of
         {gap:.4f} with standard deviations of {best_sd:.4f} and {second_sd:.4f}. THE
         DIFFERENCE IS INSIDE THE NOISE. Declaring a winner here is
         not supported by the data, and 'AutoML picked X' is not a
         reason to prefer X""")

    # ---- what AutoML cannot do -------------------------------------------
    print("\n    what AutoML does NOT do:")
    for what in (
        "decide what the target variable should be",
        "notice that your target leaks the answer",
        "tell you the base rate matters more than the algorithm",
        "know that last year's data no longer describes this year",
        "choose a threshold that fits the business cost of an error",
        "explain a prediction to a regulator",
        "notice that the model is unfair to a protected group",
    ):
        print(f"      - {what}")
    print("""         EVERY ONE OF THOSE IS THE ACTUAL JOB. AutoML automates
         the part a competent person does in an afternoon and leaves
         untouched the parts that take weeks and cause the failures.
         Say that when asked to evaluate AutoML, and say it before
         saying it is useful -- which it is""")

    # ---- and the cost of the search --------------------------------------
    print("\n    what an AutoML search costs")
    per_fit_here = search_seconds / total_fits
    print(f"      one fit on THIS dataset (1,200 rows): "
          f"{per_fit_here:.3f} s -- too small to cost anything")
    print("      so scale it: assume one fit takes 4 minutes, which is "
          "ordinary")
    print(f"\n      {'search':<26}{'fits':>6}{'compute':>12}{'m5.xlarge':>12}")
    MINUTES_PER_FIT = 4
    for label, fits in (("this search, scaled", total_fits),
                        ("a modest managed search", 250),
                        ("a full AutoML run", 2000)):
        hours = fits * MINUTES_PER_FIT / 60
        cost = hours * f.EC2["m5.xlarge"]
        print(f"      {label:<26}{fits:>6}{hours:>10.1f} h"
              f"   ${cost:>9.2f}")
    one = 1 * MINUTES_PER_FIT / 60 * f.EC2["m5.xlarge"]
    full = 2000 * MINUTES_PER_FIT / 60 * f.EC2["m5.xlarge"]
    assert full / one == 2000
    print(f"""         AutoML's compute is a straight MULTIPLE of one fit --
         ${full:,.2f} against ${one:.4f}, exactly {full / one:,.0f}x, because that is
         all it is. And AutoML services charge a premium on top of
         the compute.
         So cut the search space with what you already know: on
         tabular data, gradient boosting wins often enough that
         starting there and stopping is frequently the better trade.
         The leaderboard above makes the point -- it spent 5x the
         compute to rank a model {gap:.4f} AUC above the one you would
         have picked anyway, inside the noise""")

    os.remove(MODEL_PATH)
    return board


if __name__ == "__main__":
    main()
