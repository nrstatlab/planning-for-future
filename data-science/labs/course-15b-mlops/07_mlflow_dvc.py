"""Experiments 7, 8 and 9 -- EDA with MLflow experiment tracking, a
reproducible model under version control, and dataset versioning with DVC.

REAL MLflow, REAL git, REAL DVC. All three are installed and all three run
here; the MLflow store and the git repository are created under a temporary
directory and inspected afterwards, so nothing is asserted that was not
observed.
"""
import json
import os
import pathlib
import shutil
import subprocess
import tempfile

import numpy as np
import pandas as pd

import fixtures as f


def run(cmd, cwd, check=True):
    """Run a command and return its stdout, so the lab can assert on it."""
    p = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str),
                       capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"{cmd}\n{p.stdout}\n{p.stderr}")
    return p.stdout.strip()


def experiment_7(tmp):
    print("\n    --- experiment 7: EDA and experiment tracking with MLflow")

    import mlflow
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.dummy import DummyClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, roc_auc_score

    # MLflow 3 requires a database backend -- the old ./mlruns file store is
    # in maintenance mode and raises. SQLite is the right local choice and is
    # what the error message recommends.
    store = tmp / "mlflow.db"
    mlflow.set_tracking_uri(f"sqlite:///{store}")
    mlflow.set_experiment("loan-approval")

    df = f.train_reference(4000)
    X, y = df[f.FEATURES], df.approved
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25,
                                          random_state=f.SEED, stratify=y)

    print(f"\n      {len(Xtr):,} train / {len(Xte):,} test, "
          f"base rate {y.mean():.4f}")

    configs = [
        ("baseline-majority", DummyClassifier(strategy="most_frequent"), {}),
        ("logreg-C0.01", LogisticRegression(C=0.01, max_iter=1000), {"C": 0.01}),
        ("logreg-C1", LogisticRegression(C=1.0, max_iter=1000), {"C": 1.0}),
        ("logreg-C100", LogisticRegression(C=100.0, max_iter=1000),
         {"C": 100.0}),
        ("rf-depth3", RandomForestClassifier(max_depth=3, n_estimators=100,
                                             random_state=f.SEED),
         {"max_depth": 3}),
        ("rf-depth12", RandomForestClassifier(max_depth=12, n_estimators=100,
                                              random_state=f.SEED),
         {"max_depth": 12}),
    ]

    print(f"\n      {'run name':<20}{'accuracy':>10}{'AUC':>9}"
          f"{'train-test gap':>16}")
    results = {}
    for name, model, params in configs:
        with mlflow.start_run(run_name=name):
            model.fit(Xtr, ytr)
            acc = accuracy_score(yte, model.predict(Xte))
            tr_acc = accuracy_score(ytr, model.predict(Xtr))
            try:
                auc = roc_auc_score(yte, model.predict_proba(Xte)[:, 1])
            except Exception:                              # noqa: BLE001
                auc = float("nan")
            mlflow.log_params({"model": type(model).__name__, **params})
            mlflow.log_params({"n_train": len(Xtr), "seed": f.SEED})
            mlflow.log_metrics({"accuracy": acc, "auc": auc,
                                "train_accuracy": tr_acc,
                                "gap": tr_acc - acc})
            results[name] = (acc, auc, tr_acc - acc)
        print(f"      {name:<20}{acc:>10.4f}{auc:>9.4f}{tr_acc - acc:>16.4f}")

    # ---- read the runs BACK, which is the point of a tracking server -----
    client = mlflow.tracking.MlflowClient()
    exp = client.get_experiment_by_name("loan-approval")
    runs = client.search_runs(exp.experiment_id, order_by=["metrics.auc DESC"])
    print(f"\n      MLflow stored {len(runs)} runs in {store.name} "
          f"({store.stat().st_size:,} bytes of SQLite)")
    print(f"      queried back, ordered by AUC:")
    print(f"      {'run':<20}{'AUC':>9}   {'params'}")
    for r in runs[:3]:
        p = {k: v for k, v in r.data.params.items() if k not in ("seed",)}
        print(f"      {r.data.tags.get('mlflow.runName', '?'):<20}"
              f"{r.data.metrics['auc']:>9.4f}  {p}")

    print("""         THAT QUERY IS WHY A TRACKING SERVER EXISTS. Six runs in
         a spreadsheet is manageable; sixty is not, and by then you
         cannot remember which one used C=100 or whether the good
         result came before or after you fixed the leak.
         MLflow logs PARAMETERS, METRICS and ARTIFACTS against a run
         id, and the query above is the thing a notebook cannot do""")

    best = max(results, key=lambda k: results[k][1])
    base = results["baseline-majority"][0]
    print(f"\n      best by AUC: {best} ({results[best][1]:.4f})")
    print(f"      majority-class accuracy: {base:.4f}")

    over = max(results, key=lambda k: results[k][2])
    print(f"      largest train-test gap: {over} ({results[over][2]:.4f})")
    print("""         LOG THE TRAIN SCORE AS WELL AS THE TEST SCORE. The gap
         column is the only thing in this table that tells you WHY a
         model underperformed, and it costs one extra log_metric
         call. A tracking table without it records what happened and
         not why""")

    assert len(runs) == len(configs)
    assert results[best][1] > 0.7
    return results, store


