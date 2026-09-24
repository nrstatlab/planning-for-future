"""Experiment 13 -- serialize and store datasets in Avro and Parquet.

THIS EXPERIMENT FULLY RUNS. fastavro and pyarrow are real implementations of
the real formats, so the files written here are byte-for-byte readable by
Hadoop, Hive and Spark. Nothing is simulated.

The point of the experiment is not "how do I call the library" -- it is the
difference between a ROW format and a COLUMN format, which decides everything
about how a big-data query performs.
"""
import io
import json
import os
import tempfile

import fastavro
import pyarrow as pa
import pyarrow.parquet as pq

import fixtures as f

AVRO_SCHEMA = {
    "type": "record",
    "name": "Sale",
    "namespace": "in.ac.datascience.sales",
    "fields": [
        {"name": "date_key", "type": "string"},
        {"name": "store", "type": "string"},
        {"name": "region", "type": "string"},
        {"name": "product", "type": "string"},
        {"name": "category", "type": "string"},
        {"name": "qty", "type": "long"},
        {"name": "revenue", "type": "double"},
        {"name": "profit", "type": "double"},
    ],
}

FIELDS = [fld["name"] for fld in AVRO_SCHEMA["fields"]]


def records():
    return [{k: (int(r[k]) if k == "qty" else r[k]) for k in FIELDS}
            for _, r in f.SALES_DF.iterrows()]


