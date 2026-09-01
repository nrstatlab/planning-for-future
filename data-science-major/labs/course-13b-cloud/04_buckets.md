# Experiment 4 -- create and manage storage buckets; upload and access datasets

## *** NOT EXECUTED ***

**This repository has no cloud account, and none will be created.** Creating
one requires a payment card and accepts a billing relationship, which is not
something a study repository should do on anyone's behalf.

So this file is what you type, with the traps marked. **It has never been
run here**, and nothing in the notes claims an output for it.

The runnable half is **`04_storage.py`, which implements the key semantics and runs the pricing arithmetic**.

---

## The CLI, which is faster than the console

```bash
aws s3 mb s3://retail-lake-<your-unique-suffix>     # names are GLOBAL
aws s3 cp sales.csv s3://retail-lake/raw/2026/01/
aws s3 cp ./data s3://retail-lake/raw/ --recursive
aws s3 ls s3://retail-lake/raw/                    # by PREFIX
aws s3 ls s3://retail-lake/raw/ --recursive --human-readable --summarize
aws s3 sync ./local s3://retail-lake/curated/      # only what changed
aws s3 mv s3://retail-lake/a.csv s3://retail-lake/b.csv   # COPY + DELETE
aws s3 rm s3://retail-lake/raw/old.csv
aws s3 presign s3://retail-lake/raw/sales.csv --expires-in 3600
```

**`s3 mv` is not a rename.** There is no rename. It copies the whole object
and deletes the original, and you are billed for both.

## Bucket names are globally unique

Across every AWS customer on earth. `s3://data` was taken in 2006. Use
`<org>-<purpose>-<region>-<random>`.

## Versioning and lifecycle

```bash
aws s3api put-bucket-versioning --bucket retail-lake \
    --versioning-configuration Status=Enabled
```

**Then set a lifecycle rule immediately**, or you pay for every version of
every object for ever:

```json
{"Rules": [{
  "ID": "tier-and-expire",
  "Filter": {"Prefix": "raw/"},
  "Status": "Enabled",
  "Transitions": [
    {"Days": 30,  "StorageClass": "STANDARD_IA"},
    {"Days": 90,  "StorageClass": "GLACIER"}
  ],
  "NoncurrentVersionExpiration": {"NoncurrentDays": 30},
  "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7}
}]}
```

**That last rule matters more than it looks.** A failed multipart upload
leaves parts that are invisible in `s3 ls` and billed for ever. Many
mysterious S3 bills are abandoned multipart uploads.

## Blocking public access

```bash
aws s3api put-public-access-block --bucket retail-lake \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

**On by default since 2023**, and it should stay on. "Public S3 bucket" was
the single most common cause of data breaches for a decade. To share one
object, use a **presigned URL** — time-limited, no policy change.

## Encryption

Server-side encryption is on by default (SSE-S3). Use **SSE-KMS** when you
need an audit trail of who decrypted what, and accept that KMS charges per
request. `--sse aws:kms --sse-kms-key-id <arn>`.
