# Experiment 12 -- a simple ETL job: extract, transform, load into a cloud warehouse

## *** NOT EXECUTED ***

**This repository has no cloud account, and none will be created.** Creating
one requires a payment card and accepts a billing relationship, which is not
something a study repository should do on anyone's behalf.

So this file is what you type, with the traps marked. **It has never been
run here**, and nothing in the notes claims an output for it.

The runnable half is **`09_etl_warehouse.py`, which runs the whole pipeline into a real columnar warehouse**.

---

## AWS Glue (the managed option)

```python
import sys
from awsglue.transforms import *
from awsglue.context import GlueContext
from pyspark.context import SparkContext

glueContext = GlueContext(SparkContext.getOrCreate())

src = glueContext.create_dynamic_frame.from_catalog(
    database="retail", table_name="orders")

mapped = ApplyMapping.apply(frame=src, mappings=[
    ("order_id", "long", "order_id", "long"),
    ("region", "string", "region", "string"),
    ("qty", "long", "qty", "int"),
    ("list_price", "double", "revenue_unit", "double"),
])
clean = DropNullFields.apply(frame=mapped)

glueContext.write_dynamic_frame.from_options(
    frame=clean, connection_type="s3",
    connection_options={"path": "s3://retail-lake/curated/",
                        "partitionKeys": ["quarter"]},
    format="parquet")
```

**`partitionKeys` and `format="parquet"` are the two lines that matter**, and
they are Course 12 B's partition pruning and columnar storage arriving in the
cloud unchanged.

## The crawler, and its trap

```bash
aws glue start-crawler --name retail-crawler
```

A crawler infers the schema and registers the table in the Data Catalog.
**It infers types from a sample**, so a column that is integer in the sample
and text later becomes a runtime failure. For anything that matters, define
the table explicitly.

## Loading Redshift

```sql
COPY sales FROM 's3://retail-lake/curated/'
IAM_ROLE 'arn:aws:iam::<acct>:role/RedshiftCopyRole'
FORMAT AS PARQUET;
```

**`COPY` is the only sensible way to load Redshift.** A loop of `INSERT`
statements is orders of magnitude slower, because a columnar store is built
for bulk loads and each `INSERT` writes a nearly-empty block.

```sql
ANALYZE sales;    -- statistics, or the optimiser guesses
VACUUM sales;     -- reclaim space and re-sort after deletes
```

## Loading BigQuery

```bash
bq load --source_format=PARQUET \
  --time_partitioning_field=order_date \
  --clustering_fields=region,category \
  retail.sales gs://retail-lake/curated/*.parquet
```

**Partition on the column you filter by; cluster on the columns you filter
and group by after that.** Partitioning removes whole days from the scan;
clustering sorts within a partition so the block statistics can skip more.
Both directly reduce **bytes scanned**, which is directly the bill.

## The reconciliation nobody does and everybody should

```sql
SELECT COUNT(*) AS rows, SUM(revenue) AS revenue FROM sales;
```

Compare against the source. **Row count and the sum of a money column** —
the same two checks Course 12 B used on the Sqoop import. Rows alone will not
catch a truncated numeric type.

## Orchestration

| Tool | Shape |
|---|---|
| Step Functions | a state machine, JSON, AWS-native |
| **Airflow (MWAA/Composer)** | a Python DAG — the industry standard |
| Glue Workflows | Glue jobs only |
| EventBridge + Lambda | event-driven, for small steps |

**Retries and idempotency are the whole design problem.** A pipeline that
cannot be re-run safely will eventually be re-run anyway, at 3 a.m., by
someone who does not know what it does.
