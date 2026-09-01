# Experiment 13 -- use CloudWatch/Stackdriver to monitor endpoints, set alarms and auto-scale

## *** NOT EXECUTED ***

**This repository has no cloud account, and none will be created.** Creating
one requires a payment card and accepts a billing relationship, which is not
something a study repository should do on anyone's behalf.

So this file is what you type, with the traps marked. **It has never been
run here**, and nothing in the notes claims an output for it.

The runnable half is **`13_monitoring_autoscale.py`, which runs the control loop and measures what tuning costs**.

---

## An alarm

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name endpoint-p99-latency \
  --namespace AWS/SageMaker \
  --metric-name ModelLatency \
  --dimensions Name=EndpointName,Value=churn-endpoint \
                Name=VariantName,Value=AllTraffic \
  --extended-statistic p99 \
  --period 60 --evaluation-periods 3 \
  --threshold 500000 --comparison-operator GreaterThanThreshold \
  --treat-missing-data notBreaching \
  --alarm-actions arn:aws:sns:us-east-1:<acct>:oncall
```

**`--extended-statistic p99`, not `--statistic Average`.** The runnable half
shows twenty latencies where one request took 900 ms: the mean is 85 ms and
would never fire an alarm, while p99 is 737 ms.

**`ModelLatency` is in MICROSECONDS.** 500000 is half a second. Getting the
unit wrong is how an alarm is set 1,000x too high and never fires.

**`--treat-missing-data`** decides what "no data" means. `notBreaching` is
right for a bursty endpoint; `breaching` is right when silence itself is the
failure.

## The billing alarm, which comes first

```bash
aws cloudwatch put-metric-alarm --alarm-name monthly-spend \
  --namespace AWS/Billing --metric-name EstimatedCharges \
  --dimensions Name=Currency,Value=USD \
  --statistic Maximum --period 21600 --evaluation-periods 1 \
  --threshold 50 --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:<acct>:oncall
```

**Billing metrics exist only in `us-east-1`** regardless of where you work,
and they lag by about six hours. Set this before anything else in the course.

## Auto-scaling a SageMaker endpoint

```bash
aws application-autoscaling register-scalable-target \
  --service-namespace sagemaker \
  --resource-id endpoint/churn-endpoint/variant/AllTraffic \
  --scalable-dimension sagemaker:variant:DesiredInstanceCount \
  --min-capacity 1 --max-capacity 8

aws application-autoscaling put-scaling-policy \
  --policy-name track-invocations --policy-type TargetTrackingScaling \
  --service-namespace sagemaker \
  --resource-id endpoint/churn-endpoint/variant/AllTraffic \
  --scalable-dimension sagemaker:variant:DesiredInstanceCount \
  --target-tracking-scaling-policy-configuration '{
     "TargetValue": 750.0,
     "PredefinedMetricSpecification":
        {"PredefinedMetricType": "SageMakerVariantInvocationsPerInstance"},
     "ScaleInCooldown": 300, "ScaleOutCooldown": 60}'
```

**`ScaleOutCooldown` short and `ScaleInCooldown` long.** Scale out eagerly
because being under capacity drops requests; scale in reluctantly because
scaling back out costs boot time. The runnable half measures what happens
when you get that backwards.

## What the runnable half shows, and it is not flattering

- **Autoscaling dropped 1,014 requests where fixed capacity dropped none**,
  because the group is always sized for the previous observation.
- **The most aggressive configuration cost MORE than fixed capacity** —
  188 instance-hours against 168 — by overshooting.

**"Autoscaling saves money" is a claim about a tuned autoscaler.** Say that,
and give the numbers.

## The six metrics worth alarming on

| Metric | Alarm when | The trap |
|---|---|---|
| `ModelLatency` p99 | > 500 ms for 3 min | the mean hides it |
| `Invocation5XXErrors` | > 0 for 1 min | these are **yours** |
| `Invocation4XXErrors` | > 1% of requests | a rate, never a count |
| `CPUUtilization` | > 70% for 5 min | I/O-bound apps never reach it |
| `EstimatedCharges` | > your budget | lags ~6 h, `us-east-1` only |
| **`Invocations` == 0** | for 1 hour | **a dead endpoint still bills** |

**The last row is the one people miss.** An endpoint serving nothing looks
perfect on every performance metric and costs exactly the same as a busy one.
