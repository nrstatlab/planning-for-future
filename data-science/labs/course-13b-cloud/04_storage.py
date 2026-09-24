"""Experiments 4, 5 and 6 -- object, block and file storage on the cloud.

The console click-paths for S3, EBS and EFS are in `04_buckets.md`,
`05_ebs.md` and `06_efs.md`, all marked NOT EXECUTED -- there is no cloud
account.

What runs here is the SEMANTICS, which is what the exam is about: why an
object store has no directories, why you cannot rename, why a block volume
attaches to exactly one instance, and the pricing arithmetic that decides
which one you should have chosen.
"""
import fixtures as f
from objectstore import ObjectStore


def money(x):
    return f"${x:,.2f}"


def main():
    print("  Experiments 4, 5 and 6 -- object, block and file storage")

    # ================================================== experiment 4
    print("\n    --- experiment 4: buckets and objects")
    s3 = ObjectStore("retail-lake")
    keys = [
        "raw/2026/01/sales.csv",
        "raw/2026/02/sales.csv",
        "raw/2026/03/sales.csv",
        "curated/2026/sales.parquet",
        "models/churn/model.tar.gz",
        "README.md",
    ]
    for k in keys:
        s3.put(k, b"x" * 1024)
    print(f"      {len(s3.objects)} objects, {s3.total_bytes():,} bytes")

    print("\n      LIST with prefix 'raw/' and delimiter '/':")
    plain, prefixes = s3.list("raw/", delimiter="/")
    print(f"        objects at this level : {plain or '(none)'}")
    print(f"        common prefixes       : {prefixes}")
    assert plain == [] and prefixes == ["raw/2026/"]
    print("""         THERE IS NO DIRECTORY ANYWHERE. 'raw/2026/01/sales.csv' is
         ONE KEY containing three slashes, and the console's folder
         tree is drawn from COMMON PREFIXES computed at list time.
         Delete every object under a 'folder' and the folder is gone,
         because it never existed""")

    print("\n      LIST with prefix 'raw/' and NO delimiter:")
    plain, prefixes = s3.list("raw/")
    for k in plain:
        print(f"        {k}")
    assert len(plain) == 3 and prefixes == []
    print("""         without a delimiter you get every key under the prefix,
         flat. That is the only query an object store supports: a
         PREFIX SCAN. No WHERE, no index, no search by content""")

    # ---- rename ---------------------------------------------------------
    cost = s3.rename("README.md", "docs/README.md")
    print(f"\n      'rename' README.md -> docs/README.md")
    print(f"        bytes read {cost['bytes_read']:,}, "
          f"bytes written {cost['bytes_written']:,}, "
          f"API calls {cost['requests']}")
    assert "README.md" not in s3.objects and "docs/README.md" in s3.objects
    print("""         THERE IS NO RENAME. It is a COPY plus a DELETE, so it
         reads and writes the whole object. Renaming a 5 TB dataset
         'to tidy up the folders' moves 10 TB and is billed for it --
         and on a filesystem it would have been a metadata edit""")

    # ---- versioning -----------------------------------------------------
    print("\n      versioning ON, then overwrite and delete:")
    s3.versioning = True
    s3.put("curated/2026/sales.parquet", b"y" * 2048)
    s3.delete("curated/2026/sales.parquet")
    hist = s3.versions["curated/2026/sales.parquet"]
    current = s3.objects["curated/2026/sales.parquet"]
    print(f"        older versions kept : {len(hist)}")
    print(f"        current object      : {current['class']}")
    assert len(hist) == 2 and current["class"] == "DeleteMarker"
    print("""         a DELETE with versioning on writes a DELETE MARKER; the
         data is still there and still billed. That is the feature
         (you can undelete) and the bill (you are paying for every
         version of every object until a lifecycle rule removes
         them)""")

    # ---- storage classes ------------------------------------------------
    print("\n    storage classes -- 1 TB stored for a year, "
          "retrieved once:")
    gb = 1024
    print(f"      {'class':<22}{'storage/yr':>12}{'retrieve 1 TB':>15}"
          f"{'total':>12}{'min days':>10}")
    rows = {}
    for cls in f.S3_STORAGE:
        store = f.S3_STORAGE[cls] * gb * 12
        retrieve = f.S3_RETRIEVAL[cls] * gb
        rows[cls] = store + retrieve
        print(f"      {cls:<22}{money(store):>12}{money(retrieve):>15}"
              f"{money(store + retrieve):>12}{f.S3_MIN_DAYS[cls]:>10}")
    ratio = rows["Standard"] / rows["Glacier Deep Archive"]
    store_only = f.S3_STORAGE["Standard"] / f.S3_STORAGE["Glacier Deep Archive"]
    assert rows["Glacier Deep Archive"] < rows["Standard"] / 5
    assert store_only > 2 * ratio
    print(f"""         READ THE TWO RATIOS SEPARATELY. Deep Archive STORAGE is
         {store_only:.0f}x cheaper than Standard -- but add ONE retrieval a year
         and the all-in saving falls to {ratio:.1f}x, because the retrieval
         fee ({money(f.S3_RETRIEVAL['Glacier Deep Archive'] * gb)}) is larger than a year of its storage
         ({money(f.S3_STORAGE['Glacier Deep Archive'] * gb * 12)}). The headline discount is not the discount.
         And it has a 180-DAY MINIMUM BILLING DURATION plus a
         retrieval that takes up to 12 hours: delete an object after
         10 days and you are billed for 180.
         Storage class is a bet on your ACCESS PATTERN, and the
         penalties are what make the bet real""")

    # ---- the frequent-access reversal -----------------------------------
    print("\n    the same 1 TB, retrieved TWICE A MONTH:")
    print(f"      {'class':<22}{'storage/yr':>12}{'retrieval/yr':>14}{'total':>12}")
    freq = {}
    for cls in ("Standard", "Standard-IA", "Glacier Instant"):
        store = f.S3_STORAGE[cls] * gb * 12
        retrieve = f.S3_RETRIEVAL[cls] * gb * 24
        freq[cls] = store + retrieve
        print(f"      {cls:<22}{money(store):>12}{money(retrieve):>14}"
              f"{money(store + retrieve):>12}")
    assert freq["Standard"] < freq["Standard-IA"]
    assert freq["Standard"] < freq["Glacier Instant"]
    print("""         STANDARD IS NOW THE CHEAPEST. The 'cheap' tiers charge
         per GB retrieved, and at two retrievals a month the retrieval
         fee exceeds everything the storage discount saved.
         Infrequent-access tiers are for data you genuinely do not
         touch -- and 'we moved everything to IA to save money' is how
         a bill goes UP""")

    # ---- egress ---------------------------------------------------------
    print("\n    egress, which is the line item nobody predicts:")
    print(f"      {'transfer':<40}{'cost'}")
    for label, amount in (("1 TB in from the internet", 0),
                          ("1 TB out to the internet", gb * f.EGRESS_PER_GB),
                          ("1 TB between AZs", gb * 0.01 * 2),
                          ("1 TB S3 -> EC2, same region", 0)):
        print(f"      {label:<40}{money(amount)}")
    month_store = f.S3_STORAGE["Standard"] * gb
    one_egress = gb * f.EGRESS_PER_GB
    months = one_egress / month_store
    assert months > 3
    print(f"""         DOWNLOADING 1 TB ONCE ({money(one_egress)}) COSTS AS MUCH AS
         STORING IT FOR {months:.1f} MONTHS ({money(month_store)}/month). Ingress is
         free; egress is not. That asymmetry is the economic shape of
         every cloud -- cheap to put data in, expensive to take it out
         -- and it is the mechanism behind vendor lock-in: your data
         is not held hostage, it is simply expensive to move.
         It is also why 'move the compute to the data' survived from
         Course 12 B into the cloud era: run the job in the region
         holding the bucket and the transfer is free""")

    # ================================================== experiments 5, 6
    print("\n    --- experiments 5 and 6: block and file storage")
    print(f"\n      {'':<18}{'BLOCK (EBS)':<26}{'FILE (EFS)':<26}"
          f"{'OBJECT (S3)'}")
    for label, blk, fil, obj in (
            ("looks like", "a raw disk", "a mounted filesystem", "an HTTP API"),
            ("attached to", "ONE instance*", "MANY instances", "anything, anywhere"),
            ("access unit", "a 512 B block", "a file, byte ranges", "a whole object"),
            ("in-place edit", "yes", "yes", "NO -- rewrite it"),
            ("directories", "whatever the FS does", "real", "NONE -- prefixes"),
            ("latency", "sub-millisecond", "low millisecond", "tens of ms"),
            ("capacity", "provisioned, fixed", "elastic", "unlimited"),
            ("survives instance", "yes, if not root", "yes", "yes"),
            ("$/GB-month", f"{f.EBS_GP3_GB_MONTH:.3f}",
             f"{f.EFS_STANDARD_GB_MONTH:.2f}",
             f"{f.S3_STORAGE['Standard']:.3f}"),
    ):
        print(f"      {label:<18}{blk:<26}{fil:<26}{obj}")
    print("      * EBS Multi-Attach exists for io1/io2 and needs a "
          "cluster filesystem")

    print("\n    1 TB for a month, by type:")
    for label, price in (("EBS gp3", f.EBS_GP3_GB_MONTH),
                         ("EFS Standard", f.EFS_STANDARD_GB_MONTH),
                         ("S3 Standard", f.S3_STORAGE["Standard"])):
        print(f"      {label:<16}{money(price * gb):>10}")
    ebs, efs, s3c = (p * gb for p in (f.EBS_GP3_GB_MONTH,
                                      f.EFS_STANDARD_GB_MONTH,
                                      f.S3_STORAGE["Standard"]))
    assert efs > ebs > s3c
    print(f"""         EFS costs {efs / s3c:.0f}x what S3 does and {efs / ebs:.1f}x what EBS does,
         and it is worth it precisely when several instances must
         share a POSIX filesystem. Paying {efs / s3c:.0f}x for a dataset that one
         batch job reads once is the mistake -- that dataset belongs
         in S3.
         Choose by ACCESS PATTERN, not by price: block for a database
         or a boot disk, file for shared POSIX, object for everything
         a data pipeline reads""")

    # ---- provisioned against consumed ------------------------------------
    print("\n    provisioned against consumed, on a 1 TB EBS volume "
          "holding 200 GB:")
    print(f"      EBS billed on PROVISIONED size : "
          f"{money(f.EBS_GP3_GB_MONTH * gb)}/month")
    print(f"      S3 billed on STORED bytes      : "
          f"{money(f.S3_STORAGE['Standard'] * 200)}/month")
    over = f.EBS_GP3_GB_MONTH * gb
    used = f.S3_STORAGE["Standard"] * 200
    assert over > used * 15
    print(f"""         a factor of {over / used:.0f}. EBS bills the volume you asked for,
         empty or not; S3 bills the bytes you actually stored. An
         over-provisioned volume is invisible waste, which is why
         'just make it 1 TB to be safe' is an expensive habit""")


if __name__ == "__main__":
    main()
