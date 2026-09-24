"""Experiment 15 -- deploy a trained ML model as a REST API endpoint.

`15_deploy.md` carries the SageMaker deploy call and the console steps, NOT
EXECUTED -- there is no cloud account.

But the ENDPOINT ITSELF RUNS HERE. A real HTTP server starts on localhost,
serves a real scikit-learn model over a real JSON API, is called with real
requests, and is shut down. The contract, the error handling, the health
check and the latency measurements are genuine -- only the hosting is not.

That is the honest split: SageMaker gives you a container, a load balancer,
autoscaling and an IAM-signed URL. What it serves is this.
"""
import json
import os
import tempfile
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

import joblib
import numpy as np

import fixtures as f
from sklearn.datasets import make_classification
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SEED = 42
N_FEATURES = 10
HOST = "127.0.0.1"
PORT = 0          # the OS picks a free port; the real one is read back

_MODEL = None
_STATE = {"invocations": 0, "errors_4xx": 0, "errors_5xx": 0,
          "latencies": []}


class Handler(BaseHTTPRequestHandler):
    """The two routes every model endpoint must have, and no more."""

    def log_message(self, *args):
        pass                                  # keep the suite output clean

    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/ping":
            # SageMaker calls THIS to decide whether the container is alive.
            # It must not run the model: a health check that does real work
            # takes the endpoint down when the model is merely slow.
            self._send(200, {"status": "healthy",
                             "model_loaded": _MODEL is not None})
        elif self.path == "/metrics":
            self._send(200, dict(_STATE, latencies=len(_STATE["latencies"])))
        else:
            _STATE["errors_4xx"] += 1
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/invocations":
            _STATE["errors_4xx"] += 1
            self._send(404, {"error": "not found"})
            return
        started = time.perf_counter()
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
            rows = payload.get("instances")
            if not isinstance(rows, list) or not rows:
                raise ValueError("body must be {'instances': [[...], ...]}")
            arr = np.asarray(rows, dtype=float)
            if arr.ndim != 2 or arr.shape[1] != N_FEATURES:
                raise ValueError(
                    f"each instance needs {N_FEATURES} features, "
                    f"got shape {list(arr.shape)}")
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            # A BAD REQUEST IS A 4XX, NOT A 5XX. Getting this wrong makes
            # your error alarm fire for other people's mistakes.
            _STATE["errors_4xx"] += 1
            self._send(400, {"error": str(exc)})
            return
        try:
            proba = _MODEL.predict_proba(arr)[:, 1]
            preds = (proba >= 0.5).astype(int)
        except Exception as exc:                       # pragma: no cover
            _STATE["errors_5xx"] += 1
            self._send(500, {"error": "inference failed"})
            return
        _STATE["invocations"] += len(rows)
        _STATE["latencies"].append((time.perf_counter() - started) * 1000)
        self._send(200, {"predictions": preds.tolist(),
                         "probabilities": [round(p, 6) for p in proba]})


def build_model():
    X, y = make_classification(
        n_samples=1200, n_features=N_FEATURES, n_informative=5,
        n_redundant=2, weights=[0.85, 0.15], flip_y=0.02,
        class_sep=1.1, random_state=SEED)
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=SEED)
    pipe = Pipeline([("scale", StandardScaler()),
                     ("clf", GradientBoostingClassifier(random_state=SEED))])
    pipe.fit(Xtr, ytr)
    return pipe, Xte, yte


_PORT = None


def call(path, payload=None, method="GET"):
    url = f"http://{HOST}:{_PORT}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json"} if data else {})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read())


