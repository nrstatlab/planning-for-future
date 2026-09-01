"""Experiment 15 -- create and manage tables in HBase (CRUD operations).

HBase is not installed. `15_hbase.rb` carries the real shell commands, marked
NOT EXECUTED. What runs here is HBase's DATA MODEL, implemented honestly:
a sorted map from (row, family:qualifier, version) to bytes, with real
versioning, real tombstones and real row-key range scans.

The model IS the exam. Almost every HBase question -- why scans are fast and
gets by value are not, why a monotonic row key is a disaster, why a delete
does not free space -- is a consequence of "sorted map, sharded by row-key
range".
"""
import bisect

import fixtures as f


class HBase:
    """(row, family, qualifier) -> {timestamp: value}, kept SORTED BY ROW."""

    def __init__(self, families, max_versions=3):
        self.families = set(families)
        self.max_versions = max_versions
        self.cells = {}
        self.rows = []              # sorted, because everything depends on it
        self.clock = 0

    def _tick(self):
        self.clock += 1
        return self.clock

    def put(self, row, fam, qual, value):
        if fam not in self.families:
            raise KeyError(f"column family {fam!r} was not declared at create time")
        if row not in self.cells:
            bisect.insort(self.rows, row)
            self.cells[row] = {}
        versions = self.cells[row].setdefault((fam, qual), {})
        versions[self._tick()] = value
        for ts in sorted(versions)[:-self.max_versions]:
            del versions[ts]

    def get(self, row, fam=None, qual=None, versions=1):
        if row not in self.cells:
            return {}
        out = {}
        for (fm, q), vs in self.cells[row].items():
            if fam and fm != fam:
                continue
            if qual and q != qual:
                continue
            live = []
            for ts, v in sorted(vs.items(), reverse=True):
                if v is None:
                    break          # a tombstone MASKS every older version
                live.append((ts, v))
            live = live[:versions]
            if live:
                out[f"{fm}:{q}"] = live if versions > 1 else live[0][1]
        return out

    def delete(self, row, fam, qual):
        """A delete writes a TOMBSTONE. It does not remove anything."""
        self.cells[row].setdefault((fam, qual), {})[self._tick()] = None

    def scan(self, start=None, stop=None):
        lo = bisect.bisect_left(self.rows, start) if start else 0
        hi = bisect.bisect_left(self.rows, stop) if stop else len(self.rows)
        return [(r, self.get(r)) for r in self.rows[lo:hi]]

    def storefiles(self):
        """Every version and every tombstone still occupies a cell."""
        return sum(len(v) for row in self.cells.values() for v in row.values())


