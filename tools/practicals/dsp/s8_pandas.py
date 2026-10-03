# Stage 6b -- Pandas: the frame, hierarchical indexing, missing data,
# merge, group-by, and writing the result out.  The teaching is in Python for
# Data Analysis, Units 2 to 5; this is the pipeline's last stage.
import io
import pandas as pd

pd.set_option("display.width", 100)

# Step 1: The two tables
CUSTOMERS = pd.DataFrame({
    "cust_id": [1, 2, 3, 4, 5],
    "name": ["Asha Rao", "Biju Menon", "Chitra Das", "Devan Iyer", "Esha Khan"],
    "city": ["Vizag", "Kochi", "Kolkata", "Madurai", "Bhopal"],
    "income": [40, 57, 37, 69, None],
})
ORDERS = pd.DataFrame({
    "order_id": [101, 102, 103, 104, 105, 106, 107],
    "cust_id": [1, 2, 3, 4, 1, 1, 9],
    "amount": [1240.50, 99.00, 15750.75, 310.25, 480.00, 75.25, 55.00],
    "month": ["Jan", "Jan", "Jan", "Feb", "Feb", "Feb", "Feb"],
})
print("customers", CUSTOMERS.shape, " orders", ORDERS.shape)

# Step 2: Missing data: find it, then decide -- do not let a default decide
print()
print("missing values per column:\n", CUSTOMERS.isna().sum().to_string())
print("mean income, skipna default True :", CUSTOMERS["income"].mean())
print("mean income, skipna=False        :", CUSTOMERS["income"].mean(skipna=False))
filled = CUSTOMERS.assign(income=CUSTOMERS["income"].fillna(
    CUSTOMERS["income"].median()))
print("median-filled incomes            :", list(filled["income"]))
print("the fill is a DECISION and belongs in the report; pandas skipping NaN")
print("silently is what makes it easy to forget.")

# Step 3: Merge: the how= argument decides which rows survive
print()
for how in ("inner", "left", "outer"):
    m = ORDERS.merge(CUSTOMERS, on="cust_id", how=how)
    print(f"merge how={how:6s} -> {len(m):2d} rows, "
          f"{int(m['name'].isna().sum())} with no customer, "
          f"{int(m['order_id'].isna().sum())} with no order")
print("order 107 points at customer 9, who does not exist; an inner join drops")
print("it without a word.  Count the rows before and after every join.")

# Step 4: Group-by with several aggregates
print()
merged = ORDERS.merge(CUSTOMERS, on="cust_id", how="inner")
g = merged.groupby("name")["amount"].agg(["count", "sum", "mean"]).round(2)
g = g.sort_values("sum", ascending=False)
print(g.to_string())

# Step 5: Hierarchical index: two keys, and the two ways to get back
print()
h = merged.groupby(["month", "city"])["amount"].sum().round(2)
print(h.to_string())
print()
print("h.loc['Feb']:\n", h.loc["Feb"].to_string())
print("h.unstack() turns the inner level into columns:")
print(h.unstack().fillna(0).round(2).to_string())

# Step 6: Write the result out, and read it back
print()
buf = io.StringIO()
g.to_csv(buf)
print("to_csv:")
print(buf.getvalue().strip())
back = pd.read_csv(io.StringIO(buf.getvalue()), index_col=0)
print("round trip identical:", back.equals(g))
print()
print("read_csv guesses dtypes from the first rows; on a column of account")
print("numbers with leading zeros it guesses int and destroys them.  Pass")
print("dtype={'account': str} whenever the digits are an identifier, not a number.")
