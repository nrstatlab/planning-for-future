# Unit 3 — MLOps Fundamentals

**Syllabus topics:** MLOps challenges and risk mitigation. Responsible AI
and scaling ML solutions. Key MLOps features: EDA, feature engineering, model
training and evaluation, reproducibility. Deployment requirements, monitoring
basics. Model versioning and experimentation tracking.

---

## 3.1 What makes MLOps different from DevOps

### 🎯 The one sentence

> **DevOps versions code. MLOps must version code, data and model together —
> and any one of the three changing changes the output.**

| | **DevOps** | **MLOps** |
|---|---|---|
| Artefacts | code | **code + data + model** |
| Tests | deterministic | training may not be |
| "It works" | tests pass | **tests pass AND the metric is good enough** |
| Degrades over time | no — code does not rot | **yes — the world moves** |
| Rollback | redeploy the old build | **the old model AND its preprocessing** |
| Reviewable | read the diff | you cannot read a weight matrix |

### ⚠️ The row that causes real incidents

**A model and the code that prepares its features must be versioned and rolled
back together.** Deploying an old model with new preprocessing produces
predictions that are silently wrong — no error, no crash, just worse decisions.

---

## 3.2 The challenges, and the risk each carries

| Challenge | The risk it carries, and what mitigates it |
|---|---|
| **Training/serving skew** | the same transformation code in both paths — a feature store, or one shared library |
| **Data drift** | monitoring and alerting ([Unit 5](unit-5.md)) |
| **Reproducibility** | pin all four things — §3.5 |
| **Hidden dependencies** | data lineage; know what feeds what |
| **Technical debt** | the "glue code" and "pipeline jungle" problems |
| **Undeclared consumers** | somebody is querying your table and you do not know |

### 🎯 Training/serving skew is the most common MLOps bug

You train on a pandas DataFrame where a missing value became the column mean.
You serve from a Flask endpoint where a missing value becomes zero. **The
model is fine; the input is not**, and nothing raises an error.

**The fix is architectural**: one implementation of the transformation, called
from both paths. That is what a feature store is for, and a shared module is
enough at small scale.

### 📖 "Undeclared consumers", which sounds minor and is not

You change a column's meaning. Your own pipeline is updated. **Three teams
were querying that table and you did not know.** The mitigation is access
control plus a data catalogue — knowing who reads what is a prerequisite for
being able to change anything.

---

## 3.3 The key MLOps features, in order

### 📖 EDA and feature engineering

Before modelling, **profile**:

| Check | Why |
|---|---|
| nulls per column | a column that is 90% null is not a feature |
| distinct counts | a constant column contributes nothing; a near-unique one may be an id |
| distributions | skew, outliers, unexpected bimodality |
| **the base rate** | **the majority-class baseline — the number every accuracy is read against** |

