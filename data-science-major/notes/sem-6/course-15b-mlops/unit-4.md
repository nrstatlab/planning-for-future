# Unit 4 — Model Deployment and CI/CD Pipelines

**Syllabus topics:** Preparing models for production. Runtime
environments: dev to production adaptation. CI/CD pipelines: building ML
artifacts, testing pipelines. Deployment strategies: batch, online, A/B
testing, canary releases. Containerization and scaling (Docker, Kubernetes).

---

## 4.1 Preparing a model for production

### 🎯 What "production-ready" means, concretely

A notebook that predicts is not a deployable model. It needs:

| Requirement | Why |
|---|---|
| **A serialised artifact** | `joblib` or ONNX — not a variable in a kernel |
| **The preprocessing bundled with it** | otherwise training/serving skew |
| **Input validation** | callers send wrong things; see below |
| **A version string** | in the response, so a prediction can be traced to a model |
| **A health endpoint** | so an orchestrator can tell "running" from "working" |
| **Structured logging** | to detect drift later |
| **A latency budget** | and a timeout |

### 🔢 What the lab's endpoint actually does

[Experiment 12](lab.md#experiment-12) runs a real Flask server on a real
socket and calls it over HTTP:

| Request | Status | Body |
|---|---|---|
| `GET /health` | **200** | `{"status":"ok","model":"logreg","features":[...]}` |
| `POST /predict`, valid | **200** | `{"approved":true,"probability":0.836858,"model_version":"1.0.0"}` |
| `POST /predict`, two features missing | **400** | `{"error":"missing features","missing":["loan_amount","credit_years"]}` |
| `POST /predict`, a string where a float belongs | **400** | `{"error":"features must be numeric"}` |

> ### 🎯 The two error cases are the experiment
>
> **A demo endpoint returns a prediction. A production endpoint decides what
> to do when the caller omits two of the four features, or sends a string
> where a float belongs.**
>
> **Returning 400 with a reason** — rather than a 500, or a confidently wrong
> prediction on garbage input — is what separates the two. The model itself is
> three lines of that file.

---

## 4.2 Runtime environments

| Environment | Purpose | Data |
|---|---|---|
| **Development** | you write code | a sample, or synthetic |
| **Staging** | **as close to production as you can afford** | a production-like copy |
| **Production** | serves users | real |

### ⚠️ The differences that cause incidents

| Difference | The failure it causes |
|---|---|
| library versions | a model pickled with one scikit-learn version fails to load with another |
| **data volume** | code that works on 10,000 rows dies on 10 million |
| data *quality* | production has nulls, duplicates and encodings your sample did not |
| **secrets and endpoints** | hard-coded in dev, wrong in production |
| CPU/memory limits | fine on a laptop, OOM-killed in a container |

**The mitigation for all five is the same: make the environments as identical
as you can, and put the differences in configuration rather than in code.**
Environment variables, not `if ENVIRONMENT == "prod"`.

### 📖 The twelve-factor principle worth borrowing

> **Store configuration in the environment.** The same artefact — the same
> container image — runs in staging and in production, differing only by the
> variables passed in. If you rebuild for production, you did not test what
> you shipped.

---

## 4.3 CI/CD for ML

### 📖 The pipeline, stage by stage

```
push → lint → unit tests → DATA VALIDATION → train →
       METRIC GATE → build the ML artifact → deploy (with approval)
```

Two of those stages have no equivalent in ordinary software.

### 🎯 Data validation

**Before training, assert what must be true of the data:**

| Check | Example |
|---|---|
| schema | the expected columns, with the expected types |
| ranges | age between 18 and 120 |
| nulls | no more than 1% in any required column |
| **distribution** | the mean has not moved by more than 3 standard deviations |
| volume | at least 10,000 rows arrived |

**Training on bad data succeeds.** That is the whole problem — there is no
exception to catch, only a worse model. The validation step is where you
create the failure that would otherwise be silent.

### 🎯 The metric gate

> **This is the step that makes it an *ML* pipeline rather than a software
> one.** Ordinary CI asks "does the code work?". ML CI must also ask **"is the
> model good enough?"**

```python
m = json.load(open("metrics.json"))
if m["auc"] < MIN_AUC:
    sys.exit(f"AUC {m['auc']:.4f} below the {MIN_AUC} threshold")
```

**Compare against the current production model, not a fixed number**, once you
have one. A model above 0.75 but below what is already deployed should not
ship.

### ⚠️ And the prerequisite the gate depends on

**A CI pipeline that runs a non-deterministic training job tells you
nothing** — the metric moves between runs and the gate becomes a coin toss.

[Experiment 8](lab.md#experiment-8) is the verification: the pinned pipeline
runs twice and produces **byte-identical** metrics, while the same code with
the split's `random_state` removed produces **three different AUCs**.

### 📖 The workflow's structural decisions

From `11_github_actions.md`:

| Line | What it prevents |
|---|---|
| `needs: test` | training on code that fails its own tests |
| `if: github.ref == 'refs/heads/main'` | **a pull request deploying to production** |
| `environment: production` | unattended deployment — it requires a human approval |
| `secrets.*` | a credential in a file that lives in the repository for ever |

> **Continuous delivery does not have to mean unattended delivery**, and for a
> model that makes credit decisions it should not.

---

## 4.4 Deployment strategies

| Strategy | What it does | When |
|---|---|---|
| **Batch** | score everything overnight, write to a table | no latency requirement |
| **Online** | score on request | the API in experiment 12 |
| **Streaming** | score each event as it arrives | fraud, real-time personalisation |
| **Embedded** | the model ships inside the application | edge, mobile, offline |

### 📖 And the release strategies, which are a different axis

| Strategy | Mechanism | Risk |
|---|---|---|
| **Big bang** | replace it | **highest** |
| **Blue-green** | two environments, switch traffic, keep the old one | low; rollback is instant |
| **Canary** | 1% → 10% → 100%, watching errors | **low — the default for anything risky** |
| **A/B test** | split traffic, compare a **business** metric | needs enough traffic for significance |
| **Shadow** | run both, log both, **serve only the old one** | **zero — and it is not on the syllabus** |

### 🎯 Shadow deployment is the one to know beyond the syllabus

**Run the new model alongside the old one on real production traffic, log both
predictions, and serve only the old one's answer.**

> It is the only way to see how a model behaves on production data at **zero
> user risk**. You find the training/serving skew, the unexpected nulls and
> the latency problem before anybody is affected. It costs compute and nothing
> else.

### ⚠️ A/B testing an ML model — the trap

**You are testing a business outcome, not an accuracy.** A model with better
AUC can produce worse revenue, because the metric it optimised is not the one
the business cares about.

**And you need statistical power.** Splitting traffic 50/50 for a day is not
an experiment; decide the sample size in advance from the effect you would
care about — the same discipline as Course 4's hypothesis testing.

---

## 4.5 Containerization

### 📖 Why containers, in one line

> **The container is the unit of "it works on my machine" made portable** —
> the code, the libraries, and the OS-level dependencies, shipped as one
> artefact that runs identically wherever there is a runtime.

### ⚠️ The seven traps, from `10_docker.md`

| # | Trap | Fix |
|---|---|---|
| 1 | `FROM python:latest` | **pin the tag** |
| 2 | No `.dockerignore` | a 40 MB project becomes a 2 GB build context |
| 3 | `COPY . .` **before** `pip install` | **requirements first** — the layer cache |
| 4 | Running the Flask dev server | **gunicorn or uvicorn** |
| 5 | **`app.run(host="127.0.0.1")`** | **`0.0.0.0`** |
| 6 | Running as root | `USER app` |
| 7 | Secrets baked into the image | environment variables — `docker history` shows every layer |

### 🎯 Trap 5 costs an afternoon

The container starts, the logs look perfect, and `curl` from the host gets
connection refused. **`127.0.0.1` inside a container refers to the
container**, so the service is reachable only from inside itself.

### 🔢 Trap 3, and why the ordering matters

**Docker caches each layer.** Copying `requirements.txt` and installing
*before* copying the code means the expensive `pip install` layer is rebuilt
only when the dependencies change — not on every one-line code edit.

### 🔢 Base image size

| Base | Size |
|---|---|
| `python:3.11` | ~1 GB |
| **`python:3.11-slim`** | **~150 MB** |
| `python:3.11-alpine` | ~50 MB, **but** musl breaks many scientific wheels |

**Slim is usually right. Alpine is a trap for scientific Python.**

---

## 4.6 Scaling with Kubernetes

```yaml
resources:
  requests: {memory: "256Mi", cpu: "250m"}
  limits:   {memory: "512Mi", cpu: "500m"}
readinessProbe:
  httpGet: {path: /health, port: 8000}
livenessProbe:
  httpGet: {path: /health, port: 8000}
```

### ⚠️ Readiness and liveness are not the same thing

| Probe | Question | Failing it means |
|---|---|---|
| **Readiness** | should this pod receive traffic? | **removed from the load balancer** |
| **Liveness** | is this pod broken? | **restarted** |

> **Getting them the wrong way round gives you a pod that is restarted every
> time it is briefly slow**, which turns a latency spike into an outage. This
> is the standard Kubernetes exam question.

### 📖 Requests against limits

**`requests` is what the scheduler reserves; `limits` is where the container
is killed.** A container with no memory limit can take down its node — and an
ML container loading a large model is exactly the kind that does.

### 📖 Horizontal against vertical scaling

| | **Horizontal** | **Vertical** |
|---|---|---|
| Means | more instances | a bigger machine |
| Limit | coordination overhead | **the largest machine available** |
| Suits | **stateless services** — an inference API is one | databases, training jobs |

**An inference API is stateless and scales horizontally almost perfectly**,
which is why it is the easy case. Training does not: it scales vertically
until you need distributed training, which is a different problem.

---

## What to be able to do after this unit

- [ ] List what a model needs before it is deployable
- [ ] **Say why returning 400 with a reason matters more than the model**
- [ ] Name five ways dev and production differ, and the single mitigation
- [ ] Give the CI/CD stages, and the **two** with no software equivalent
- [ ] **Explain the metric gate and why it compares against production**
- [ ] Explain why a non-deterministic pipeline makes CI meaningless
- [ ] Distinguish batch, online, streaming and embedded deployment
- [ ] **Compare canary, blue-green, A/B and shadow**, and say which is zero-risk
- [ ] Give three Docker traps and their fixes
- [ ] **Explain the requirements-before-code ordering** in terms of layer caching
- [ ] **Distinguish readiness from liveness**, and say what going wrong costs

**Cross-check yourself:** run
`12_serve_drift_govern.py`
and
`07_mlflow_dvc.py`.
