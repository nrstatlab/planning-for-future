# Stage 5 -- the DOCUMENT model, implemented in plain Python so that the
# semantics of every PyMongo call above can be checked without a server.
# Each function here does exactly what the collection method beside it does.
import copy

# Step 1: The collection: four customer documents
DOCS = [
    {"_id": 1, "name": "Asha Rao",   "address": {"city": "Vizag"},
     "income": 40, "tags": ["retail", "west"],
     "orders": [{"amt": 1240.50}, {"amt": 480.00}, {"amt": 75.25}]},
    {"_id": 2, "name": "Biju Menon", "address": {"city": "Kochi"},
     "income": 57, "tags": ["wholesale"], "orders": [{"amt": 99.00}]},
    {"_id": 3, "name": "Chitra Das", "address": {"city": "Kolkata"},
     "income": 37, "tags": ["retail", "east"],
     "orders": [{"amt": 15750.75}]},
    {"_id": 4, "name": "Devan Iyer", "address": {"city": "Madurai"},
     "income": 69, "tags": ["retail"], "orders": [{"amt": 310.25}]},
]

# Step 2: find, with a query and a projection
def dig(doc, path):
    """Resolve a dotted path such as address.city."""
    cur = doc
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur

OPS = {"$gt": lambda a, b: a is not None and a > b,
       "$gte": lambda a, b: a is not None and a >= b,
       "$lt": lambda a, b: a is not None and a < b,
       "$in": lambda a, b: a in b or (isinstance(a, list) and set(a) & set(b)),
       "$eq": lambda a, b: a == b}

def matches(doc, query):
    for field, cond in query.items():
        value = dig(doc, field)
        if isinstance(cond, dict):
            for op, arg in cond.items():
                if not OPS[op](value, arg):
                    return False
        elif isinstance(value, list):
            if cond not in value:          # arrays match on any element
                return False
        elif value != cond:
            return False
    return True

def project(doc, spec):
    if not spec:
        return copy.deepcopy(doc)
    keep = {k for k, v in spec.items() if v}
    out = {}
    for k in keep:
        v = dig(doc, k)
        if v is not None:
            out[k] = v
    if spec.get("_id", 1):
        out["_id"] = doc["_id"]
    return out

def find(docs, query=None, projection=None):
    return [project(d, projection) for d in docs if matches(d, query or {})]

print("find all:", len(find(DOCS)), "document(s)")
print("find {'address.city': 'Kochi'}:",
      find(DOCS, {"address.city": "Kochi"}, {"name": 1, "_id": 0}))
print("find {'income': {'$gt': 40}}:",
      [d["name"] for d in find(DOCS, {"income": {"$gt": 40}})])
print("find {'tags': 'retail'} (array matches any element):",
      [d["name"] for d in find(DOCS, {"tags": "retail"})])

# Step 3: update_one with $set and $inc
def update_one(docs, query, update):
    for d in docs:
        if matches(d, query):
            for field, value in update.get("$set", {}).items():
                d[field] = value
            for field, value in update.get("$inc", {}).items():
                d[field] = d.get(field, 0) + value
            return 1
    return 0

n = update_one(DOCS, {"_id": 1}, {"$set": {"status": "gold"}, "$inc": {"income": 5}})
print()
print(f"update_one matched {n}; doc 1 is now income={DOCS[0]['income']},"
      f" status={DOCS[0]['status']!r}")
print("  $set adds a field that no other document has -- no schema objects,")
print("  and no other document is touched.  That is the whole difference from SQL.")

# Step 4: replace_one keeps the _id and discards everything else
def replace_one(docs, query, doc):
    for i, d in enumerate(docs):
        if matches(d, query):
            new = dict(doc)
            new["_id"] = d["_id"]
            docs[i] = new
            return 1
    return 0

replace_one(DOCS, {"_id": 4}, {"name": "Devan Iyer", "income": 70})
print()
print("after replace_one, doc 4 =", DOCS[3])
print("  address, tags and orders are GONE.  replace_one is not update_one;")
print("  confusing the two is how live collections lose fields.")

# Step 5: delete_many
def delete_many(docs, query):
    keep = [d for d in docs if not matches(d, query)]
    removed = len(docs) - len(keep)
    docs[:] = keep
    return removed

print()
print("delete_many({'income': {'$lt': 40}}) removed",
      delete_many(DOCS, {"income": {"$lt": 40}}), "document(s);",
      len(DOCS), "remain")

# Step 6: An aggregation pipeline: unwind, group, sort
def aggregate(docs, pipeline):
    stage_docs = [copy.deepcopy(d) for d in docs]
    for stage in pipeline:
        (op, spec), = stage.items()
        if op == "$match":
            stage_docs = [d for d in stage_docs if matches(d, spec)]
        elif op == "$unwind":
            path = spec.lstrip("$")
            out = []
            for d in stage_docs:
                for item in dig(d, path) or []:
                    copyd = copy.deepcopy(d)
                    copyd[path] = item
                    out.append(copyd)
            stage_docs = out
        elif op == "$group":
            groups = {}
            for d in stage_docs:
                key = dig(d, spec["_id"].lstrip("$"))
                g = groups.setdefault(key, {"_id": key})
                for field, acc in spec.items():
                    if field == "_id":
                        continue
                    (fn, arg), = acc.items()
                    val = 1 if fn == "$sum" and arg == 1 else dig(d, str(arg).lstrip("$"))
                    g[field] = g.get(field, 0) + (val or 0)
            stage_docs = list(groups.values())
        elif op == "$sort":
            for field, direction in reversed(list(spec.items())):
                stage_docs.sort(key=lambda d: d[field], reverse=direction < 0)
    return stage_docs

print()
print("aggregate runs on what is LEFT after the three mutations above:",
      len(DOCS), "documents")
print("aggregate: total order value per customer, largest first")
for row in aggregate(DOCS, [{"$unwind": "$orders"},
                            {"$group": {"_id": "$name", "n": {"$sum": 1},
                                        "total": {"$sum": "$orders.amt"}}},
                            {"$sort": {"total": -1}}]):
    print(f"   {row['_id']:12s} {row['n']} order(s)  total {row['total']:9.2f}")
print("  Devan Iyer is absent although he is still in the collection: replace_one")
print("  removed his orders array, and $unwind DROPS a document whose array is")
print("  missing or empty rather than passing it through.  Use")
print("  {'$unwind': {'path': '$orders', 'preserveNullAndEmptyArrays': True}}")
print("  when that is not what you want.")

# Step 7: What an index buys, counted
def scan(docs, key):
    seen = 0
    for d in docs:
        seen += 1
        if d["_id"] == key:
            return d, seen
    return None, seen

index = {d["_id"]: d for d in DOCS}
doc, seen = scan(DOCS, 2)
print()
print(f"collection scan for _id=2 examined {seen} of {len(DOCS)} documents")
print(f"index lookup examined 1, and found {index[2]['name']!r}")
print("on three documents this is a curiosity; on four million it is the")
print("difference between a query and an outage.")
