# Experiment 14 -- use cloud AutoML services for a dataset prediction task

## *** NOT EXECUTED ***

**This repository has no cloud account, and none will be created.** Creating
one requires a payment card and accepts a billing relationship, which is not
something a study repository should do on anyone's behalf.

So this file is what you type, with the traps marked. **It has never been
run here**, and nothing in the notes claims an output for it.

The runnable half is **`11_train_and_automl.py`, which runs a real 5-model, 5-fold search and reports the leaderboard**.

---

## SageMaker Autopilot

```python
from sagemaker.automl.automl import AutoML

automl = AutoML(
    role=role,
    target_attribute_name="churned",
    output_path=f"s3://{bucket}/autopilot/",
    problem_type="BinaryClassification",
    job_objective={"MetricName": "AUC"},
    max_candidates=20,
    max_runtime_per_training_job_in_seconds=600,
)
automl.fit(inputs=f"s3://{bucket}/train/train.csv")
automl.describe_auto_ml_job()["BestCandidate"]
```

**`max_candidates` and `max_runtime_per_training_job_in_seconds` are the
budget**, and they are not optional. Without them the job explores until it
is satisfied, and it bills the whole time.

## Vertex AI AutoML

```bash
gcloud ai custom-jobs create --region=us-central1 ...
# or, tabular:
gcloud beta ai models list --region=us-central1
```

Vertex bills AutoML in **node-hours** with a documented minimum. Read the
minimum before starting — a small dataset does not produce a small bill.

## Azure Automated ML

```python
from azure.ai.ml import automl
job = automl.classification(
    training_data=train, target_column_name="churned",
    primary_metric="AUC_weighted",
    experiment_timeout_minutes=30,          # THE BUDGET
    enable_early_termination=True,
)
```

## What these actually do

**They fit many models, cross-validate each, and rank them.** The runnable
half does exactly this with five candidates and 5-fold CV, and prints the
leaderboard. There is no intelligence in it — it is a **search**, and its
value is that it is exhaustive where a human would be lazy.

**And read the top of that leaderboard carefully.** In the run here the top
two models differ by 0.0047 AUC with standard deviations of 0.0210 and
0.0196. **The difference is inside the noise**, and "AutoML picked X" is not
a reason to prefer X.

## What AutoML does not do

- decide what the target variable should be
- notice that your target **leaks** the answer
- tell you the base rate matters more than the algorithm
- know that last year's data no longer describes this year
- choose a threshold that fits the business cost of an error
- explain a prediction to a regulator
- notice the model is unfair to a protected group

**Every one of those is the actual job.** AutoML automates the afternoon and
leaves the weeks untouched.

## The explainability report

Autopilot generates a candidate-definition notebook and a data-exploration
notebook. **Read them** — they are the best thing about the product, because
they show you the feature engineering it chose, which is the part you would
otherwise never see and could not defend.