[Experiment 2](lab.md#experiment-2) profiles every column and prints the base
rate before anything is fitted, which is the habit to copy.

### ⚠️ Feature engineering, and the leak that ruins projects

**Data leakage** is any feature that would not be available at prediction
time.

| Leak | Why it happens |
|---|---|
| a column computed **after** the outcome | "days until repayment" for a default model |
| scaling fitted on **all** the data | test-set statistics reach the training set |
| a row-order artefact | the data was sorted by the target |

**A suspiciously good result is a leak until proved otherwise.** That is a
practical rule, and `sklearn`'s `Pipeline` exists to make the second kind
hard: fit on train, transform test, never the reverse.

### 📖 Model training and evaluation

[Experiment 7](lab.md#experiment-7) fits six models and logs each to MLflow:

| Run | Accuracy | AUC | **Train − test gap** |
|---|---|---|---|
| **baseline-majority** | **0.5540** | 0.5000 | −0.0003 |
| logreg-C0.01 | 0.7060 | **0.7752** | −0.0083 |
| logreg-C1 | 0.7080 | 0.7752 | −0.0100 |
| rf-depth3 | 0.6880 | 0.7526 | 0.0153 |
| **rf-depth12** | 0.6850 | 0.7463 | **0.2783** |

> ### 🎯 Log the train score as well as the test score
>
> **The gap column is the only thing in this table that tells you *why* a
> model underperformed**, and it costs one extra `log_metric` call.
> `rf-depth12` has a gap of **0.2783** — it memorised the training set. A
> tracking table without that column records what happened and not why.
>
> **And note the baseline row: 0.5540.** Every other number is read against
> it.

---

## 3.4 Experimentation tracking

### 📖 What a tracking server stores

| Kind | Examples |
|---|---|
| **Parameters** | `C=0.01`, `max_depth=12`, `n_train=3000`, `seed=42` |
| **Metrics** | accuracy, AUC, train accuracy, the gap |
| **Artifacts** | the model file, plots, the confusion matrix |
| **Tags and source** | the git commit, the run name, who ran it |

```python
import mlflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("loan-approval")

with mlflow.start_run(run_name="logreg-C1"):
    model.fit(Xtr, ytr)
    mlflow.log_params({"model": "LogisticRegression", "C": 1.0, "seed": 42})
    mlflow.log_metrics({"accuracy": acc, "auc": auc, "gap": tr - acc})
    mlflow.sklearn.log_model(model, "model")
```

### 💡 Why a database backend, not `./mlruns`

**MLflow 3 refuses the old file store** — it raises rather than starting, and
recommends `sqlite:///mlflow.db`. The lab uses SQLite for that reason and
prints the file size, which is worth knowing: **six runs is under a megabyte**,
and a real project's tracking database stays small because it holds pointers,
not data.

### 🎯 The query is the point

```python
client.search_runs(exp_id, order_by=["metrics.auc DESC"])
```

> **Six runs in a spreadsheet is manageable; sixty is not**, and by then you
> cannot remember which one used `C=100`, or whether the good result came
> before or after you fixed the leak. **That query is the thing a notebook
> cannot do.**

---

## 3.5 Reproducibility — the four things that must be pinned

| # | Pin | How |
|---|---|---|
| 1 | **the code** | a git commit |
| 2 | **the data** | a seed, or **DVC** for real files ([experiment 9](lab.md#experiment-9)) |
| 3 | **the environment** | `requirements.txt` with `==`, **not** `>=` |
| 4 | **the randomness** | `random_state` on every estimator **AND on the split** |

### ⚠️ Number 4 is the one everybody forgets

[Experiment 8](lab.md#experiment-8) demonstrates it. The same code, with the
model still seeded and only `train_test_split`'s `random_state` removed, run
three times:

**Three different AUCs from identical code.**

> **That is enough to make every number in your report unrepeatable**, and it
> is the single most common reproducibility bug in student projects. The
> split has its own random state, separate from the model's.

### 🔢 And the check that proves reproducibility

The same experiment runs the pinned pipeline **twice** and asserts the outputs
are **byte-identical** — same AUC to six decimal places, same coefficients.

It then compares the fitted coefficients against the **known** ones that
generated the data:

| Feature | Fitted | True |
|---|---|---|
| income | 0.8749 | 0.9000 |
| loan_amount | −0.6898 | −0.7000 |
| credit_years | 0.4542 | 0.5000 |

> **A model that converges has proved nothing. A model that recovers the
> parameters which produced the data has.**

---

## 3.6 Model versioning

**A model version is not a filename.** It is:

| Component | Answers |
|---|---|
| the code commit | what algorithm and what preprocessing? |
| **the data version** | **what did it learn from?** |
| the hyperparameters | how was it configured? |
| the metrics | how good was it, on what? |
| the environment | which library versions? |

### 📖 What DVC does, and why git alone cannot

[Experiment 9](lab.md#experiment-9) commits a 4,000-row dataset, then a
drifted version, then rolls back:

| | **git alone** | **git + DVC** |
|---|---|---|
| Stores | every version, **in full** | a hash; data in a cache or remote |
| Repo size | grows with every data change | **stays small** |
| Diff | useless on a binary | compares hashes |
| Large files | slow, often refused | fine |
| **Reproduce** | code only | **code AND data** |

**Git tracks the pointer, not the data.** The `.dvc` file is a few hundred
bytes holding an md5 and a size; the CSV is in `.gitignore` and lives in the
DVC cache.

### 🎯 The two-command workflow

```bash
git checkout <sha>     # moves the code AND the pointer
dvc checkout           # reads the pointer, restores the data
```

> **When a model in production starts behaving oddly, the question is "what
> did it see when it was trained".** Without data versioning that question has
> no answer. With it, one git commit identifies the code *and* the data,
> together.

---

## 3.7 Responsible AI and scaling

**Deployment requirements** — what a model needs before it can be served at
all — are the subject of [Unit 4](unit-4.md); the monitoring basics that pair
with them are [Unit 5](unit-5.md).

| Concern | The practical control |
|---|---|
| **Fairness** | per-group metrics, not one aggregate ([Unit 5](unit-5.md)) |
| **Transparency** | a **model card**: data, metrics, limits, intended use |
| **Accountability** | a named owner and an appeal route |
| **Privacy** | minimisation, retention limits, **deletion that works** |
| **Reliability** | monitoring, drift alerts, a rollback plan |

### 📖 Scaling ML, and what breaks first

| Scale | What breaks |
|---|---|
| 1 model, 1 team | nothing; a notebook is fine |
| 5 models | **which one is deployed?** — you need a registry |
| 20 models | **shared features diverge** — you need a feature store |
| 50 models | **nobody knows what depends on what** — you need lineage |

**Each tool on that list exists because a specific thing broke at a specific
scale.** Adopting them before the breakage is how teams end up operating a
platform instead of shipping models.

---

## What to be able to do after this unit

- [ ] **Give three ways MLOps differs from DevOps**
- [ ] Explain training/serving skew and its architectural fix
- [ ] Define data leakage and give three ways it happens
- [ ] Say why the train/test **gap** belongs in a tracking table
- [ ] Describe what an experiment tracker stores, and why a notebook cannot replace it
- [ ] **List the four things that must be pinned**, and say which is most often forgotten
- [ ] Explain what a "model version" comprises beyond a file
- [ ] **Explain what DVC stores in git and what it does not**
- [ ] Give the two-command rollback workflow
- [ ] Name the five Responsible AI controls

**Cross-check yourself:** run
`07_mlflow_dvc.py`.
