# Experiment 15 — logging and monitoring with Prometheus and Grafana

## *** NOT EXECUTED ***

**Prometheus and Grafana are both server processes**, and neither can be
installed here — this environment's egress policy blocks the Debian
repositories, and neither is pip-installable as a server. **Nothing in this
file has been run**, and nothing in the notes claims an output for it.

**The runnable half is `12_serve_drift_govern.py`**,
which serves a real `/metrics` endpoint in **Prometheus exposition format**,
calls it over HTTP, and parses the response back to confirm the format is
valid:

```
# HELP model_requests_total Total prediction requests.
# TYPE model_requests_total counter
model_requests_total 3
# HELP model_errors_total Total rejected requests.
# TYPE model_errors_total counter
model_errors_total 2
# HELP model_latency_seconds Prediction latency.
# TYPE model_latency_seconds gauge
model_latency_seconds 0.160414
```

> ### 🎯 That endpoint is the entire contract
>
> **Prometheus does not need an agent inside your application.** It *scrapes*
> a plain-text HTTP endpoint on a schedule. Producing that text correctly is
> the part you control and the part that is verified above; running the
> scraper and drawing the dashboard is the part this environment cannot do.

---

## The proper client library

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from flask import Flask, Response

REQUESTS = Counter("model_requests_total",
                   "Prediction requests", ["outcome"])
LATENCY = Histogram("model_latency_seconds",
                    "Prediction latency",
                    buckets=[.005, .01, .025, .05, .1, .25, .5, 1, 2.5])
DRIFT = Gauge("model_feature_psi", "PSI against training", ["feature"])
MODEL_VERSION = Gauge("model_version_info", "Deployed version", ["version"])


@app.post("/predict")
def predict():
    with LATENCY.time():
        ...
        REQUESTS.labels(outcome="approved" if approved else "declined").inc()


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")
```

### The four metric types, and choosing between them

| Type | Only ever | Use for |
|---|---|---|
| **Counter** | goes **up** (or resets to 0) | requests, errors, predictions |
| **Gauge** | goes up **and down** | queue depth, PSI, memory, model version |
| **Histogram** | buckets, summed server-side | **latency** — lets you compute p95 across instances |
| Summary | quantiles computed client-side | rarely the right choice |

> ### ⚠️ Use a Histogram for latency, not a Gauge
>
> A gauge holding "the mean latency" **cannot be aggregated**. Averaging the
> means of four instances is not the mean, and there is no way to recover p95
> at all. A histogram ships the bucket counts, and `histogram_quantile()`
> computes the percentile across every instance correctly.
>
> The runnable half uses a gauge for simplicity and **its output above says
> `gauge` honestly** — that is a simplification, not a recommendation.

---

## Prometheus configuration

`prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - alerts.yml

scrape_configs:
  - job_name: loan-model
    static_configs:
      - targets: ["loan-model:8000"]
```

`alerts.yml` — **the part that matters**:

```yaml
groups:
  - name: model
    rules:
      - alert: HighErrorRate
        expr: |
          rate(model_requests_total{outcome="error"}[5m])
          / rate(model_requests_total[5m]) > 0.05
        for: 10m
        labels: {severity: page}
        annotations:
          summary: "Over 5% of predictions are failing"

      - alert: LatencyP95High
        expr: histogram_quantile(0.95,
                rate(model_latency_seconds_bucket[5m])) > 0.5
        for: 10m
        labels: {severity: warning}

      - alert: FeatureDrift
        expr: model_feature_psi > 0.2
        for: 1h
        labels: {severity: warning}
        annotations:
          summary: "PSI above 0.2 -- see experiment 13"
```

### 🎯 `for: 10m` is the most important line in the file

**Without it, one slow request pages somebody at 03:00.** The `for` clause
requires the condition to hold continuously before the alert fires, and
choosing it is the whole craft of alerting: too short and you train people to
ignore alerts; too long and you find out from a customer.

**Note that `FeatureDrift` uses `for: 1h`** — drift is a slow phenomenon and a
single noisy batch should not page anyone. That threshold of 0.2 is the same
one `12_serve_drift_govern.py` measures against
known injected drift, where it caught 4 of 5 drifted batches with 0 false
alarms.

---

## Grafana

```bash
docker run -d -p 3000:3000 grafana/grafana:11.4.0
# add Prometheus as a data source at http://prometheus:9090
```

### The four panels a model dashboard needs

| Panel | Query |
|---|---|
| **Request rate** | `rate(model_requests_total[5m])` |
| **Error rate** | `rate(model_requests_total{outcome="error"}[5m]) / rate(model_requests_total[5m])` |
| **Latency p50/p95/p99** | `histogram_quantile(0.95, rate(model_latency_seconds_bucket[5m]))` |
| **Feature drift** | `model_feature_psi` — one line per feature |

> ### 💡 And the panel nobody builds, which is the one that matters
>
> **The prediction distribution over time** — what fraction of applications
> the model approves, by day.
>
> Every panel above monitors the *service*. That one monitors the *model*. A
> model can be fast, error-free and approving 90% of applications when it used
> to approve 45%, and **only this panel shows it.**

### The four golden signals, for reference

**Latency, traffic, errors, saturation.** They come from Google's SRE book and
apply to any service. **For an ML service you add a fifth: prediction
distribution**, for the reason above.

---

## Logging, which the syllabus names alongside monitoring

**Metrics and logs answer different questions.** Metrics tell you *that*
something is wrong; logs tell you *what*.

```python
import logging, json, uuid

logging.basicConfig(format="%(message)s", level=logging.INFO)


def log_prediction(features, probability, version):
    logging.info(json.dumps({
        "event": "prediction",
        "request_id": str(uuid.uuid4()),
        "model_version": version,
        "probability": round(probability, 6),
        "features": features,           # see the warning below
        "ts": time.time(),
    }))
```

> ### ⚠️ Two rules for ML logging
>
> **1. Log structured JSON, not prose.** `"Predicted 0.83 for user 42"` cannot
> be queried; a JSON object can.
>
> **2. Logging the features is how you detect drift later — and it is
> personal data.** Under GDPR that log is subject to the same retention and
> erasure rules as the database, which experiment 16 covers. Log a hashed
> subject id, set a retention period, and be able to delete.

---

## What goes in the lab record

| Item | Value |
|---|---|
| Your `/metrics` output (or the one from `12_serve_drift_govern.py`) | |
| `prometheus.yml`, and a screenshot of the target as **UP** | |
| A Grafana screenshot with all four panels | |
| An alert you deliberately triggered, and its firing time | |
| The `for:` duration you chose, **and why** | |
| One structured log line | |

One paragraph: **your latency gauge reads 0.16 s. Explain why that number
cannot be aggregated across three instances, and what a histogram would give
you instead.**
