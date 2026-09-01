# Experiment 8 -- connect to cloud-hosted database services (RDS, BigQuery, Cosmos DB)

## *** NOT EXECUTED ***

**This repository has no cloud account, and none will be created.** Creating
one requires a payment card and accepts a billing relationship, which is not
something a study repository should do on anyone's behalf.

So this file is what you type, with the traps marked. **It has never been
run here**, and nothing in the notes claims an output for it.

The runnable half is **`09_etl_warehouse.py`, which runs the same extract and the same warehouse queries locally**.

---

## RDS (managed PostgreSQL/MySQL)

```bash
aws rds create-db-instance \
  --db-instance-identifier retail-db --db-instance-class db.t3.micro \
  --engine postgres --allocated-storage 20 \
  --master-username admin --manage-master-user-password \
  --no-publicly-accessible --backup-retention-period 7
```

```bash
psql -h retail-db.xxxx.us-east-1.rds.amazonaws.com -U admin -d postgres
```

**`--no-publicly-accessible` is the right default.** Reach it from an EC2
instance in the same VPC, or through a bastion, or with SSM Session Manager.
A publicly reachable database with a weak password is found by scanners in
hours.

**And the security group needs an inbound rule for port 5432 from your
instance's security group** — group-to-group, not a CIDR. That is the fix for
almost every "connection timed out".

## BigQuery

```bash
bq mk --dataset retail
bq load --autodetect --source_format=CSV retail.sales gs://bucket/sales.csv

bq query --use_legacy_sql=false --dry_run \
  'SELECT region, SUM(revenue) FROM retail.sales GROUP BY region'
```

**`--dry_run` prints the bytes the query would scan without running it, and
therefore what it would cost.** Run it before every large query. It is the
single most valuable BigQuery habit.

```bash
bq query --use_legacy_sql=false --maximum_bytes_billed=1000000000 '...'
```

**`--maximum_bytes_billed` is a seatbelt**: the query fails rather than
billing more than you said. Set it in every automated job.

## Cosmos DB

```bash
az cosmosdb create --name retail-cosmos --resource-group rg \
  --kind GlobalDocumentDB --default-consistency-level Session
az cosmosdb sql database create --account-name retail-cosmos \
  --resource-group rg --name retail
```

**The consistency level is the interesting choice**, and it is Course 10's
CAP discussion made into a dropdown:

| Level | Guarantee | Cost |
|---|---|---|
| Strong | linearizable | highest RU, single region write |
| **Bounded staleness** | lag bounded by time or versions | high |
| **Session** | your own writes are read back | **the default, and usually right** |
| Consistent prefix | order preserved, some lag | low |
| Eventual | none | **lowest RU** |

**Cosmos bills in Request Units**, and stronger consistency costs more RUs
per read. That is CAP with a price tag attached.

## Managed against self-hosted

| | Self-hosted on EC2 | Managed (RDS) |
|---|---|---|
| Patching | you | automatic, in a window |
| Backups | you write them | continuous, point-in-time |
| Failover | you build it | Multi-AZ, ~60 s |
| Version upgrade | your weekend | a click, with a restart |
| Root/superuser | yes | **no** |
| Cost | instance only | instance + ~20-30% |

**"No superuser" is the row that surprises people.** Some extensions, some
`ALTER SYSTEM` settings and any filesystem access are unavailable. If your
application needs those, managed is not an option — and knowing that before
you migrate is the point.