def experiment_8(tmp):
    print("\n    --- experiment 8: reproducibility under version control")

    repo = tmp / "model-repo"
    repo.mkdir()
    run("git init -q .", repo)
    run("git config user.email lab@example.invalid", repo)
    run("git config user.name Lab", repo)

    train_py = repo / "train.py"
    train_py.write_text('''"""Train the loan model. Deterministic by construction."""
import json, sys, pathlib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import data as d

SEED = 42

def main(out="metrics.json"):
    df = d.load()
    X, y = df[d.FEATURES], df.approved
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.25, random_state=SEED, stratify=y)
    m = LogisticRegression(C=1.0, max_iter=1000, random_state=SEED)
    m.fit(Xtr, ytr)
    auc = roc_auc_score(yte, m.predict_proba(Xte)[:, 1])
    coef = dict(zip(d.FEATURES, m.coef_[0].round(6).tolist()))
    pathlib.Path(out).write_text(json.dumps(
        {"auc": round(float(auc), 6), "coef": coef, "seed": SEED}, indent=2))
    return auc

if __name__ == "__main__":
    print(main())
''')
    data_py = repo / "data.py"
    data_py.write_text(f'''"""The dataset, pinned by seed."""
import numpy as np, pandas as pd
FEATURES = {f.FEATURES!r}
TRUE_COEF = {f.TRUE_COEF!r}
def load(n=4000, seed=42):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({{c: rng.normal(0, 1, n) for c in FEATURES}})
    z = {f.TRUE_INTERCEPT} + sum(TRUE_COEF[c] * df[c] for c in FEATURES)
    p = 1 / (1 + np.exp(-z))
    df["approved"] = (rng.random(n) < p).astype(int)
    return df
''')
    (repo / "requirements.txt").write_text(
        "scikit-learn==1.9.0\nnumpy==2.4.0\npandas==2.3.3\n")

    run("git add -A", repo)
    run('git commit -q -m "training pipeline, pinned"', repo)
    sha = run("git rev-parse --short HEAD", repo)
    print(f"\n      committed as {sha}")

    # ---- run it twice; the results must be identical ---------------------
    a = run(f"python3 train.py", repo)
    m1 = json.loads((repo / "metrics.json").read_text())
    b = run(f"python3 train.py", repo)
    m2 = json.loads((repo / "metrics.json").read_text())

    print(f"      run 1 AUC {m1['auc']:.6f}")
    print(f"      run 2 AUC {m2['auc']:.6f}")
    print(f"      identical: {m1 == m2}")
    assert m1 == m2, "the pipeline is not deterministic"

    print(f"\n      the fitted coefficients, against the KNOWN truth:")
    print(f"      {'feature':<16}{'fitted':>10}{'true':>10}{'error':>10}")
    for k, v in m1["coef"].items():
        t = f.TRUE_COEF[k]
        print(f"      {k:<16}{v:>10.4f}{t:>10.4f}{v - t:>10.4f}")
    print("""         THE DATA WAS GENERATED FROM THOSE COEFFICIENTS, so the
         fit can be CHECKED rather than merely reported. A model that
         converges has proved nothing; a model that recovers the
         parameters that produced the data has""")

    print("\n      the four things that must be pinned for reproducibility:")
    for i, (thing, how) in enumerate([
        ("the CODE", f"git commit {sha}"),
        ("the DATA", "a seed here; DVC in experiment 9 for real files"),
        ("the ENVIRONMENT", "requirements.txt with == , not >="),
        ("the RANDOMNESS", "random_state on every estimator AND the split"),
    ], start=1):
        print(f"        {i}. {thing:<20}{how}")
    print("""         MISS ANY ONE AND THE RESULT IS NOT REPRODUCIBLE. The
         one people forget is the fourth: train_test_split has its own
         random_state, separate from the model's, and a pipeline that
         pins only the model still gets a different answer every
         time""")

    # ---- and demonstrate the failure ------------------------------------
    unpinned = repo / "train_unpinned.py"
    unpinned.write_text(train_py.read_text().replace(
        "random_state=SEED, stratify=y", "stratify=y"))
    aucs = []
    for _ in range(3):
        out = run("python3 train_unpinned.py out.json", repo)
        aucs.append(round(float(out), 6))
    print(f"\n      the SAME code with the split's random_state removed:")
    print(f"        three runs -> {aucs}")
    spread = max(aucs) - min(aucs)
    print(f"        spread {spread:.6f}")
    if spread > 0:
        print("""         THREE DIFFERENT ANSWERS FROM IDENTICAL CODE. The model
         was still seeded; only the train/test SPLIT was not. That is
         enough to make every number in your report unrepeatable, and
         it is the single most common reproducibility bug in student
         projects""")
    else:
        print("""         they happened to agree here, which does not make the
         code reproducible -- an unseeded split is unreproducible
         whether or not a given run reveals it""")

    assert sha
    return m1, aucs


