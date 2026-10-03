# Stage 4 -- LOAD into a relational database: design, create, populate, and
# all four CRUD operations, run in sqlite3.  The SQL below is standard and
# runs unchanged on MySQL; only the connect call differs.
import sqlite3

# Step 1: Connect, with the foreign keys switched on
con = sqlite3.connect(":memory:")
con.execute("PRAGMA foreign_keys = ON")      # sqlite needs this asked for
cur = con.cursor()

# Step 2: The schema, normalised
cur.executescript("""
CREATE TABLE city (
  city_id   INTEGER PRIMARY KEY,
  name      TEXT NOT NULL UNIQUE
);
CREATE TABLE customer (
  cust_id   INTEGER PRIMARY KEY,
  name      TEXT    NOT NULL,
  city_id   INTEGER NOT NULL REFERENCES city(city_id),
  income    INTEGER NOT NULL CHECK (income >= 0)
);
CREATE TABLE ordr (
  order_id  INTEGER PRIMARY KEY,
  cust_id   INTEGER NOT NULL REFERENCES customer(cust_id),
  amount    REAL    NOT NULL CHECK (amount > 0),
  placed    TEXT    NOT NULL
);
CREATE INDEX ix_order_cust ON ordr(cust_id);
""")
print("tables:", [r[0] for r in cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")])

# Step 3: CREATE: parameterised inserts
cities = [(1, "Vizag"), (2, "Kochi"), (3, "Kolkata"), (4, "Madurai")]
customers = [(1, "Asha Rao", 1, 40), (2, "Biju Menon", 2, 57),
             (3, "Chitra Das", 3, 37), (4, "Devan Iyer", 4, 69)]
orders = [(101, 1, 1240.50, "2026-01-14"), (102, 2, 99.00, "2026-01-14"),
          (103, 3, 15750.75, "2026-01-15"), (104, 4, 310.25, "2026-01-15"),
          (105, 1, 480.00, "2026-01-16"), (106, 1, 75.25, "2026-01-17")]
cur.executemany("INSERT INTO city VALUES (?, ?)", cities)
cur.executemany("INSERT INTO customer VALUES (?, ?, ?, ?)", customers)
cur.executemany("INSERT INTO ordr VALUES (?, ?, ?, ?)", orders)
con.commit()
print("inserted:", cur.execute("SELECT COUNT(*) FROM customer").fetchone()[0],
      "customers,", cur.execute("SELECT COUNT(*) FROM ordr").fetchone()[0], "orders")

# Step 4: The constraints do their job
for sql, params, why in (
        ("INSERT INTO customer VALUES (?, ?, ?, ?)", (5, "Esha Khan", 9, 36),
         "city_id 9 does not exist"),
        ("INSERT INTO ordr VALUES (?, ?, ?, ?)", (107, 1, -5.0, "2026-01-18"),
         "amount must be positive"),
        ("INSERT INTO city VALUES (?, ?)", (5, "Vizag"), "city name is UNIQUE")):
    try:
        cur.execute(sql, params)
        print("  NOT REJECTED --", why)
    except sqlite3.IntegrityError as e:
        print(f"  rejected ({why}): {type(e).__name__}")

# Step 5: READ: a three-table join with an aggregate
print()
print("orders per customer, with the city:")
q = """
SELECT c.name AS customer, ci.name AS city,
       COUNT(o.order_id) AS n_orders,
       ROUND(SUM(o.amount), 2) AS total
FROM customer c
JOIN city ci ON ci.city_id = c.city_id
LEFT JOIN ordr o ON o.cust_id = c.cust_id
GROUP BY c.cust_id
HAVING COUNT(o.order_id) > 0
ORDER BY total DESC
"""
for row in cur.execute(q):
    print(f"  {row[0]:12s} {row[1]:9s} {row[2]:2d} order(s)  total {row[3]:9.2f}")

# Step 6: UPDATE and DELETE, both with a WHERE
print()
cur.execute("UPDATE customer SET income = income + 5 WHERE city_id = 1")
print("UPDATE touched", cur.rowcount, "row(s); Asha's income is now",
      cur.execute("SELECT income FROM customer WHERE cust_id = 1").fetchone()[0])
cur.execute("DELETE FROM ordr WHERE amount < 100")
print("DELETE removed", cur.rowcount, "row(s);",
      cur.execute("SELECT COUNT(*) FROM ordr").fetchone()[0], "orders remain")
con.commit()

# Step 7: The transaction that is rolled back
print()
try:
    cur.execute("BEGIN")
    cur.execute("UPDATE customer SET income = 0")
    raise RuntimeError("something failed half way through")
except RuntimeError as e:
    con.rollback()
    print("rolled back after:", e)
print("incomes after the rollback:",
      [r[0] for r in cur.execute("SELECT income FROM customer ORDER BY cust_id")])
con.close()