def main():
    print("  Experiment 15 -- the HBase data model, implemented")

    t = HBase(families={"info", "sales"}, max_versions=3)

    # ---- CREATE and PUT --------------------------------------------------
    # First, a row key that looks reasonable and is NOT unique at the grain.
    naive = {f"{r['region']}#{r['store']}#{r['date_key']}"
             for _, r in f.SALES_DF.iterrows()}
    print(f"\n    row key 'region#store#date' over {len(f.SALES_DF)} fact rows")
    print(f"    produces only {len(naive)} DISTINCT KEYS -- "
          f"{len(f.SALES_DF) - len(naive)} row would be overwritten")
    assert len(naive) == 8, "two facts share a store and a date"
    print("""         Vijayawada sold Rice AND Shampoo on D1, so those two
         facts collide. HBase would not complain -- it would simply
         version one over the other and lose a sale.
         A row key must be UNIQUE AT THE GRAIN. In an RDBMS the
         primary key declaration catches this; in HBase nothing does,
         and that is the failure mode to remember""")

    for _, r in f.SALES_DF.iterrows():
        # row key: region#store#date#product -- unique, composite, NOT monotonic
        key = (f"{r['region']}#{r['store']}#{r['date_key']}#"
               f"{r['product'].split()[0]}")
        t.put(key, "info", "product", r["product"])
        t.put(key, "info", "category", r["category"])
        t.put(key, "sales", "qty", int(r["qty"]))
        t.put(key, "sales", "revenue", float(r["revenue"]))

    print(f"\n    {len(t.rows)} rows, {t.storefiles()} cells")
    print(f"    row keys are SORTED, always:")
    for k in t.rows[:4]:
        print(f"      {k}")
    print(f"      ... {len(t.rows) - 4} more")
    assert t.rows == sorted(t.rows)

    # ---- GET -------------------------------------------------------------
    key = t.rows[0]
    print(f"\n    GET '{key}':")
    for col, val in sorted(t.get(key).items()):
        print(f"      {col:<18}{val}")

    # ---- versions --------------------------------------------------------
    t.put(key, "sales", "qty", 99)
    t.put(key, "sales", "qty", 111)
    vs = t.get(key, "sales", "qty", versions=3)["sales:qty"]
    print(f"\n    after two more PUTs to the same cell, 3 versions:")
    for ts, v in vs:
        print(f"      ts={ts:<5}{v}")
    assert [v for _, v in vs][:2] == [111, 99]
    assert len(vs) == 3, "VERSIONS => 3 caps the history at three"
    print("""         a PUT to an existing cell does not overwrite -- it adds a
         VERSION, and the old value is still readable. VERSIONS => 3
         at create time is what caps it. That is why HBase is
         described as a multidimensional map: row, family, qualifier
         AND time""")

    # ---- delete ----------------------------------------------------------
    before = t.storefiles()
    t.delete(key, "info", "category")
    after = t.storefiles()
    assert "info:category" not in t.get(key)
    assert after > before, "a delete makes the table BIGGER until compaction"
    print(f"\n    DELETE info:category")
    print(f"      readable? {'yes' if 'info:category' in t.get(key) else 'no'}")
    print(f"      cells:    {before} -> {after}")
    print("""         THE TABLE GOT BIGGER. A delete writes a tombstone marker;
         the data and the marker both disappear only at MAJOR
         COMPACTION. This is the answer to 'I deleted a billion rows
         and disk usage went up'""")

    # ---- scan ------------------------------------------------------------
    south = t.scan("South", "South~")
    north = t.scan("North", "North~")
    print(f"\n    SCAN 'South' .. 'South~' -> {len(south)} rows")
    print(f"    SCAN 'North' .. 'North~' -> {len(north)} rows")
    assert len(south) + len(north) == len(t.rows)
    assert len(south) == 6 and len(north) == 3
    assert len(t.rows) == 9, "the unique key keeps all nine facts"
    print("""         a range scan on the row-key PREFIX reads exactly the
         rows you want, sequentially, from one or two regions. That
         is the fastest thing HBase does -- and it works only because
         'region' is the FIRST component of the key""")

    print("\n    the same question asked the wrong way:")
    matches = [r for r, cols in t.scan() if cols.get("info:category") == "Grocery"]
    print(f"      find category = 'Grocery' -> {len(matches)} rows, "
          f"after scanning all {len(t.rows)}")
    print("""         HBase has NO SECONDARY INDEX. Filtering on a value means
         a FULL TABLE SCAN with a server-side filter -- correct, and
         O(table). If you need that query, you build a second table
         keyed by category, and you keep it in sync yourself""")

    # ---- row key design --------------------------------------------------
    print("\n    row key design, which is the whole job:")
    print(f"      {'key':<34}{'regions hit by a write':<24}verdict")
    for key_desc, hits, verdict in (
            ("timestamp (1723459200, ...)", "ONE -- always the last", "HOTSPOT"),
            ("sequential id (1, 2, 3, ...)", "ONE -- always the last", "HOTSPOT"),
            ("md5(id) + id", "all, evenly", "good, scans lost"),
            ("region#store#date", "by region", "good, prefix scans work")):
        print(f"      {key_desc:<34}{hits:<24}{verdict}")
    print("""         a monotonically increasing row key sends EVERY write to
         the same RegionServer, so a 50-node cluster runs at the
         speed of one node. Salting or hashing fixes the hotspot and
         destroys range scans -- you cannot have both, and choosing
         is what row-key design means""")

    # ---- HBase against the two things it is confused with ----------------
    print("\n    HBase against what students compare it to:")
    print(f"      {'':<14}{'HBase':<26}{'Hive':<22}{'MongoDB (Course 10)'}")
    for label, hb, hv, mg in (
            ("model", "sparse sorted map", "tables over files", "documents"),
            ("latency", "milliseconds", "seconds to minutes", "milliseconds"),
            ("random writes", "YES", "no", "YES"),
            ("secondary index", "no", "no", "YES"),
            ("query language", "get/put/scan only", "HiveQL", "MQL"),
            ("schema", "families fixed, cols free", "fixed", "free")):
        print(f"      {label:<14}{hb:<26}{hv:<22}{mg}")
    print("""         HBase and Hive both sit on HDFS and answer completely
         different questions: Hive scans everything slowly, HBase
         fetches one row instantly. And note the row students always
         get wrong -- HBase has NO secondary index where MongoDB
         does, which is the sharpest difference between the two
         NoSQL stores this programme teaches""")


if __name__ == "__main__":
    main()
