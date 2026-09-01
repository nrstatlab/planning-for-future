# Experiment 5 -- launch an instance and configure block storage (EBS)

## *** NOT EXECUTED ***

**This repository has no cloud account, and none will be created.** Creating
one requires a payment card and accepts a billing relationship, which is not
something a study repository should do on anyone's behalf.

So this file is what you type, with the traps marked. **It has never been
run here**, and nothing in the notes claims an output for it.

The runnable half is **`04_storage.py`, which compares block, file and object semantics and cost**.

---

## Launch, attach, format, mount

```bash
aws ec2 run-instances --image-id ami-xxxx --instance-type t3.micro \
  --key-name mykey --security-group-ids sg-xxxx --subnet-id subnet-xxxx

aws ec2 create-volume --size 20 --volume-type gp3 \
  --availability-zone us-east-1a
aws ec2 attach-volume --volume-id vol-xxxx --instance-id i-xxxx \
  --device /dev/sdf
```

Then, on the instance:

```bash
lsblk                                   # find it -- it appears as /dev/nvme1n1
sudo file -s /dev/nvme1n1               # "data" means NO FILESYSTEM yet
sudo mkfs -t xfs /dev/nvme1n1           # DESTROYS anything on it
sudo mkdir /data && sudo mount /dev/nvme1n1 /data
sudo blkid                              # get the UUID
echo 'UUID=<uuid> /data xfs defaults,nofail 0 2' | sudo tee -a /etc/fstab
```

## The three that go wrong

**1. `mkfs` on the wrong device.** `lsblk` first, every time. Formatting the
root volume ends the instance.

**2. Forgetting `/etc/fstab`.** The volume is not mounted after a reboot and
your application starts writing to the root disk instead — silently, until it
fills.

**3. `nofail` omitted.** If the volume is missing at boot, the instance hangs
in the boot sequence and you cannot SSH in to fix it. `nofail` turns a
catastrophe into a missing directory.

## An EBS volume is in ONE availability zone

You cannot attach `us-east-1a`'s volume to an instance in `us-east-1b`. To
move it: snapshot it (snapshots go to S3, which is regional), then create a
volume from the snapshot in the other AZ.

**That constraint is why "an EBS volume attaches to one instance" is really
"one instance, in one AZ"** — and it is why EFS exists.

## Volume types, and how to choose

| Type | For | Notes |
|---|---|---|
| **gp3** | almost everything | IOPS and throughput are **independent of size** |
| gp2 | legacy | IOPS scale with size — the reason gp3 replaced it |
| io2 Block Express | a demanding database | expensive, and supports Multi-Attach |
| st1 | big sequential reads | HDD; terrible at random I/O |
| sc1 | cold archive on a disk | cheapest, slowest |

**gp3 is the default answer.** Under gp2 you would over-provision a volume
purely to buy IOPS; gp3 unbundled them.

## Snapshots

```bash
aws ec2 create-snapshot --volume-id vol-xxxx --description "before upgrade"
```

Snapshots are **incremental** — only changed blocks — and stored in S3.
Deleting an intermediate snapshot does not break later ones; AWS re-parents
the blocks. But snapshots of a **mounted, busy filesystem** may be
crash-consistent rather than clean: freeze or unmount for a database.
