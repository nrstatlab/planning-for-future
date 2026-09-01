# Experiment 10 -- launch a SageMaker notebook, attach an IAM role and an S3 bucket

## *** NOT EXECUTED ***

**This repository has no cloud account, and none will be created.** Creating
one requires a payment card and accepts a billing relationship, which is not
something a study repository should do on anyone's behalf.

So this file is what you type, with the traps marked. **It has never been
run here**, and nothing in the notes claims an output for it.

The runnable half is **`03_iam_and_account.py`, which implements IAM's evaluation algorithm and proves what the role can do**.

---

## The role first, then the notebook

```bash
aws iam create-role --role-name SageMakerExecutionRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "sagemaker.amazonaws.com"},
      "Action": "sts:AssumeRole"}]}'
```

**That document is the TRUST POLICY, and it is not the permissions.** It says
*who may become this role*; a separate permissions policy says *what the role
may then do*. Confusing the two is the commonest IAM error after the explicit
Deny.

```bash
aws iam put-role-policy --role-name SageMakerExecutionRole \
  --policy-name S3Scoped --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {"Effect": "Allow", "Action": ["s3:GetObject"],
       "Resource": "arn:aws:s3:::retail-lake/train/*"},
      {"Effect": "Allow", "Action": ["s3:PutObject"],
       "Resource": "arn:aws:s3:::retail-lake/models/*"}]}'
```

**Two statements, two prefixes, two actions.** Not `s3:*` on `*`. The
runnable half shows both policies letting the training job succeed, and only
one of them also permitting `iam:CreateUser`.

## Then the notebook

```bash
aws sagemaker create-notebook-instance \
  --notebook-instance-name lab10 \
  --instance-type ml.t3.medium \
  --role-arn arn:aws:iam::<acct>:role/SageMakerExecutionRole \
  --volume-size-in-gb 20
aws sagemaker describe-notebook-instance --notebook-instance-name lab10
aws sagemaker create-presigned-notebook-instance-url \
  --notebook-instance-name lab10
```

Inside the notebook, **no credentials exist anywhere**:

```python
import boto3, sagemaker
session = sagemaker.Session()
role = sagemaker.get_execution_role()      # reads the ATTACHED role
bucket = "retail-lake"
session.upload_data("train.csv", bucket=bucket, key_prefix="train")
```

## ⚠ What not to do

```python
boto3.client("s3", aws_access_key_id="AKIA...", aws_secret_access_key="...")
```

**Keys in a notebook end up in git.** GitHub scans for them and AWS
quarantines the account, which is the good outcome; the bad outcome is a
cryptomining bill. The execution role exists precisely so this is never
necessary.

## Stop it when you are done

```bash
aws sagemaker stop-notebook-instance --notebook-instance-name lab10
aws sagemaker delete-notebook-instance --notebook-instance-name lab10
```

**Stopping keeps the EBS volume (and its charge); deleting removes
everything.** A stopped notebook costs only storage; a running one costs the
instance whether or not the browser tab is open.