def percentile(values, p):
    s = sorted(values)
    k = (len(s) - 1) * p / 100
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def main():
    global _MODEL, _PORT
    print("  Experiment 15 -- a model deployed as a REST endpoint, "
          "actually served")

    model, X_test, y_test = build_model()
    path = os.path.join(tempfile.gettempdir(), "cloud13b_endpoint.joblib")
    joblib.dump(model, path)
    _MODEL = joblib.load(path)
    print(f"\n    artefact loaded from disk: {os.path.getsize(path):,} bytes")

    HTTPServer.allow_reuse_address = True
    server = HTTPServer((HOST, PORT), Handler)
    global _PORT
    _PORT = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"    endpoint listening on http://{HOST}:{_PORT}  "
          f"(a REAL HTTP server)")

    try:
        # ---- health check ------------------------------------------------
        code, body = call("/ping")
        print(f"\n    GET /ping        -> {code} {body}")
        assert code == 200 and body["model_loaded"] is True
        print("""         /ping answers WITHOUT running the model. A health check
         that does real inference marks the container unhealthy
         whenever the model is merely slow, and the platform then
         kills a container that was working -- a self-inflicted
         outage, and a classic one""")

        # ---- a real prediction -------------------------------------------
        sample = X_test[:3].tolist()
        code, body = call("/invocations", {"instances": sample}, "POST")
        print(f"\n    POST /invocations with 3 rows -> {code}")
        print(f"      predictions   : {body['predictions']}")
        print(f"      probabilities : {body['probabilities']}")
        assert code == 200 and len(body["predictions"]) == 3
        local = model.predict(X_test[:3]).tolist()
        assert body["predictions"] == local
        print("""         the endpoint's answers are IDENTICAL to calling the model
         in-process. That equality is the deployment test worth
         writing: serving must not change predictions, and a
         preprocessing step that lives in your notebook rather than
         in the pipeline is exactly how it does""")

        # ---- batch --------------------------------------------------------
        code, body = call("/invocations",
                          {"instances": X_test.tolist()}, "POST")
        assert code == 200
        preds = np.array(body["predictions"])
        acc = (preds == y_test).mean()
        print(f"\n    POST /invocations with all {len(X_test)} rows -> {code}, "
              f"accuracy {acc:.4f}")
        assert acc > 0.90

        # ---- the errors ---------------------------------------------------
        print("\n    error handling, which is most of a real endpoint:")
        cases = [
            ("wrong feature count", {"instances": [[1.0, 2.0]]}, "POST",
             "/invocations"),
            ("not a list", {"instances": "hello"}, "POST", "/invocations"),
            ("empty body", {}, "POST", "/invocations"),
            ("wrong route", {"instances": sample}, "POST", "/predict"),
            ("wrong route, GET", None, "GET", "/predict"),
        ]
        print(f"      {'case':<24}{'status':>8}  message")
        for label, payload, method, route in cases:
            code, body = call(route, payload, method)
            msg = body.get("error", "")[:46]
            print(f"      {label:<24}{code:>8}  {msg}")
            assert 400 <= code < 500, "a client mistake must not be a 5xx"
        print("""         EVERY ONE IS A 4XX, NOT A 5XX, and that distinction is
         operational rather than pedantic: 5xx means YOUR service is
         broken and should page someone. If malformed client input
         returns 500, your error alarm fires for other people's bugs
         and you stop trusting it""")

        # ---- latency -------------------------------------------------------
        print("\n    latency over 200 single-row requests:")
        _STATE["latencies"].clear()
        for i in range(200):
            code, _ = call("/invocations",
                           {"instances": [X_test[i % len(X_test)].tolist()]},
                           "POST")
            assert code == 200
        lat = _STATE["latencies"]
        p50, p95, p99 = (percentile(lat, p) for p in (50, 95, 99))
        mean = sum(lat) / len(lat)
        print(f"      mean {mean:.3f} ms   p50 {p50:.3f} ms   "
              f"p95 {p95:.3f} ms   p99 {p99:.3f} ms")
        assert p99 >= p50
        print(f"""         p99 is {p99 / p50:.1f}x p50 on an idle laptop serving one model.
         On a shared endpoint under load that ratio grows, which is
         why the alarm in experiment 13 is on p99 and not the mean.
         These are SERVER-SIDE numbers; a client also pays network
         time, and the user's experience is the sum""")

        # ---- batching -------------------------------------------------------
        print("\n    one request of 100 rows against 100 requests of one row:")
        _STATE["latencies"].clear()
        t0 = time.perf_counter()
        call("/invocations", {"instances": X_test[:100].tolist()}, "POST")
        batched = (time.perf_counter() - t0) * 1000
        t0 = time.perf_counter()
        for i in range(100):
            call("/invocations", {"instances": [X_test[i].tolist()]}, "POST")
        singly = (time.perf_counter() - t0) * 1000
        print(f"      batched  : {batched:8.2f} ms total")
        print(f"      one by one: {singly:8.2f} ms total "
              f"({singly / batched:.0f}x)")
        assert singly > batched
        print(f"""         {singly / batched:.0f}x, and none of it is the model -- it is per-request
         overhead: HTTP, JSON parsing, and a NumPy call whose fixed
         cost is paid 100 times instead of once.
         This is why batch transform exists alongside real-time
         endpoints. If you are scoring a file of a million rows,
         calling an endpoint a million times is the expensive way to
         do arithmetic""")

        # ---- metrics --------------------------------------------------------
        code, metrics = call("/metrics")
        print(f"\n    GET /metrics -> {metrics['invocations']:,} invocations, "
              f"{metrics['errors_4xx']} 4xx, {metrics['errors_5xx']} 5xx")
        assert metrics["errors_5xx"] == 0

    finally:
        server.shutdown()
        server.server_close()
        os.remove(path)
        print("\n    endpoint shut down and artefact removed.")

    # ---- and the part that is NOT simulated -----------------------------
    print("\n    what SageMaker adds that this server does not have:")
    print(f"      {'':<26}{'this script':<22}{'a managed endpoint'}")
    for label, here, cloud in (
            ("TLS", "no", "yes, terminated for you"),
            ("authentication", "NONE -- anyone", "IAM-signed requests"),
            ("load balancing", "one process", "across instances and AZs"),
            ("autoscaling", "no", "on InvocationsPerInstance"),
            ("blue/green deploy", "no", "traffic shifted gradually"),
            ("metrics", "the dict above", "CloudWatch, automatically"),
            ("cost", "electricity", "PER HOUR, until deleted")):
        print(f"      {label:<26}{here:<22}{cloud}")
    hourly = f.EC2["m5.large"]
    print(f"\n      an ml.m5.large endpoint: ${hourly:.4f}/hour "
          f"= ${hourly * f.HOURS_PER_MONTH:,.2f}/month, called or not")
    print("""         THE LAST ROW AGAIN. A training job stops; an endpoint does
         not. Deleting the endpoint is a step in the experiment, not
         an afterthought -- and if traffic is occasional, a serverless
         endpoint or batch transform costs a fraction of it""")


if __name__ == "__main__":
    main()
