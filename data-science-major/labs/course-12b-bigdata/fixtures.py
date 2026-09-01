"""Shared data for Course 12 B.

Three datasets, deliberately small enough to check by hand, and one of them
deliberately IMPORTED from Course 11 rather than copied, so the two courses
cannot drift apart:

  * SALES  -- Course 11's star schema, loaded from labs/course-11-bi/fixtures.py
              at import time. A Hive query here and a DAX measure there are
              computed from THE SAME NINE ROWS, so if they disagree, one of
              them is wrong and the suite says so.
  * DOCS   -- six short documents, used for word count (experiment 7) and for
              the inverted index (experiment 8). Every count is small enough
              to verify by counting.
  * LOGS   -- 40 deterministic Apache-style access log lines, used for the
              Flume (12) and Spark (17) experiments. No randomness anywhere.
"""
import importlib.util
import pathlib

# Course 11's fixtures module is also called "fixtures", so it is loaded by
# path under a distinct name rather than through sys.path -- otherwise the two
# collide and Python hands back this half-built module instead.
_C11_PATH = (pathlib.Path(__file__).resolve().parents[1]
             / "course-11-bi" / "fixtures.py")
_spec = importlib.util.spec_from_file_location("c11_fixtures", _C11_PATH)
c11 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(c11)

# ---------------------------------------------------------------- sales
# The flat star, exactly as Course 11 builds it: nine fact rows joined to four
# dimensions, with revenue, cost and profit derived.
SALES_DF = c11.star()
SALES_COLUMNS = list(SALES_DF.columns)
SALES = [tuple(r) for r in SALES_DF.itertuples(index=False)]

# ---------------------------------------------------------------- documents

DOCS = {
    "doc1.txt": "the quick brown fox jumps over the lazy dog",
    "doc2.txt": "the lazy dog sleeps all day",
    "doc3.txt": "a quick brown dog outpaces a quick fox",
    "doc4.txt": "big data is data that is too big for one machine",
    "doc5.txt": "hadoop stores big data and spark processes big data",
    "doc6.txt": "the fox and the dog",
}

# ---------------------------------------------------------------- logs


def access_logs(n=40):
    """Deterministic Apache-style access lines -- no randomness anywhere."""
    ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4"]
    paths = ["/index.html", "/api/sales", "/api/sales", "/login", "/static/app.js"]
    codes = [200, 200, 200, 404, 500]
    out = []
    for i in range(n):
        out.append(
            f'{ips[i % len(ips)]} - - [12/Aug/2025:{9 + i // 10:02d}:'
            f'{(i * 7) % 60:02d}:00 +0530] "GET {paths[i % len(paths)]} '
            f'HTTP/1.1" {codes[i % len(codes)]} {512 + i * 13}'
        )
    return out


# ---------------------------------------------------------------- helpers


def sales_dicts():
    return SALES_DF.to_dict(orient="records")


def total_revenue():
    return float(SALES_DF["revenue"].sum())
