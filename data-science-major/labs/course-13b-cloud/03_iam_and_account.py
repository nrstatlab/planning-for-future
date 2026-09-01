"""Experiments 3 and 10 -- cloud account setup, and IAM roles for SageMaker.

There is no cloud account for this repository and none will be created, so
`03_account_setup.md` and `10_sagemaker_notebook.md` carry the console
click-paths, marked NOT EXECUTED.

What runs here is the part that is actually examinable: AWS's policy
evaluation algorithm, implemented in iam.py and exercised against a realistic
policy set. The three rules are the whole subject.
"""
import fixtures as f
from iam import evaluate


def show(policies, cases, title):
    print(f"\n    {title}")
    print(f"      {'action':<32}{'resource':<47}{'result':<7}why")
    for action, resource in cases:
        trace = {}
        decision = evaluate(policies, action, resource, trace)
        print(f"      {action:<32}{resource:<47}"
              f"{decision:<7}{trace['reason']}")
    return {(a, r): evaluate(policies, a, r) for a, r in cases}


def main():
    print("  Experiments 3 and 10 -- accounts, roles and IAM evaluation")

    print("""
    the three rules, in order:
      1. an EXPLICIT DENY anywhere wins -- always, unconditionally
      2. otherwise an ALLOW that matches grants access
      3. otherwise DENY -- the IMPLICIT DENY""")

    cases = [
        ("s3:GetObject",    "arn:aws:s3:::retail-lake/raw/sales.csv"),
        ("s3:PutObject",    "arn:aws:s3:::retail-lake/raw/sales.csv"),
        ("s3:PutObject",    "arn:aws:s3:::retail-lake/models/model.pkl"),
        ("s3:DeleteObject", "arn:aws:s3:::retail-lake/raw/sales.csv"),
        ("s3:GetObject",    "arn:aws:s3:::other-bucket/secret.csv"),
        ("sagemaker:CreateTrainingJob", "arn:aws:sagemaker:*:*:training-job/x"),
    ]
    got = show(f.POLICIES, cases, "the attached policies, evaluated:")

    assert got[("s3:GetObject", "arn:aws:s3:::retail-lake/raw/sales.csv")] == "Allow"
    assert got[("s3:PutObject", "arn:aws:s3:::retail-lake/raw/sales.csv")] == "Deny"
    assert got[("s3:PutObject", "arn:aws:s3:::retail-lake/models/model.pkl")] == "Allow"
    assert got[("s3:GetObject", "arn:aws:s3:::other-bucket/secret.csv")] == "Deny"

    print("""         READ ROWS 2 AND 3 TOGETHER. The same action on the same
         bucket is denied under raw/ and allowed under models/, because
         a Deny statement scoped to one prefix beats an Allow scoped to
         the bucket. Prefix-scoped policies are how a data lake keeps a
         raw zone immutable while the rest stays writable""")

    # ---- the demonstration that surprises people ------------------------
    print("\n    now ADD a policy granting s3:* on everything:")
    admin = {"name": "S3FullAccess",
             "statements": [{"Effect": "Allow", "Action": ["s3:*"],
                             "Resource": ["*"]}]}
    with_admin = f.POLICIES + [admin]
    trace = {}
    still = evaluate(with_admin, "s3:PutObject",
                     "arn:aws:s3:::retail-lake/raw/sales.csv", trace)
    print(f"      s3:PutObject on raw/  -> {still}   ({trace['reason']})")
    assert still == "Deny"
    print("""         STILL DENIED, with full S3 admin attached. An explicit
         Deny cannot be out-voted, out-numbered or out-scoped -- there
         is no 'more specific allow wins' rule. To lift it you must
         REMOVE the Deny.
         This is the single most common IAM misunderstanding, and it is
         also the feature: a Deny is how an organisation guarantees
         something, rather than hoping nobody granted otherwise""")

    # ---- ordering does not matter ---------------------------------------
    reversed_order = list(reversed(with_admin))
    assert evaluate(reversed_order, "s3:PutObject",
                    "arn:aws:s3:::retail-lake/raw/sales.csv") == "Deny"
    print("\n    policy ORDER does not matter -- reversed, the answer is the same")
    print("""         unlike a firewall rule list, IAM is not first-match.
         Every statement is evaluated, then the three rules decide.
         Say that and you have answered 'how does IAM resolve
         conflicting policies?'""")

    # ---- roles against users --------------------------------------------
    print("\n    a ROLE is not a user:")
    print(f"      {'':<16}{'user':<30}{'role'}")
    for label, u, r in (
            ("credentials", "long-lived access key", "TEMPORARY, auto-rotated"),
            ("who assumes it", "a person", "a SERVICE or another principal"),
            ("in a notebook", "keys in a file  <- BAD", "attached; no keys exist"),
            ("if leaked", "valid until revoked", "expires in minutes to hours")):
        print(f"      {label:<16}{u:<30}{r}")
    print("""         a SageMaker notebook gets an EXECUTION ROLE, so no access
         key is ever written to disk. That is why experiment 10 says
         'attach IAM role' rather than 'paste your credentials', and
         'I put my keys in the notebook' is the answer that loses the
         marks""")

    # ---- least privilege, made concrete ---------------------------------
    print("\n    least privilege, as an exercise:")
    over = {"name": "ItWorksNow",
            "statements": [{"Effect": "Allow", "Action": ["*"],
                            "Resource": ["*"]}]}
    tight = {"name": "TrainingJobOnly",
             "statements": [
                 {"Effect": "Allow",
                  "Action": ["s3:GetObject"],
                  "Resource": ["arn:aws:s3:::retail-lake/train/*"]},
                 {"Effect": "Allow",
                  "Action": ["s3:PutObject"],
                  "Resource": ["arn:aws:s3:::retail-lake/models/*"]},
             ]}
    probe = [("s3:GetObject", "arn:aws:s3:::retail-lake/train/x.csv"),
             ("s3:PutObject", "arn:aws:s3:::retail-lake/models/m.tar.gz"),
             ("iam:CreateUser", "*"),
             ("ec2:TerminateInstances", "*")]
    print(f"      {'action':<26}{'*:* policy':<14}{'scoped policy'}")
    for a, r in probe:
        print(f"      {a:<26}{evaluate([over], a, r):<14}"
              f"{evaluate([tight], a, r)}")
    assert evaluate([over], "iam:CreateUser", "*") == "Allow"
    assert evaluate([tight], "iam:CreateUser", "*") == "Deny"
    print("""         both policies let the training job run. One of them also
         lets it create IAM users and terminate every instance in the
         account. '*:* made it work' is not a solution, it is a
         postponed incident""")

    # ---- the free tier, and what actually costs money -------------------
    print("\n    the free tier, and the three things that bill anyway:")
    print(f"      {'service':<22}{'free tier':<34}{'what still costs'}")
    for svc, free, cost in (
            ("EC2", "750 hrs/month t2/t3.micro, 12 mo", "any larger instance"),
            ("S3", "5 GB Standard, 12 mo", "EGRESS to the internet"),
            ("RDS", "750 hrs/month db.t3.micro, 12 mo", "storage over 20 GB"),
            ("Lambda", "1M requests/month, ALWAYS free", "duration x memory"),
            ("SageMaker", "250 hrs notebook, 2 mo", "ENDPOINTS, billed hourly")):
        print(f"      {svc:<22}{free:<34}{cost}")
    endpoint_month = f.EC2["m5.large"] * f.HOURS_PER_MONTH
    print(f"\n      a forgotten ml.m5.large endpoint costs about "
          f"${endpoint_month:,.0f}/month")
    assert 60 < endpoint_month < 90
    print("""         THE ENDPOINT IS THE TRAP. A training job ends and stops
         billing; an endpoint runs until you delete it, at hourly
         rates, whether or not anything calls it. Every 'I got a
         surprise AWS bill' story is a resource nobody switched off --
         set a BUDGET ALARM on day one, before anything else""")


if __name__ == "__main__":
    main()
