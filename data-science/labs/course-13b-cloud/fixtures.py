"""Shared data and shared cost tables for Course 13 B.

No cloud account exists for this repository and none will be created, so the
console click-paths and CLI commands are documented and marked NOT EXECUTED.
What runs here is everything that does not need a provider: the IAM policy
evaluation algorithm, object-store key semantics, the pricing arithmetic, an
autoscaling control loop, a real ETL into a real columnar warehouse, a real
model, and a real HTTP endpoint serving it.

The dataset is Course 11's star schema again, imported not copied, so the
warehouse figures in experiment 12 must agree with Course 11's DAX, Course
12 B's Hive/Spark, and each other.

Every price below is a LIST PRICE from the providers' public pages, us-east-1
/ us-central1, as of early 2026. They change; the ARITHMETIC does not, and
the arithmetic is the examinable part. Each constant names its unit so a
stale number can be replaced without hunting through the code.
"""
import importlib.util
import pathlib

_C11_PATH = (pathlib.Path(__file__).resolve().parents[1]
             / "course-11-bi" / "fixtures.py")
_spec = importlib.util.spec_from_file_location("c11_fixtures", _C11_PATH)
c11 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(c11)

SALES_DF = c11.star()


def total_revenue():
    return float(SALES_DF["revenue"].sum())


# --------------------------------------------------------------- pricing
# All figures USD unless stated.

S3_STORAGE = {                      # $ per GB-month
    "Standard":            0.023,
    "Standard-IA":         0.0125,
    "One Zone-IA":         0.010,
    "Glacier Instant":     0.004,
    "Glacier Flexible":    0.0036,
    "Glacier Deep Archive": 0.00099,
}

S3_RETRIEVAL = {                    # $ per GB retrieved
    "Standard":            0.0,
    "Standard-IA":         0.01,
    "One Zone-IA":         0.01,
    "Glacier Instant":     0.03,
    "Glacier Flexible":    0.01,
    "Glacier Deep Archive": 0.02,
}

S3_MIN_DAYS = {                     # minimum billed storage duration
    "Standard": 0, "Standard-IA": 30, "One Zone-IA": 30,
    "Glacier Instant": 90, "Glacier Flexible": 90,
    "Glacier Deep Archive": 180,
}

EBS_GP3_GB_MONTH = 0.08             # $ per GB-month
EFS_STANDARD_GB_MONTH = 0.30        # $ per GB-month
EGRESS_PER_GB = 0.09                # $ per GB to the internet, first 10 TB
BIGQUERY_PER_TB_SCANNED = 6.25      # $ per TB scanned, on-demand
REDSHIFT_RA3_XLPLUS_HOUR = 1.086    # $ per node-hour

EC2 = {                             # $ per hour, on-demand, Linux
    "t3.micro":    0.0104,
    "t3.medium":   0.0416,
    "m5.large":    0.096,
    "m5.xlarge":   0.192,
    "c5.4xlarge":  0.68,
    "p3.2xlarge":  3.06,            # 1 x V100 GPU
    "p4d.24xlarge": 32.7726,        # 8 x A100
}

RESERVED_DISCOUNT = 0.40            # 1-year, no upfront, roughly
SPOT_DISCOUNT = 0.70                # typical, and interruptible

HOURS_PER_MONTH = 730               # the standard billing month


# --------------------------------------------------------------- IAM

# A deliberately realistic set: one allow, one scoped allow, one explicit
# deny that overrides everything, and a role with no statement at all.
POLICIES = [
    {
        "name": "DataScientistRead",
        "statements": [
            {"Effect": "Allow",
             "Action": ["s3:GetObject", "s3:ListBucket"],
             "Resource": ["arn:aws:s3:::retail-lake",
                          "arn:aws:s3:::retail-lake/*"]},
        ],
    },
    {
        "name": "SageMakerExecution",
        "statements": [
            {"Effect": "Allow",
             "Action": ["s3:GetObject", "s3:PutObject"],
             "Resource": ["arn:aws:s3:::retail-lake/models/*"]},
            {"Effect": "Allow",
             "Action": ["sagemaker:*"],
             "Resource": ["*"]},
        ],
    },
    {
        "name": "ProtectRawZone",
        "statements": [
            {"Effect": "Deny",
             "Action": ["s3:DeleteObject", "s3:PutObject"],
             "Resource": ["arn:aws:s3:::retail-lake/raw/*"]},
        ],
    },
]


# --------------------------------------------------------------- traffic


def daily_traffic(peak=1000, base=120):
    """A deterministic 24-hour request-rate curve, requests per second.

    Two peaks (mid-morning and evening) and a quiet night, which is what a
    consumer-facing endpoint actually looks like. No randomness, so the
    autoscaling results in experiment 13 reproduce exactly.
    """
    shape = [0.10, 0.07, 0.05, 0.05, 0.06, 0.12,   # 00-05
             0.28, 0.55, 0.80, 1.00, 0.92, 0.78,   # 06-11
             0.70, 0.66, 0.62, 0.65, 0.74, 0.88,   # 12-17
             0.96, 0.90, 0.72, 0.52, 0.32, 0.18]   # 18-23
    return [round(base + (peak - base) * s) for s in shape]
