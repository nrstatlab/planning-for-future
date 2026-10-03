# Stage 1b -- the anomaly pass.  Every record that fails is COUNTED and
# REPORTED, never silently dropped: a pipeline that quietly loses rows is
# worse than one that stops, because nobody finds out.
# Step 1: The batch, with five faults in it
RAW = [
    {"id": "1", "name": "Asha Rao",   "city": "Vizag",   "income": "40", "visits": "7"},
    {"id": "2", "name": "Biju Menon", "city": "Kochi",   "income": "57", "visits": "5"},
    {"id": "3", "name": "Chitra Das", "city": "",        "income": "37", "visits": "8"},
    {"id": "4", "name": "Devan Iyer", "city": "Madurai", "income": "n/a", "visits": "10"},
    {"id": "5", "name": "Esha Khan",  "city": "Bhopal",  "income": "36"},
    {"id": "2", "name": "Biju Menon", "city": "Kochi",   "income": "57", "visits": "5"},
    {"id": "7", "name": "Gita Nair",  "city": "Surat",   "income": "48", "visits": "-3"},
]

# Step 2: What each field must be
REQUIRED = ("id", "name", "city", "income", "visits")
NUMERIC = {"id": int, "income": int, "visits": int}
RANGES = {"income": (0, 1000), "visits": (0, 365)}

# Step 3: Presence, then type, then range, then duplicates, record by record
def clean(rows):
    good, problems = [], []
    seen = set()
    for i, r in enumerate(rows, 1):
        issues = []

        missing = [f for f in REQUIRED if f not in r]
        if missing:
            issues.append(f"missing field(s) {missing}")
        blank = [f for f in REQUIRED if f in r and str(r[f]).strip() == ""]
        if blank:
            issues.append(f"blank field(s) {blank}")

        typed = {}
        for f, fn in NUMERIC.items():
            if f in r and str(r[f]).strip() != "":
                try:
                    typed[f] = fn(r[f])
                except ValueError:
                    issues.append(f"{f}={r[f]!r} is not an integer")

        for f, (lo, hi) in RANGES.items():
            if f in typed and not (lo <= typed[f] <= hi):
                issues.append(f"{f}={typed[f]} outside [{lo}, {hi}]")

        key = r.get("id")
        if key in seen:
            issues.append(f"duplicate id {key}")
        elif key is not None:
            seen.add(key)

        if issues:
            problems.append((i, key, issues))
        else:
            rec = dict(r)
            rec.update(typed)
            good.append(rec)
    return good, problems

# Step 4: Run the pass, and report every rejection with its reason
good, problems = clean(RAW)
print(f"read {len(RAW)} record(s): {len(good)} accepted, {len(problems)} rejected")
print()
print("rejected, with the reason:")
for i, key, issues in problems:
    print(f"  row {i} (id {key}): " + "; ".join(issues))
print()
# Step 5: The accepted records, now typed
print("accepted:")
for r in good:
    print("  ", r)
print()
# Step 6: Why the order of the checks matters
print("the three checks in order, and why the order matters:")
print("  presence  -> a missing field cannot be converted")
print("  type      -> a non-integer cannot be range-checked")
print("  range     -> and only a number has a range")
print("running them in any other order raises exceptions instead of reporting faults.")
