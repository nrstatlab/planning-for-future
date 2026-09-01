# Experiment 11 -- build a classification/regression model on a managed ML platform

## *** NOT EXECUTED ***

**This repository has no cloud account, and none will be created.** Creating
one requires a payment card and accepts a billing relationship, which is not
something a study repository should do on anyone's behalf.

So this file is what you type, with the traps marked. **It has never been
run here**, and nothing in the notes claims an output for it.

The runnable half is **`11_train_and_automl.py`, which trains the same model and prices the instance choice**.

---

## The SDK call

```python
from sagemaker.sklearn.estimator import SKLearn

estimator = SKLearn(
    entry_point="train.py",
    role=role,
    instance_type="ml.m5.xlarge",
    instance_count=1,
    framework_version="1.2-1",
    hyperparameters={"n_estimators": 100, "max_depth": 5},
    output_path=f"s3://{bucket}/models/",
)
estimator.fit({"train": f"s3://{bucket}/train/",
               "validation": f"s3://{bucket}/validation/"})
```

## The three things that make it a MANAGED job

1. **`entry_point="train.py"`** — your ordinary scikit-learn script, run
   inside a container SageMaker builds. The algorithm is unchanged.
2. **`instance_type`** — billed per second, spun up for the job and destroyed
   after. This is the actual product.
3. **`output_path`** — the artefact lands in S3. Training and serving are
   separate systems joined by one file.

## The `train.py` contract

```python
import argparse, os, joblib, pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

parser = argparse.ArgumentParser()
parser.add_argument("--n_estimators", type=int, default=100)
parser.add_argument("--train", default=os.environ["SM_CHANNEL_TRAIN"])
parser.add_argument("--model-dir", default=os.environ["SM_MODEL_DIR"])
args = parser.parse_args()

df = pd.read_csv(os.path.join(args.train, "train.csv"))
X, y = df.drop(columns=["target"]), df["target"]
model = GradientBoostingClassifier(n_estimators=args.n_estimators).fit(X, y)
joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))
```

**Hyperparameters arrive as command-line arguments; channels arrive as
environment variables; the model must be written to `SM_MODEL_DIR`.** Those
three conventions are the entire interface, and getting `SM_MODEL_DIR` wrong
is why a job "succeeds" and produces no artefact.

## Spot training

```python
estimator = SKLearn(..., use_spot_instances=True,
                    max_run=3600, max_wait=7200,
                    checkpoint_s3_uri=f"s3://{bucket}/checkpoints/")
```

**Up to 70% cheaper, and interruptible.** `max_wait` must exceed `max_run` to
leave room for interruptions, and without `checkpoint_s3_uri` an interrupted
job restarts from zero. For a 20-minute job spot is free money; for a 20-hour
job without checkpoints it is a trap.

## Instance choice, which is answered by the algorithm

| Algorithm | Instance | Why |
|---|---|---|
| scikit-learn, XGBoost on tabular | **m5 / c5** | no GPU code path exists |
| Deep learning, training | p3 / p4d / g5 | dense matrix multiplication |
| Deep learning, inference | g4dn / inf1 | cheaper per prediction |
| Anything, if the data fits in RAM | the smallest that fits | you are paying for RAM |

**Gradient boosting on tabular data does not use a GPU.** A `p4d.24xlarge`
would run this model at the same speed for roughly 170 times the price — a
figure the runnable half computes.
