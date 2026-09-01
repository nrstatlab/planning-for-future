# Experiment 3 -- create and configure a cloud account (AWS/Azure/GCP free tier)

## *** NOT EXECUTED ***

**This repository has no cloud account, and none will be created.** Creating
one requires a payment card and accepts a billing relationship, which is not
something a study repository should do on anyone's behalf.

So this file is what you type, with the traps marked. **It has never been
run here**, and nothing in the notes claims an output for it.

The runnable half is **`03_iam_and_account.py`, which implements and exercises IAM's evaluation algorithm**.

---

## Do these six things in this order, before anything else

1. **Enable MFA on the root account.** Then never use the root account again.
2. **Create an IAM user for yourself** with `AdministratorAccess`, and use
   that.
3. **Set a budget alarm.** Billing → Budgets → a monthly cost budget with an
   alert at 50%, 80% and 100%. **Do this on day one**, not after the bill.
4. **Enable Cost Explorer.** It takes 24 hours to populate, so turn it on now.
5. **Pick one region and stay in it.** Resources in another region are
   invisible in the console and still bill.
6. **Install and configure the CLI:**

```bash
aws configure          # access key, secret, default region, output format
aws sts get-caller-identity        # who am I, really
aws configure list-profiles
```

## Root against IAM user

| | Root | IAM user |
|---|---|---|
| Created by | signing up | you |
| Can | **everything, including closing the account** | what its policies allow |
| MFA | **mandatory, immediately** | strongly recommended |
| Daily use | **never** | yes |
| Recovers | account-level problems only | — |

## The free tier, honestly

| Type | Duration | Examples |
|---|---|---|
| **12 months free** | from signup | 750 h/month t3.micro, 5 GB S3, 750 h RDS |
| **Always free** | forever | 1 M Lambda requests/month, 25 GB DynamoDB |
| **Trials** | short, one-off | SageMaker 250 h for 2 months |

**Three things bill you anyway, inside the free tier:**

- **Egress.** Ingress is free; downloading is not.
- **Anything larger than the free size.** A `t3.small` is not a `t3.micro`.
- **Resources you forgot.** An idle NAT Gateway is about $32/month, an
  unattached Elastic IP is about $3.60/month, and a SageMaker endpoint is
  about $70/month.

## The equivalents, when the exam asks

| Concept | AWS | Azure | GCP |
|---|---|---|---|
| Object storage | S3 | Blob Storage | Cloud Storage |
| Block storage | EBS | Managed Disks | Persistent Disk |
| File storage | EFS | Azure Files | Filestore |
| VM | EC2 | Virtual Machines | Compute Engine |
| Managed SQL | RDS | SQL Database | Cloud SQL |
| Warehouse | Redshift | Synapse | **BigQuery** |
| Serverless functions | Lambda | Functions | Cloud Functions |
| Managed ML | SageMaker | Azure ML | Vertex AI |
| Monitoring | CloudWatch | Monitor | Cloud Monitoring |
| Identity | IAM | Entra ID | IAM |

**Learn the row, not the column.** Every provider has all of these, and an
exam answer that names the concept and gives one vendor's term for it is
worth more than a memorised AWS product list.

## Then clean up

```bash
aws ec2 describe-instances --query \
  'Reservations[].Instances[?State.Name==`running`].[InstanceId,InstanceType]'
aws s3 ls
aws sagemaker list-endpoints
```

**Run those three at the end of every lab session.** Nothing else in this
course will save you as much money.
