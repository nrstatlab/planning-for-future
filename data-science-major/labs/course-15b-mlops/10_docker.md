# Experiment 10 — containerize an ML model with Docker

## *** NOT EXECUTED ***

**The Docker client is installed here but there is no daemon.** `docker info`
reports the client and then:

```
failed to connect to the docker API at unix:///var/run/docker.sock;
check if the path is correct and if the daemon is running
```

So no image can be built and no container run. **Nothing in this file has been
run**, and nothing in the notes claims an output for it.

**The runnable half is `12_serve_drift_govern.py`**,
which runs the *same Flask application* directly — a real server on a real
socket, called over HTTP, with `/health`, `/predict` and `/metrics` all
exercised and their status codes asserted. **The container adds packaging, not
behaviour**, so the application below is already verified; what is unverified
is the Dockerfile.

---

## The Dockerfile

```dockerfile
# 1. A specific, slim base. NOT "python:latest" -- that is a moving target
#    and your build stops being reproducible the day it changes.
FROM python:3.11-slim AS base

# 2. Do not run as root. Containers are not a security boundary by default.
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# 3. Copy requirements FIRST, install, THEN copy the code.
#    This is the layer-caching trick and it is the single biggest
#    build-time win: the pip layer is only rebuilt when the
#    requirements change, not on every code edit.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Now the code and the model artifact.
COPY --chown=app:app app.py model.pkl ./

USER app

# 5. Document the port. EXPOSE does not publish it -- -p does.
EXPOSE 8000

# 6. A health check, so the orchestrator knows the difference between
#    "the process is running" and "the service works".
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; \
        urllib.request.urlopen('http://localhost:8000/health').read()"

# 7. gunicorn, NOT the Flask development server.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", \
     "--timeout", "30", "app:app"]
```

`requirements.txt` — **pinned exactly**:

```
flask==3.1.3
gunicorn==23.0.0
scikit-learn==1.9.0
numpy==2.4.0
pandas==2.3.3
```

`.dockerignore` — **the file everyone forgets**:

```
.git
.venv
__pycache__
*.pyc
mlruns/
data/
notebooks/
.dvc/cache
```

> **Without `.dockerignore`, `COPY . .` sends your entire `.git` directory and
> every cached dataset to the daemon as build context.** A 40 MB project
> becomes a 2 GB build. It is the most common reason a student's image is
> enormous.

---

## Building and running

```bash
docker build -t loan-model:1.0.0 .
docker images loan-model                  # check the size

docker run -d --name loan -p 8000:8000 loan-model:1.0.0
docker ps
docker logs loan

curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
     -H 'Content-Type: application/json' \
     -d '{"income":1.4,"loan_amount":-0.3,"credit_years":0.8,"age":0.2}'

docker stop loan && docker rm loan
```

---

## The seven traps, in the order people hit them

| # | Trap | Fix |
|---|---|---|
| 1 | `FROM python:latest` | **pin the tag** — `python:3.11-slim` |
| 2 | No `.dockerignore` | see above; check with `docker build` context size |
| 3 | `COPY . .` before `pip install` | **requirements first** — the cache layer |
| 4 | Running the Flask dev server | **gunicorn or uvicorn**; Flask says so itself at startup |
| 5 | `app.run(host="127.0.0.1")` | **`0.0.0.0`** — `127.0.0.1` inside a container is unreachable from outside |
| 6 | Running as root | `USER app` |
| 7 | Secrets baked into the image | **environment variables or a secret mount** — `docker history` shows every layer |

> ### 🎯 Trap 5 is the one that costs an afternoon
>
> The container starts, the logs look perfect, and `curl` from the host gets
> connection refused. **`127.0.0.1` inside a container refers to the
> container**, so binding there makes the service reachable only from inside
> itself. `0.0.0.0` binds all interfaces.

### 🔢 Image size, which is worth measuring

| Base | Approximate size |
|---|---|
| `python:3.11` | ~1 GB |
| **`python:3.11-slim`** | **~150 MB** |
| `python:3.11-alpine` | ~50 MB, **but** musl breaks many wheels — scikit-learn compiles from source and the build takes an hour |

**Slim is usually the right answer.** Alpine is smaller and is a trap for
scientific Python.

---

## Multi-stage, if the model needs building

```dockerfile
FROM python:3.11 AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /root/.local /home/app/.local
ENV PATH=/home/app/.local/bin:$PATH
COPY app.py model.pkl /app/
WORKDIR /app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

**The compiler and the build tools stay in the first stage and never reach the
shipped image.** For a compiled dependency this can halve the size.

---

## Kubernetes, which the syllabus also names

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: loan-model
spec:
  replicas: 3
  selector:
    matchLabels: {app: loan-model}
  template:
    metadata:
      labels: {app: loan-model}
    spec:
      containers:
      - name: api
        image: loan-model:1.0.0
        ports: [{containerPort: 8000}]
        resources:
          requests: {memory: "256Mi", cpu: "250m"}
          limits:   {memory: "512Mi", cpu: "500m"}
        readinessProbe:
          httpGet: {path: /health, port: 8000}
          initialDelaySeconds: 5
        livenessProbe:
          httpGet: {path: /health, port: 8000}
          initialDelaySeconds: 15
```

> ### ⚠️ `readinessProbe` and `livenessProbe` are not the same thing
>
> **Readiness** — "should this pod receive traffic?" Failing removes it from
> the load balancer. **Liveness** — "is this pod broken?" Failing **restarts
> it**.
>
> Getting them the wrong way round gives you a pod that is restarted every
> time it is briefly slow, which turns a latency spike into an outage. This is
> the standard Kubernetes exam question.
>
> **`resources.requests` is what the scheduler reserves; `limits` is where it
> is killed.** A container with no memory limit can take down its node.

---

## What goes in the lab record

| Item | Value |
|---|---|
| Image name, tag, and **size** | |
| Build time: cold, and after a one-line code change | |
| `docker ps` output | |
| The `/health` and `/predict` responses through the container | |
| What happened when you bound to `127.0.0.1` | |
| Image size with `slim` against the full base | |
| Same endpoint responses from `12_serve_drift_govern.py`, for comparison | |

One paragraph: **explain the requirements-before-code ordering in terms of
layer caching, and give the build-time difference you measured.**
