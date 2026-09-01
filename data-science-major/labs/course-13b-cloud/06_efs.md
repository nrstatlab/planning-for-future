# Experiment 6 -- create and configure file storage on a cloud VM (EFS)

## *** NOT EXECUTED ***

**This repository has no cloud account, and none will be created.** Creating
one requires a payment card and accepts a billing relationship, which is not
something a study repository should do on anyone's behalf.

So this file is what you type, with the traps marked. **It has never been
run here**, and nothing in the notes claims an output for it.

The runnable half is **`04_storage.py`, which prices EFS against EBS and S3 on the same terabyte**.

---

## Create and mount

```bash
aws efs create-file-system --performance-mode generalPurpose \
    --throughput-mode elastic --tags Key=Name,Value=shared-data
aws efs create-mount-target --file-system-id fs-xxxx \
    --subnet-id subnet-xxxx --security-groups sg-xxxx
```

On each instance:

```bash
sudo apt install -y amazon-efs-utils
sudo mkdir /shared
sudo mount -t efs -o tls fs-xxxx:/ /shared
echo 'fs-xxxx:/ /shared efs _netdev,tls 0 0' | sudo tee -a /etc/fstab
```

**`_netdev` is not optional.** It tells systemd to wait for the network
before mounting. Without it the mount fails at boot, every time.

## The security group rule everyone forgets

The EFS mount target needs an inbound rule allowing **NFS (TCP 2049)** from
the instances' security group. Without it the mount hangs — it does not fail
with a useful message, it hangs — and this is the single most common EFS
problem.

## What EFS is actually for

Mount it on **many instances at once**, and they all see the same files with
POSIX semantics — locking, permissions, in-place writes. That is the whole
feature, and nothing else in the storage lineup offers it.

| Use it for | Do not use it for |
|---|---|
| a shared home directory across a fleet | a dataset one batch job reads once |
| shared model artefacts several workers read | a database's data files |
| a lift-and-shift app that expects a filesystem | anything a pipeline can read from S3 |

## Cost, which is the reason to think twice

EFS Standard is about **$0.30/GB-month** — roughly 13x S3 Standard and
nearly 4x EBS gp3. Use **EFS Infrequent Access** with a lifecycle policy
(`--lifecycle-policy TransitionToIA=AFTER_30_DAYS`) and the cold portion
drops by about 90%.

**"We put the training data on EFS because it was easy to mount" is how a
storage bill triples.** That data belongs in S3.

## Azure and GCP

| | AWS | Azure | GCP |
|---|---|---|---|
| Managed NFS | EFS | Azure Files (NFS/SMB) | Filestore |
| Protocol | NFSv4.1 | SMB **and** NFS | NFSv3 |

**Azure Files speaks SMB**, which matters if your workload is Windows —
that is the one real difference between the three.
