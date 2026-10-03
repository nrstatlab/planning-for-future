# NOT EXECUTED -- PyMySQL needs a MySQL server, which these pages are not
# built against.  Every SQL statement here is the one the sqlite3 listing
# above ran; only the connection and the placeholder style differ.
import pymysql

con = pymysql.connect(
    host="localhost", user="student", password="...", database="etl",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,   # rows as dicts, not tuples
    autocommit=False,                         # the default, and the right one
)
try:
    with con.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS customer (
              cust_id INT PRIMARY KEY,
              name    VARCHAR(60) NOT NULL,
              city_id INT NOT NULL,
              income  INT NOT NULL CHECK (income >= 0),
              FOREIGN KEY (city_id) REFERENCES city(city_id)
            ) ENGINE=InnoDB
        """)
        cur.executemany(
            "INSERT INTO customer VALUES (%s, %s, %s, %s)",
            [(1, "Asha Rao", 1, 40), (2, "Biju Menon", 2, 57)])
        cur.execute("SELECT name, income FROM customer WHERE income > %s", (40,))
        for row in cur.fetchall():
            print(row)                        # {'name': 'Biju Menon', 'income': 57}
    con.commit()
except Exception:
    con.rollback()
    raise
finally:
    con.close()

# THREE DIFFERENCES FROM THE sqlite3 LISTING, AND NOTHING ELSE:
#   1. the placeholder is %s, not ?  -- and it is still a PLACEHOLDER, not
#      string formatting.  "... WHERE income > %s" % 40 is a SQL injection,
#      cur.execute(sql, (40,)) is not.
#   2. ENGINE=InnoDB, because MyISAM ignores foreign keys silently.
#   3. autocommit=False and an explicit commit(), so a half-finished load
#      leaves the table as it was.
