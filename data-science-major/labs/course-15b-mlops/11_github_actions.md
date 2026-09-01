# Experiment 11 — automate training and deployment with GitHub Actions

## *** NOT EXECUTED ***

**A GitHub Actions workflow runs on GitHub's runners**, triggered by a push to
a repository. There is no runner here and no way to trigger one. **Nothing in
this file has been run**, and nothing in the notes claims an output for it.

**What is verified** is the pipeline the workflow would execute:
`07_mlflow_dvc.py` runs the training pipeline twice and
asserts the results are **byte-identical**, which is the property CI exists to
protect. A workflow that runs a non-deterministic pipeline tells you nothing.

---

## The workflow

`.github/workflows/ml-pipeline.yml`:

```yaml
name: ML pipeline

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: "0 3 * * 1"        # Monday 03:00 UTC -- retrain weekly

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip                     # cache the wheels between runs

      - name: Install
        run: pip install -r requirements.txt -r requirements-dev.txt

      - name: Lint
        run: ruff check .

      - name: Unit tests
        run: pytest -q --cov=src --cov-report=term-missing

      - name: Data validation
        run: python -m src.validate_data data/applicants.csv

  train:
    needs: test                          # do not train if the tests fail
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.11", cache: pip}

      - name: Install
        run: pip install -r requirements.txt

      - name: Pull the data
        run: dvc pull                    # experiment 9's other half
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Train
        run: python -m src.train --out metrics.json

      - name: Gate on the metric
        run: python -m src.gate metrics.json --min-auc 0.75

      - uses: actions/upload-artifact@v4
        with:
          name: model
          path: |
            model.pkl
            metrics.json

  deploy:
    needs: train
    if: github.ref == 'refs/heads/main'   # never deploy from a PR
    runs-on: ubuntu-latest
    environment: production               # requires a manual approval
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with: {name: model}

      - name: Build and push the image
        run: |
          echo "${{ secrets.REGISTRY_TOKEN }}" | docker login -u ci --password-stdin
          docker build -t $REGISTRY/loan-model:${{ github.sha }} .
          docker push $REGISTRY/loan-model:${{ github.sha }}
```

---

## The five design decisions in that file

### 1. `needs: test` — the gate

**The training job does not start unless the tests pass.** Without `needs`,
GitHub runs jobs in parallel and you get a trained model from code that fails
its own tests.

### 2. `src.gate --min-auc 0.75` — the metric gate

> ### 🎯 This is the step that makes it an *ML* pipeline rather than a
> software one
>
> Ordinary CI asks "does the code work?". **ML CI must also ask "is the model
> good enough?"** — because a pipeline can run perfectly and produce a model
> that is worse than the one in production.
>
> ```python
> # src/gate.py
> import json, sys
> m = json.load(open(sys.argv[1]))
> if m["auc"] < float(sys.argv[3]):
>     sys.exit(f"AUC {m['auc']:.4f} below the {sys.argv[3]} threshold")
> ```
>
> **Compare against the CURRENT PRODUCTION model, not a fixed number**, once
> you have one. A model that is merely above 0.75 but below what is already
> deployed should not ship.

### 3. `if: github.ref == 'refs/heads/main'`

**A pull request must not deploy.** Without this line, anyone who opens a PR
deploys to production.

### 4. `environment: production`

Attaches GitHub's **required-reviewers** protection, so the deploy job pauses
for a human. **Continuous delivery does not have to mean unattended
delivery**, and for a model that makes credit decisions it should not.

### 5. `secrets.*`

> ### ⚠️ Never put a credential in the YAML
>
> The workflow file is in the repository, and the repository history is
> forever. Secrets live in **Settings → Secrets and variables → Actions**, and
> GitHub masks them in the logs.
>
> **They are not masked if you `echo` them into a file the workflow later
> prints.** That is the usual way they leak.

---

## What CI/CD means for ML, specifically

| Ordinary software | ML |
|---|---|
| CI: build, lint, test | **plus data validation, plus a training run** |
| The artifact is a binary | **the artifact is a model AND its metrics** |
| Tests are deterministic | **training may not be** — pin every seed |
| "It passes" is enough | **"it passes AND it beats the current model"** |
| Roll back = redeploy the old build | **roll back = redeploy the old model AND its preprocessing** |

**The last row is the one that bites.** A model and the code that prepares its
features must be versioned and rolled back *together*; deploying an old model
with new preprocessing produces silently wrong predictions.

### The four deployment strategies the syllabus names

| Strategy | What it does | When |
|---|---|---|
| **Batch** | score everything overnight | no latency requirement |
| **Online** | score on request | the API in `12_serve_drift_govern.py` |
| **A/B test** | split traffic, compare a business metric | you have enough traffic for significance |
| **Canary** | 1% → 10% → 100%, watching errors | **the default for anything risky** |

**And the fifth, which is not on the list and should be: shadow deployment.**
Run the new model alongside the old one on real traffic, log both, serve only
the old one's answer. It is the only way to see how a model behaves on
production data at zero risk.

---

## If you are running this yourself

Push the file to `.github/workflows/` in any GitHub repository. The **Actions**
tab shows each run, each job, and every step's log.

To debug locally without pushing:

```bash
# nektos/act runs workflows in Docker -- and needs a Docker daemon,
# which is the same thing missing here
act -j test
```

## What goes in the lab record

| Item | Value |
|---|---|
| A screenshot of a green run, all three jobs | |
| Run time: cold cache, and with the pip cache warm | |
| **A screenshot of a FAILED run and what failed** | |
| The metric gate rejecting a deliberately bad model | |
| The deploy job waiting for approval | |
| Evidence your pipeline is deterministic — two runs, same metrics | |

Two things to do deliberately, because passing runs teach nothing:

1. **Break a test and push.** Confirm the `train` job never starts.
2. **Lower `--min-auc` to 0.99 and push.** Confirm the gate stops the deploy
   even though every test passed.