def experiment_9(tmp):
    print("\n    --- experiment 9: dataset and model versioning with DVC")

    repo = tmp / "dvc-repo"
    repo.mkdir()
    run("git init -q .", repo)
    run("git config user.email lab@example.invalid", repo)
    run("git config user.name Lab", repo)
    out = run("dvc init -q", repo)
    run("git add -A", repo)
    run('git commit -q -m "dvc init"', repo)

    data_dir = repo / "data"
    data_dir.mkdir()
    v1 = f.train_reference(4000)
    v1.to_csv(data_dir / "applicants.csv", index=False)
    size_v1 = (data_dir / "applicants.csv").stat().st_size

    run("dvc add data/applicants.csv", repo)
    run("git add -A", repo)
    run('git commit -q -m "data v1: 4000 clean applications"', repo)
    sha_v1 = run("git rev-parse --short HEAD", repo)

    pointer = (data_dir / "applicants.csv.dvc").read_text()
    print(f"\n      data v1: {len(v1):,} rows, {size_v1:,} bytes on disk")
    print(f"      committed as {sha_v1}")
    print(f"\n      what git actually stores -- applicants.csv.dvc:")
    for line in pointer.strip().splitlines():
        print(f"        {line}")
    print(f"        ({len(pointer)} bytes, against {size_v1:,} for the data)")

    tracked = run("git ls-files", repo)
    assert "applicants.csv.dvc" in tracked
    assert "data/applicants.csv" not in tracked.split("\n")
    print("""         GIT TRACKS THE POINTER, NOT THE DATA. The .dvc file is
         a few hundred bytes holding an md5 and a size; the CSV
         itself is in .gitignore and lives in the DVC cache.
         THAT IS THE WHOLE IDEA. Git is very bad at large binary
         files -- it stores a full copy of every version for ever and
         cannot diff them -- so DVC keeps the data out of git and puts
         a content hash in its place""")

    # ---- version 2: the data drifts --------------------------------------
    v2 = f.applicants(4000, seed=f.SEED, drift=1.5)
    v2.to_csv(data_dir / "applicants.csv", index=False)
    run("dvc add data/applicants.csv", repo)
    run("git add -A", repo)
    run('git commit -q -m "data v2: income distribution shifted"', repo)
    sha_v2 = run("git rev-parse --short HEAD", repo)

    md5_v1 = [l for l in pointer.splitlines() if "md5" in l][0].strip()
    md5_v2 = [l for l in (data_dir / "applicants.csv.dvc").read_text()
              .splitlines() if "md5" in l][0].strip()
    print(f"\n      data v2 committed as {sha_v2}")
    print(f"        v1 {md5_v1}")
    print(f"        v2 {md5_v2}")
    assert md5_v1 != md5_v2

    # ---- and go back ------------------------------------------------------
    run(f"git checkout -q {sha_v1}", repo)
    run("dvc checkout -q", repo, check=False)
    back = pd.read_csv(data_dir / "applicants.csv")
    same = np.allclose(back.income.mean(), v1.income.mean())
    print(f"\n      checked out {sha_v1} and ran 'dvc checkout':")
    print(f"        income mean now {back.income.mean():.4f}, "
          f"v1 was {v1.income.mean():.4f}, v2 was {v2.income.mean():.4f}")
    print(f"        recovered v1 exactly: {same}")
    assert same, "dvc checkout did not restore the old data"

    print("""         'git checkout' MOVED THE CODE AND THE POINTER; 'dvc
         checkout' READ THE POINTER AND RESTORED THE DATA. Two
         commands, and that pairing is the entire workflow.
         WHY IT MATTERS FOR MLOps: when a model in production starts
         behaving oddly, the question is 'what did it see when it was
         trained'. Without data versioning that question has no
         answer. With it, the model's git commit identifies its code
         AND its data, together""")

    print(f"\n      {'':<18}{'git alone':<30}{'git + DVC'}")
    for a, b, c in [
        ("stores", "every version, in full", "a hash; data in a cache/remote"),
        ("repo size", "grows with every data change", "stays small"),
        ("diff", "useless on a binary", "compares hashes"),
        ("large files", "slow, often refused", "fine"),
        ("reproduce", "code only", "**code AND data**"),
    ]:
        print(f"      {a:<18}{b:<30}{c}")

    run(f"git checkout -q {sha_v2}", repo, check=False)
    return sha_v1, sha_v2


def main():
    print("  Experiments 7, 8 and 9 -- MLflow, reproducibility, DVC")
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="mlops-"))
    try:
        experiment_7(tmp)
        experiment_8(tmp)
        experiment_9(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\n    all assertions passed")


if __name__ == "__main__":
    main()