def main():
    print("  Experiment 13 -- Avro and Parquet, both really written")

    rows = records()
    tmp = tempfile.mkdtemp(prefix="bigdata13_")

    # ---- Avro ------------------------------------------------------------
    avro_path = os.path.join(tmp, "sales.avro")
    with open(avro_path, "wb") as fh:
        fastavro.writer(fh, fastavro.parse_schema(AVRO_SCHEMA), rows)
    with open(avro_path, "rb") as fh:
        back = list(fastavro.reader(fh))
    assert back == rows, "Avro must round-trip exactly"
    avro_size = os.path.getsize(avro_path)
    # The notes quote this figure, so it is asserted. It is deterministic --
    # fixed rows, fixed schema -- but NOT independent of the schema's text:
    # the namespace is stored in the file header, so renaming it moves the
    # byte count. That is how this assertion earns its place; the figure had
    # already drifted once, silently, when the namespace changed.
    assert avro_size == 938, (
        f"Avro file is {avro_size} bytes, the notes say 938 -- "
        "update lab.md and unit-4.md, or find out what changed")
    print(f"\n    Avro   : {len(rows)} records, {avro_size} bytes, round-trip exact")

    # the schema travels INSIDE the file -- this is the property that matters
    with open(avro_path, "rb") as fh:
        embedded = fastavro.reader(fh).writer_schema
    assert embedded["name"] == "in.ac.datascience.sales.Sale", (
        "Avro stores the FULL name -- namespace + name -- not the short one")
    assert [fl["name"] for fl in embedded["fields"]] == FIELDS
    print(f"\n      the embedded schema's full name is {embedded['name']!r}")
    print("""         the WRITER'S SCHEMA is stored in the file header, so an
         Avro file is self-describing. A reader five years later needs
         no external metadata, which is exactly what a CSV cannot
         promise -- and why Avro is the ingestion format""")

    # ---- schema evolution, demonstrated ----------------------------------
    evolved = json.loads(json.dumps(AVRO_SCHEMA))
    evolved["fields"].append(
        {"name": "channel", "type": ["null", "string"], "default": None})
    buf = io.BytesIO()
    with open(avro_path, "rb") as fh:
        old_bytes = fh.read()
    read_new = list(fastavro.reader(io.BytesIO(old_bytes),
                                    reader_schema=fastavro.parse_schema(evolved)))
    assert all(r["channel"] is None for r in read_new)
    assert len(read_new) == len(rows)
    print(f"\n    schema evolution: read {len(rows)} OLD records with a NEW schema")
    print(f"      the added field 'channel' comes back as "
          f"{read_new[0]['channel']!r} -- its DEFAULT")
    print("""         the old file was NOT rewritten. Avro resolves the writer's
         schema against the reader's, field by field, and fills in
         defaults for anything missing. A field added WITHOUT a
         default breaks exactly this, which is the one rule to
         remember about evolving an Avro schema""")

    # ---- Parquet ---------------------------------------------------------
    table = pa.Table.from_pylist(rows)
    pq_path = os.path.join(tmp, "sales.parquet")
    pq.write_table(table, pq_path, compression="snappy")
    pq_size = os.path.getsize(pq_path)
    back_pq = pq.read_table(pq_path).to_pylist()
    assert back_pq == rows, "Parquet must round-trip exactly"
    print(f"\n    Parquet: {len(rows)} records, {pq_size} bytes, round-trip exact")

    # column projection -- the whole reason Parquet exists
    one_col = pq.read_table(pq_path, columns=["revenue"])
    assert one_col.num_columns == 1 and one_col.num_rows == len(rows)
    meta = pq.ParquetFile(pq_path).metadata
    rg = meta.row_group(0)
    col_sizes = {rg.column(i).path_in_schema:
                 rg.column(i).total_compressed_size
                 for i in range(rg.num_columns)}
    print(f"\n    bytes stored PER COLUMN inside the Parquet file:")
    for name, sz in sorted(col_sizes.items(), key=lambda kv: -kv[1]):
        print(f"      {name:<12}{sz:>7}")
    total = sum(col_sizes.values())
    rev = col_sizes["revenue"]
    print(f"      {'TOTAL':<12}{total:>7}")
    print(f"\n    SELECT revenue reads {rev} of {total} column bytes "
          f"({100 * rev / total:.1f}%)")
    assert rev < total / 4
    print("""         THAT is column projection, and it is why Parquet wins on
         analytical queries: a SELECT of one column out of eight
         reads roughly one column's worth of bytes. A row format has
         to read every row in full and discard seven fields""")

    # predicate pushdown via row-group statistics
    stats = rg.column([i for i in range(rg.num_columns)
                       if rg.column(i).path_in_schema == "revenue"][0]).statistics
    print(f"\n    row-group statistics for 'revenue': "
          f"min {stats.min:,.0f}, max {stats.max:,.0f}")
    assert stats.min == 600.0 and stats.max == 2800.0
    print("""         a query for revenue > 5000 can SKIP THIS ENTIRE ROW GROUP
         without decoding a byte, because the max is 2,800. That is
         predicate pushdown, and on a partitioned Parquet dataset it
         is often a bigger win than the compression""")

    # ---- the comparison the exam asks for --------------------------------
    csv_path = os.path.join(tmp, "sales.csv")
    f.SALES_DF[FIELDS].to_csv(csv_path, index=False)
    csv_size = os.path.getsize(csv_path)
    print(f"\n    {'format':<12}{'bytes':>8}  {'layout':<8}{'schema':<15}{'best for'}")
    for name, size, layout, schema, use in (
            ("CSV", csv_size, "row", "none", "interchange, and nothing else"),
            ("Avro", avro_size, "row", "in the file", "ingestion, streaming, evolution"),
            ("Parquet", pq_size, "COLUMN", "in the footer", "analytics, column projection"),
            ("SequenceFile", None, "row", "external", "legacy Hadoop key/value")):
        shown = f"{size:>8}" if size else f"{'--':>8}"
        print(f"    {name:<12}{shown}  {layout:<8}{schema:<15}{use}")
    print(f"""
         on NINE ROWS Parquet is LARGER than CSV ({pq_size} against
         {csv_size}) -- the footer, the schema and the per-column
         metadata are fixed overhead that nine rows cannot amortise.
         Report that honestly: Parquet's advantage is asymptotic, and
         quoting a compression ratio from a toy file is how people
         get caught out in a viva""")

    # ---- and now at a size where the claim can be tested ----------------
    # 108,000 records. TWO versions: one that repeats the nine rows exactly,
    # and one where every row differs -- because a columnar format's headline
    # ratio is mostly a statement about how repetitive the data is, and
    # quoting the repetitive number alone would be misleading.
    big = rows * 12000
    varied = [dict(r, qty=r["qty"] + i % 97,
                   revenue=r["revenue"] + (i % 8191) * 0.25,
                   store=f"{r['store']}-{i % 500}")
              for i, r in enumerate(big)]
    vsizes = {}
    for name, data in (("repetitive", big), ("varied", varied)):
        va = os.path.join(tmp, f"v_{name}.avro")
        vp = os.path.join(tmp, f"v_{name}.parquet")
        vc = os.path.join(tmp, f"v_{name}.csv")
        with open(va, "wb") as fh:
            fastavro.writer(fh, fastavro.parse_schema(AVRO_SCHEMA), data)
        pq.write_table(pa.Table.from_pylist(data), vp, compression="snappy")
        with open(vc, "w") as fh:
            fh.write(",".join(FIELDS) + "\n")
            for r in data:
                fh.write(",".join(str(r[k]) for k in FIELDS) + "\n")
        vsizes[name] = {"CSV": os.path.getsize(vc), "Avro": os.path.getsize(va),
                        "Parquet": os.path.getsize(vp)}
        for pth in (va, vp, vc):
            os.remove(pth)

    print(f"\n    the same schema at {len(big):,} records:")
    print(f"      {'data':<12}{'CSV':>12}{'Avro':>12}{'Parquet':>12}"
          f"{'CSV/Parquet':>13}")
    for name in ("repetitive", "varied"):
        z = vsizes[name]
        print(f"      {name:<12}{z['CSV']:>12,}{z['Avro']:>12,}"
              f"{z['Parquet']:>12,}{z['CSV'] / z['Parquet']:>12.1f}x")
    rep = vsizes["repetitive"]["CSV"] / vsizes["repetitive"]["Parquet"]
    var = vsizes["varied"]["CSV"] / vsizes["varied"]["Parquet"]
    assert rep > var * 5, "the repetitive figure must be visibly inflated"
    assert var > 1.5, "Parquet should still beat CSV on varied data"
    print(f"""         READ BOTH ROWS. The {rep:.0f}x on repetitive data is an
         ARTEFACT: 12,000 identical copies of nine rows dictionary-
         encode to almost nothing. Give every row a distinct store
         and revenue and the ratio falls to {var:.1f}x. Even that is
         optimistic -- date, region and category are still repetitive
         here -- and Parquet-against-CSV in production usually lands
         between 3x and 10x.
         A columnar format's headline compression number is mostly a
         statement about how REPETITIVE your data is, and a benchmark
         on duplicated rows says nothing at all""")

    print("\n    which format for which job:")
    print("      row-by-row WRITES, whole-record reads     -> Avro")
    print("      column aggregates over billions of rows   -> Parquet")
    print("      a landing zone that must survive schema")
    print("      changes for years                         -> Avro")
    print("      the table Hive and Spark actually query   -> Parquet")
    print("""         the standard architecture uses BOTH: Avro at the edge
         where records arrive one at a time and schemas drift, then a
         batch job converts to Parquet for the query layer. That
         answer is worth full marks on 'compare Avro and Parquet'""")

    for path in (avro_path, pq_path, csv_path):
        os.remove(path)
    os.rmdir(tmp)


if __name__ == "__main__":
    main()
