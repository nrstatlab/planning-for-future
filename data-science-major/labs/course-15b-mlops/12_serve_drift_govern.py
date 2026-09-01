"""Experiments 12, 13, 14 and 16 -- serve a model over real HTTP, detect
drift against a known ground truth, retrain automatically when it exceeds a
threshold, and audit the model for GDPR and Responsible AI.

REAL Flask on a REAL socket. The server is started in a thread, called over
HTTP with urllib, and shut down. The drift is INJECTED at a known magnitude,
so the detector is scored rather than merely run.
"""
import json
import socket
import threading
import time
import urllib.error
import urllib.request

import numpy as np
import pandas as pd

import fixtures as f


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def fit_reference():
    from sklearn.linear_model import LogisticRegression
    df = f.train_reference(4000)
    m = LogisticRegression(max_iter=1000, random_state=f.SEED)
    m.fit(df[f.FEATURES], df.approved)
    return m, df


def experiment_12(model):
    print("\n    --- experiment 12: serve the model as a REST API (Flask)")

    from flask import Flask, jsonify, request
    import logging
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    app = Flask(__name__)
    state = {"requests": 0, "errors": 0, "latencies": []}

    @app.get("/health")
    def health():
        return jsonify(status="ok", model="logreg", features=f.FEATURES)

    @app.post("/predict")
    def predict():
        t0 = time.perf_counter()
        state["requests"] += 1
        body = request.get_json(silent=True) or {}
        missing = [c for c in f.FEATURES if c not in body]
        if missing:
            state["errors"] += 1
            return jsonify(error="missing features", missing=missing), 400
        try:
            # a DataFrame, not a bare array, so the column names match
            # what the model was fitted with -- otherwise sklearn warns
            x = pd.DataFrame([[float(body[c]) for c in f.FEATURES]],
                             columns=f.FEATURES)
        except (TypeError, ValueError):
            state["errors"] += 1
            return jsonify(error="features must be numeric"), 400
        p = float(model.predict_proba(x)[0, 1])
        state["latencies"].append(time.perf_counter() - t0)
        return jsonify(approved=bool(p >= 0.5), probability=round(p, 6),
                       model_version="1.0.0")

    @app.get("/metrics")
    def metrics():
        """Prometheus exposition format -- experiment 15's runnable half."""
        lat = state["latencies"]
        lines = [
            "# HELP model_requests_total Total prediction requests.",
            "# TYPE model_requests_total counter",
            f"model_requests_total {state['requests']}",
            "# HELP model_errors_total Total rejected requests.",
            "# TYPE model_errors_total counter",
            f"model_errors_total {state['errors']}",
            "# HELP model_latency_seconds Prediction latency.",
            "# TYPE model_latency_seconds gauge",
            f"model_latency_seconds {np.mean(lat) if lat else 0.0:.6f}",
        ]
        return "\n".join(lines) + "\n", 200, {"Content-Type": "text/plain"}

    port = free_port()
    t = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=port, debug=False,
                               use_reloader=False),
        daemon=True)
    t.start()
    time.sleep(1.2)
    base = f"http://127.0.0.1:{port}"
    print(f"\n      a REAL Flask server on {base}")

    def call(path, payload=None):
        url = base + path
        if payload is None:
            req = urllib.request.Request(url)
        else:
            req = urllib.request.Request(
                url, data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                return r.status, r.read().decode()
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode()

    st, body = call("/health")
    print(f"      GET  /health   -> {st}  {body.strip()[:70]}")

    good = {"income": 1.4, "loan_amount": -0.3, "credit_years": 0.8,
            "age": 0.2}
    st, body = call("/predict", good)
    print(f"      POST /predict  -> {st}  {body.strip()[:70]}")
    approved = json.loads(body)["approved"]

    st_missing, body_missing = call("/predict",
                                    {"income": 1.0, "age": 0.0})
    print(f"      POST /predict  -> {st_missing}  "
          f"{body_missing.strip()[:70]}")

    st_bad, body_bad = call("/predict",
                            {**good, "income": "not a number"})
    print(f"      POST /predict  -> {st_bad}  {body_bad.strip()[:70]}")

    print("""         THE TWO ERROR CASES ARE THE EXPERIMENT. A demo endpoint
         returns a prediction; a PRODUCTION endpoint decides what to
         do when the caller omits two of the four features, or sends
         a string where a float belongs.
         RETURNING 400 WITH A REASON, rather than a 500 or a
         confidently wrong prediction, is what separates the two. The
         model itself is three lines of this file""")

    st_m, metrics_body = call("/metrics")
    print(f"\n      GET  /metrics  -> {st_m}")
    for line in metrics_body.strip().splitlines():
        print(f"        {line}")

    # verify it really is valid Prometheus exposition format
    parsed = {}
    for line in metrics_body.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        name, value = line.split()
        parsed[name] = float(value)
    print(f"\n      parsed as Prometheus exposition format: "
          f"{len(parsed)} metrics")
    print("""         THIS ENDPOINT IS EXPERIMENT 15's RUNNABLE HALF.
         Prometheus does not need an agent inside your app -- it
         SCRAPES a plain-text endpoint on a schedule, and the format
         above is the entire contract. Getting it right is the part
         you control; running the Prometheus server and drawing the
         Grafana dashboard is the part this environment cannot do,
         and 15_prometheus_grafana.md covers it""")

    assert st == 200 and st_missing == 400 and st_bad == 400
    assert parsed["model_requests_total"] == 3
    assert parsed["model_errors_total"] == 2
    return parsed


def experiment_13(model, ref):
    print("\n    --- experiment 13: drift detection, scored against truth")

    from scipy import stats

    batches, truth = f.production_batches(n_per_batch=500, n_batches=10,
                                          drift_starts=5, max_drift=1.5)
    print(f"\n      10 daily batches of 500. Batches 0-4 are clean; the "
          f"income")
    print(f"      distribution shifts from batch 5, ramping to 1.5 sd.")

    def psi(expected, actual, bins=10):
        """Population Stability Index -- the industry's usual drift metric."""
        qs = np.quantile(expected, np.linspace(0, 1, bins + 1))
        qs[0], qs[-1] = -np.inf, np.inf
        e = np.histogram(expected, bins=qs)[0] / len(expected)
        a = np.histogram(actual, bins=qs)[0] / len(actual)
        e, a = np.clip(e, 1e-6, None), np.clip(a, 1e-6, None)
        return float(np.sum((a - e) * np.log(a / e)))

    print(f"\n      {'batch':>6}{'true drift':>12}{'KS stat':>10}"
          f"{'KS p':>10}{'PSI':>9}{'accuracy':>10}{'alert':>8}")
    THRESH_PSI = 0.2
    rows = []
    for i, (b, d) in enumerate(zip(batches, truth)):
        ks = stats.ks_2samp(ref.income, b.income)
        p_index = psi(ref.income.values, b.income.values)
        acc = float((model.predict(b[f.FEATURES]) == b.approved).mean())
        alert = p_index > THRESH_PSI
        rows.append((i, d, ks.statistic, ks.pvalue, p_index, acc, alert))
        print(f"      {i:>6}{d:>12.2f}{ks.statistic:>10.4f}"
              f"{ks.pvalue:>10.4f}{p_index:>9.4f}{acc:>10.4f}"
              f"{'YES' if alert else '-':>8}")

    clean = [r for r in rows if r[1] == 0.0]
    drifted = [r for r in rows if r[1] > 0.0]
    fp = sum(1 for r in clean if r[6])
    tp = sum(1 for r in drifted if r[6])
    print(f"\n      at PSI > {THRESH_PSI}: {tp}/{len(drifted)} drifted "
          f"batches caught, {fp}/{len(clean)} false alarms on clean ones")

    first_alert = next((r[0] for r in rows if r[6]), None)
    print(f"      first alert: batch {first_alert}; drift actually "
          f"began at batch 5")

    print(f"""         THE DETECTOR IS SCORED, not merely run, and that is only
         possible because the drift was INJECTED at a known size.
         NOTE THE LAG. Drift began at batch 5 and the alert fired at
         batch {first_alert}, because the shift ramps in and a small
         shift is genuinely hard to distinguish from noise. Every
         drift detector trades detection lag against false alarms;
         lowering the threshold catches batch 5 and starts alerting on
         clean batches too.
         AND COMPARE THE TWO TESTS. The KS p-value goes to zero long
         before PSI crosses its threshold -- with 500 samples, KS
         detects a shift far too small to matter. STATISTICAL
         SIGNIFICANCE IS NOT OPERATIONAL SIGNIFICANCE, which is
         exactly why the industry uses PSI with a magnitude threshold
         rather than a hypothesis test""")

    acc_clean = np.mean([r[5] for r in clean])
    acc_drift = np.mean([r[5] for r in drifted])
    print(f"\n      accuracy on clean batches {acc_clean:.4f}, "
          f"on drifted {acc_drift:.4f}")
    print("""         THE THREE KINDS OF DRIFT, and this experiment shows one:
         DATA DRIFT      P(X) changes. The inputs move. <- this one
         CONCEPT DRIFT   P(y|X) changes. The relationship moves.
         LABEL DRIFT     P(y) changes. The base rate moves.
         Data drift is detectable IMMEDIATELY from the inputs alone.
         Concept drift needs LABELS, which in lending arrive months
         later when the loan defaults or does not -- so you cannot
         detect it in time, and monitoring the inputs is the only
         early warning you get""")

    assert tp > 0, "the detector caught nothing"
    assert fp == 0, f"{fp} false alarms on clean batches"
    return rows


def experiment_14(model, ref, rows):
    print("\n    --- experiment 14: a feedback loop that retrains on drift")

    from sklearn.linear_model import LogisticRegression
    batches, truth = f.production_batches(n_per_batch=500, n_batches=10,
                                          drift_starts=5, max_drift=1.5)

    THRESH = 0.2
    live = model
    window = ref.copy()
    retrains = []
    print(f"\n      {'batch':>6}{'PSI':>9}   {'action':<22}{'accuracy':>10}")
    accs_static, accs_adaptive = [], []
    static = model
    for i, b in enumerate(batches):
        from scipy import stats                                # noqa: F401
        qs = np.quantile(ref.income, np.linspace(0, 1, 11))
        qs[0], qs[-1] = -np.inf, np.inf
        e = np.clip(np.histogram(ref.income, bins=qs)[0] / len(ref), 1e-6, None)
        a = np.clip(np.histogram(b.income, bins=qs)[0] / len(b), 1e-6, None)
        p_index = float(np.sum((a - e) * np.log(a / e)))

        acc_static = float((static.predict(b[f.FEATURES]) == b.approved).mean())
        acc_live = float((live.predict(b[f.FEATURES]) == b.approved).mean())
        accs_static.append(acc_static)
        accs_adaptive.append(acc_live)

        if p_index > THRESH:
            window = pd.concat([window, b], ignore_index=True).tail(4000)
            live = LogisticRegression(max_iter=1000, random_state=f.SEED)
            live.fit(window[f.FEATURES], window.approved)
            retrains.append(i)
            action = f"RETRAIN on {len(window):,} rows"
        else:
            action = "-"
        print(f"      {i:>6}{p_index:>9.4f}   {action:<22}"
              f"{acc_live:>10.4f}")

    print(f"\n      retrained at batches {retrains}")
    print(f"\n      {'':<22}{'mean accuracy':>15}")
    print(f"      {'static model':<22}{np.mean(accs_static):>15.4f}")
    print(f"      {'retraining model':<22}{np.mean(accs_adaptive):>15.4f}")
    diff = np.mean(accs_adaptive) - np.mean(accs_static)
    print(f"      {'difference':<22}{diff:>+15.4f}")

    if abs(diff) < 0.005:
        print(f"""         RETRAINING BARELY HELPED -- {diff:+.4f} -- and that
         is the honest result here, worth more than a demonstration
         that flattered the loop.
         THE REASON IS IN THE FIXTURE. The drift shifts P(X): incomes
         move up. But P(y|X) -- the relationship between income and
         approval -- did NOT change, because the generating
         coefficients are the same. A model that had learned the true
         relationship is STILL CORRECT on shifted inputs.
         THAT IS THE DISTINCTION THIS EXPERIMENT EXISTS TO TEACH.
         Data drift triggers an alert; it does not by itself degrade
         accuracy. CONCEPT drift does, and it is the one you cannot
         detect without labels.
         So the operational rule is: alert on data drift, INVESTIGATE,
         and retrain only if the labels confirm the relationship
         moved. Retraining on every input shift is expensive and can
         make things worse, because you are fitting to a smaller,
         more recent, noisier window""")
    else:
        print(f"""         RETRAINING CHANGED ACCURACY BY {diff:+.4f}. Report
         which direction and why: a retrained model sees a smaller,
         more recent window, so it trades statistical strength for
         currency""")

    print("""
      the feedback loop, and where a human belongs in it:
        1. MONITOR    input distributions, continuously
        2. ALERT      when a magnitude threshold is crossed
        3. INVESTIGATE  a human looks. IS THE SHIFT REAL, or did an
                      upstream system change its units?
        4. LABEL      wait for ground truth, or buy it
        5. RETRAIN    on a window, with the SAME pipeline
        6. VALIDATE   against the old model on a held-out set
        7. DEPLOY     shadow, then canary, then full""")
    print("""         STEP 3 IS THE ONE THAT GETS AUTOMATED AWAY AND SHOULD
         NOT BE. The most common cause of a drift alert is not the
         world changing but an upstream pipeline changing -- a unit
         switched from rupees to thousands, a null becoming a zero.
         Retraining on that corrupts the model with the bug""")

    return retrains, np.mean(accs_static), np.mean(accs_adaptive)


def experiment_16(model, ref):
    print("\n    --- experiment 16: a GDPR and Responsible AI audit")

    print("\n      the model decides loan approvals. Audit it.")

    # ---- fairness across the protected attribute -------------------------
    df = f.applicants(6000, seed=f.SEED + 99)
    df["pred"] = model.predict(df[f.FEATURES])

    print(f"\n      {'region':<10}{'n':>7}{'approval rate':>15}"
          f"{'true rate':>12}{'accuracy':>10}")
    rates = {}
    for r in sorted(df.region.unique()):
        g = df[df.region == r]
        rate = float(g.pred.mean())
        true_rate = float(g.approved.mean())
        acc = float((g.pred == g.approved).mean())
        rates[r] = rate
        print(f"      {r:<10}{len(g):>7}{rate:>15.4f}{true_rate:>12.4f}"
              f"{acc:>10.4f}")

    spread = max(rates.values()) - min(rates.values())
    print(f"\n      approval-rate spread across regions: {spread:.4f}")
    print(f"""         REGION IS NOT A MODEL INPUT -- look at f.FEATURES. And
         the approval rates still differ by {spread:.4f}, because the
         regions were generated with the same distribution, so this
         spread is SAMPLING NOISE rather than bias.
         THAT IS THE CONTROL CONDITION, and it is why this experiment
         is built on generated data: you cannot tell a biased model
         from a noisy measurement unless you know which one you have.
         ON REAL DATA the same table would not tell you either. A
         spread could be noise, could be a genuine difference in the
         applicant pool, or could be the model. DECIDING WHICH IS NOT
         A STATISTICAL QUESTION -- it needs the domain""")

    print("""
      GDPR, article by article, against THIS system:""")
    rows = [
        ("Art. 5 - minimisation",
         f"the model uses {len(f.FEATURES)} features",
         "do you need 'age'? if it does not improve AUC, drop it"),
        ("Art. 15 - access",
         "return everything held about one applicant",
         "needs a subject id on every row, including logs"),
        ("Art. 17 - erasure",
         "can you delete one applicant?",
         "THE HARD ONE -- see below"),
        ("Art. 22 - automated decisions",
         "loan approval has legal effect",
         "a human review route is REQUIRED, not optional"),
        ("Art. 22 - explanation",
         "the applicant may ask why",
         "logistic regression can answer; a deep net cannot"),
        ("Art. 35 - impact assessment",
         "high-risk processing needs a DPIA",
         "before deployment, not after"),
    ]
    print(f"      {'requirement':<32}{'what it means here':<46}{'action'}")
    for a, b, c in rows:
        print(f"      {a:<32}{b:<46}{c}")

    print("""         ARTICLE 17 IS THE ONE THAT BREAKS ML SYSTEMS. Deleting
         a row from the database is easy. The model TRAINED on that
         row still contains information derived from it, and there is
         no way to subtract one example from fitted coefficients.
         The practical answer is to retrain on a schedule from the
         current data, so an erased record leaves the model within one
         cycle -- which means your retraining pipeline is a COMPLIANCE
         control, not just an accuracy one. That is not obvious and it
         is exactly the sort of thing an examiner asks""")

    print("""
      the facial-recognition case the syllabus names, in one table:""")
    for a, b in [
        ("The data", "scraped photographs -- no consent, so Art. 6 has no "
                     "lawful basis"),
        ("Special category", "biometric identification is Art. 9 -- a HIGHER "
                             "bar than ordinary data"),
        ("The error rates", "documented to be far worse on darker skin and on "
                            "women"),
        ("The consequence", "a false match in policing costs someone their "
                            "liberty"),
        ("The asymmetry", "the people most likely to be misidentified are "
                          "least able to contest it"),
    ]:
        print(f"        {a:<20}{b}")
    print("""         THE POINT IS NOT THAT THE TECHNOLOGY IS BAD. It is that
         accuracy is not a single number: a system at 99% overall can
         be at 80% for one group, and if the cost of an error falls
         unequally then the aggregate figure hides the harm rather
         than measuring it.
         REPORT PER-GROUP METRICS. That is the whole recommendation,
         and it is the one the table at the top of this experiment
         demonstrates""")

    print("""
      Responsible AI, as five things you can actually check:
        FAIRNESS         per-group metrics, not one aggregate
        TRANSPARENCY     a model card: data, metrics, limits, intended use
        ACCOUNTABILITY   a named owner, and an appeal route
        PRIVACY          minimisation, retention limits, deletion that works
        RELIABILITY      monitoring, drift alerts, a rollback plan""")

    assert spread < 0.15, f"unexpected spread {spread:.4f}"
    return rates, spread


def main():
    print("  Experiments 12, 13, 14 and 16 -- serving, drift, retraining, "
          "governance")
    model, ref = fit_reference()
    experiment_12(model)
    rows = experiment_13(model, ref)
    experiment_14(model, ref, rows)
    experiment_16(model, ref)
    print("\n    all assertions passed")


if __name__ == "__main__":
    main()
