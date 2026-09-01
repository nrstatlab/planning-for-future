# Experiment 15 -- deploy a trained ML model as a REST API endpoint

## *** NOT EXECUTED ***

**This repository has no cloud account, and none will be created.** Creating
one requires a payment card and accepts a billing relationship, which is not
something a study repository should do on anyone's behalf.

So this file is what you type, with the traps marked. **It has never been
run here**, and nothing in the notes claims an output for it.

The runnable half is **`15_deploy_endpoint.py`, which starts a REAL HTTP server, serves a REAL model and calls it**.

---

## Deploy

```python
predictor = estimator.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large",
    endpoint_name="churn-endpoint",
)
predictor.predict([[1.2, 0.4, ...]])
```

Or from the CLI, in the three steps the SDK hides:

```bash
aws sagemaker create-model --model-name churn-model \
  --primary-container Image=<ecr-uri>,ModelDataUrl=s3://bucket/models/model.tar.gz \
  --execution-role-arn arn:aws:iam::<acct>:role/SageMakerExecutionRole

aws sagemaker create-endpoint-config --endpoint-config-name churn-config \
  --production-variants VariantName=AllTraffic,ModelName=churn-model,\
InitialInstanceCount=1,InstanceType=ml.m5.large,InitialVariantWeight=1

aws sagemaker create-endpoint --endpoint-name churn-endpoint \
  --endpoint-config-name churn-config
```

**Model, endpoint config, endpoint — three objects, not one.** That is what
makes blue/green possible: create a second config and update the endpoint,
and traffic shifts without downtime.

## Invoke it

```bash
aws sagemaker-runtime invoke-endpoint \
  --endpoint-name churn-endpoint \
  --content-type application/json \
  --body '{"instances": [[1.2, 0.4, 3.3, ...]]}' \
  /dev/stdout
```

**The request is IAM-signed.** There is no API key to leak, and access is
governed by the same policy evaluation as everything else.

## The container contract

Your container must answer two routes:

| Route | Must |
|---|---|
| `GET /ping` | return 200 quickly, **without running the model** |
| `POST /invocations` | run inference |

**A health check that does real inference marks the container unhealthy
whenever the model is merely slow — and the platform then kills a container
that was working.** The runnable half implements both routes and says so.

## Real-time, serverless or batch

| | Real-time | Serverless | Batch transform |
|---|---|---|---|
| Latency | ms | ms, **after a cold start** | minutes to hours |
| Billed | **per hour, always** | per request | per job |
| Idle cost | **the full instance** | **zero** | zero |
| Good for | steady traffic | spiky or occasional | scoring a whole file |

**An `ml.m5.large` endpoint is about $70/month whether or not anything calls
it.** If traffic is occasional, serverless inference costs a fraction; if you
are scoring a file, batch transform is the right tool and an endpoint is the
expensive way to do arithmetic — the runnable half measures a **37x**
difference between one batched request and 100 single ones.

## Then delete it

```bash
aws sagemaker delete-endpoint --endpoint-name churn-endpoint
aws sagemaker delete-endpoint-config --endpoint-config-name churn-config
aws sagemaker delete-model --model-name churn-model
```

**Deleting the endpoint is a step in the experiment, not an afterthought.**
Every "surprise AWS bill" story is a resource nobody switched off.

## Monitoring the deployed model

Data drift is the failure that has no error message: the endpoint keeps
returning 200 and the predictions quietly stop being right.

```python
from sagemaker.model_monitor import DefaultModelMonitor
monitor = DefaultModelMonitor(role=role, instance_type="ml.m5.xlarge")
monitor.suggest_baseline(baseline_dataset=f"s3://{bucket}/train/train.csv")
monitor.create_monitoring_schedule(endpoint_input=predictor.endpoint_name,
                                   schedule_cron_expression="cron(0 * ? * * *)")
```

**Baseline the training distribution, then compare production inputs against
it hourly.** A drift alarm is the only thing that catches a model that has
stopped working while every infrastructure metric stays green.
