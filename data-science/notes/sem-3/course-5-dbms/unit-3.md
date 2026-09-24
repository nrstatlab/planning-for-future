# Unit 3 — The Relational Model and Normalization

**Syllabus topics:** Introduction, CODD rules, relational data model,
concept of key, relational integrity, relational algebra, relational algebra
operations, advantages of relational algebra, limitations of relational
algebra, functional dependencies and normal forms.

---

This is the hardest unit in the course, and normalization is the hardest part
of it. It is also the part most reliably asked as a ten-mark question.

## 3.1 The relational data model

Proposed by **E. F. Codd** in 1970. Data is stored in **relations** — tables of
rows and columns.

| Formal term | Common term |
|---|---|
| Relation | Table |
| Tuple | Row / record |
| Attribute | Column / field |
| Domain | Set of allowed values for a column |
| Degree | Number of **attributes** (columns) |
| Cardinality | Number of **tuples** (rows) |
| Relation schema | The table's structure |
| Relation instance | The data in it at a point in time |

**Degree and cardinality are frequently swapped in exams.** Degree counts
columns; cardinality counts rows.

### Properties of a relation

1. Each cell holds **one atomic value** — no lists, no repeating groups
2. Every attribute has a distinct name
3. Values in an attribute come from the same domain
4. **The order of tuples is irrelevant** — a relation is a *set*
5. **The order of attributes is irrelevant**
6. **No duplicate tuples**

Property 4 is why `SELECT` results have no guaranteed order unless you write
`ORDER BY`. A common source of confusion.

## 3.2 Codd's 12 rules

Codd published 12 rules (numbered 0 to 12, so thirteen in all) defining what
makes a DBMS genuinely relational. Know the concept and be able to name several;
few real systems satisfy all of them.

| # | Rule | Meaning |
|:---:|---|---|
| 0 | Foundation | The system must be relational, a database and a management system |
| 1 | Information | All data represented as values in tables |
| 2 | Guaranteed access | Every value reachable by table + primary key + column |
| 3 | Systematic NULL | NULLs supported uniformly for missing data |
| 4 | Active online catalogue | Metadata stored as tables, queryable the same way |
| 5 | Comprehensive sublanguage | One language for definition, manipulation and control |
| 6 | View updating | All theoretically updatable views must be updatable |
| 7 | High-level insert/update/delete | Set-at-a-time, not row-at-a-time |
| 8 | Physical data independence | Storage changes do not affect applications |
| 9 | Logical data independence | Logical changes do not affect applications |
| 10 | Integrity independence | Constraints stored in the catalogue, not in programs |
| 11 | Distribution independence | Distributing the data does not affect applications |
| 12 | Non-subversion | A low-level interface cannot bypass the constraints |

## 3.3 Relational integrity constraints

| Constraint | Rule |
|---|---|
| **Domain integrity** | Every value must belong to the attribute's domain |
| **Entity integrity** | **The primary key can never be NULL** |
| **Referential integrity** | A foreign key must match an existing primary key value, or be NULL |
| **Key constraint** | Primary key values must be unique |

**Entity integrity** exists because a NULL primary key could not identify
anything.

**Referential integrity** is what stops you assigning an employee to department
99 when no such department exists — as demonstrated in
`03_employee.sql`, where that
exact update is tested and correctly rejected.

### Referential actions

What happens when a referenced row is deleted or updated:

| Action | Effect |
|---|---|
| `CASCADE` | Delete/update the dependent rows too |
| `SET NULL` | Set the foreign key to NULL |
| `SET DEFAULT` | Set it to its default value |
| `RESTRICT` / `NO ACTION` | Reject the operation — the default |

## 3.4 Relational algebra

A **procedural** query language: it specifies *how* to compute the result. It is
the theoretical foundation of SQL, and query optimisers work in terms of it.

### Basic operations

| Operation | Symbol | Meaning |
|---|:---:|---|
| **Select** | σ (sigma) | Choose **rows** matching a condition |
| **Project** | π (pi) | Choose **columns** |
| **Union** | ∪ | All tuples in either relation |
| **Set difference** | − | Tuples in the first but not the second |
| **Cartesian product** | × | Every combination of rows |
| **Rename** | ρ (rho) | Rename a relation or attribute |

**Select picks rows, project picks columns.** Swapping them is the most common
error, largely because SQL's `SELECT` keyword actually does the *projection*.

```
σ_{salary > 50000}(EMPLOYEE)          →  SELECT * FROM Employee WHERE salary > 50000
π_{name, salary}(EMPLOYEE)            →  SELECT name, salary FROM Employee
π_{name}(σ_{dept_id = 2}(EMPLOYEE))   →  SELECT name FROM Employee WHERE dept_id = 2
```

### Derived operations

| Operation | Symbol | Meaning |
|---|:---:|---|
| **Intersection** | ∩ | Tuples in both — equals R − (R − S) |
| **Natural join** | ⋈ | Join on all common attributes, removing duplicates |
| **Theta join** | ⋈_θ | Join on an arbitrary condition |
| **Equi join** | ⋈_{=} | Theta join where the condition is equality |
| **Outer joins** | ⟕ ⟖ ⟗ | Left, right, full — keep unmatched rows, padded with NULL |
| **Division** | ÷ | "For all" queries |

**Union compatibility:** ∪, ∩ and − require both relations to have the same
number of attributes with matching domains. Without it the operation is
undefined.

### Advantages of relational algebra

1. **A formal mathematical foundation** for query languages
2. **Enables query optimisation** — algebraic equivalences let the optimiser
   rewrite a query into a cheaper but equivalent form
3. **Closure** — every operation takes relations and returns a relation, so
   operations compose freely
4. **Procedural clarity** — the order of operations is explicit

### Limitations of relational algebra

1. **No aggregate functions** — no `COUNT`, `SUM`, `AVG` in the basic algebra
2. **No grouping**
3. **No sorting** — a relation is a set, so it has no order
4. **No arithmetic or computed columns**
5. **No recursion** — cannot express transitive closure ("all managers above
   this employee")
6. **No update operations** — it is a query language only
7. **No null handling** in the pure theory

**Extended relational algebra** adds aggregation and grouping, which is how SQL
manages `GROUP BY`. Mentioning that distinction earns marks.

## 3.5 Functional dependencies

> **X → Y** ("X determines Y") means: whenever two tuples agree on X, they must
> agree on Y.

`roll_no → name` — the roll number determines the name. Given a roll number,
the name is fixed.

`name → roll_no` is **false** — two students may share a name.

### Types of functional dependency

| Type | Definition | Example |
|---|---|---|
| **Full** | Y depends on the whole of X, not any part | {roll, course} → marks |
| **Partial** | Y depends on only part of a composite X | {roll, course} → student_name |
| **Transitive** | X → Y and Y → Z, so X → Z | roll → dept_id → dept_name |
| **Trivial** | Y is a subset of X | {roll, name} → name |

**Partial dependency is what 2NF removes. Transitive dependency is what 3NF
removes.** Fixing those two definitions in your mind makes normalization
mechanical.

### Armstrong's axioms

| Axiom | Rule |
|---|---|
| **Reflexivity** | If Y ⊆ X then X → Y |
| **Augmentation** | If X → Y then XZ → YZ |
| **Transitivity** | If X → Y and Y → Z then X → Z |

Derived rules: union, decomposition, pseudo-transitivity.

## 3.6 Normalization

### 🎯 Why normalize

Normalization removes redundancy and the **anomalies** that come with it.

Consider this unnormalized table:

| roll | name | course_id | course_name | instructor | inst_phone |
|---|---|---|---|---|---|
| 101 | Ananya | CS01 | Databases | Dr Rao | 9876543210 |
| 101 | Ananya | CS02 | Python | Dr Devi | 9876500000 |
| 102 | Bhavana | CS01 | Databases | Dr Rao | 9876543210 |

Three problems, all examinable:

| Anomaly | Problem |
|---|---|
| **Insertion** | A new course with no students enrolled cannot be recorded — there is no roll number to complete the key |
| **Update** | Dr Rao changes phone number; it must be changed in *every* row, and missing one creates inconsistency |
| **Deletion** | If student 102 withdraws and that was the last CS01 row, the fact that CS01 exists is lost entirely |

Normalization is the systematic removal of these.

### First Normal Form (1NF)

> Every attribute holds a **single atomic value**. No repeating groups, no
> multivalued attributes.

**Violates 1NF:**

| roll | name | phone |
|---|---|---|
| 101 | Ananya | 9876543210, 9123456789 |

**In 1NF:**

| roll | name | phone |
|---|---|---|
| 101 | Ananya | 9876543210 |
| 101 | Ananya | 9123456789 |

Or better, a separate `STUDENT_PHONE` table.

### Second Normal Form (2NF)

> In 1NF, **and** every non-key attribute is **fully** functionally dependent on
> the **whole** primary key — no partial dependencies.

2NF only matters when the primary key is **composite**. A single-attribute
primary key means partial dependency is impossible, so a 1NF table with a simple
key is automatically in 2NF.

**Violates 2NF.** Key is {roll, course_id}:

| roll | course_id | student_name | marks |
|---|---|---|---|

`student_name` depends only on `roll`, which is *part* of the key — a partial
dependency.

**Decomposed into 2NF:**

```
STUDENT(roll PK, student_name)
ENROLMENT(roll FK, course_id FK, marks, PRIMARY KEY(roll, course_id))
```

### Third Normal Form (3NF)

> In 2NF, **and** no non-key attribute transitively depends on the primary key.
> Every non-key attribute depends on the key, the whole key, and nothing but the
> key.

**Violates 3NF:**

| emp_id | emp_name | dept_id | dept_name |
|---|---|---|---|

`emp_id → dept_id → dept_name`, so `dept_name` depends on the key only
transitively.

**Decomposed into 3NF:**

```
EMPLOYEE(emp_id PK, emp_name, dept_id FK)
DEPARTMENT(dept_id PK, dept_name)
```

That is exactly the structure of the Employee lab schema — the lab tables are
already in 3NF, which is why they need no decomposition.

### Boyce-Codd Normal Form (BCNF)

> For every non-trivial dependency X → Y, **X must be a super key**.

BCNF is stricter than 3NF. A table in 3NF may still violate BCNF when it has
**overlapping candidate keys**. The classic example:

| student | subject | teacher |
|---|---|---|

with `{student, subject} → teacher` and `teacher → subject`. The second
dependency has a non-super-key on the left, so it is in 3NF but not BCNF.

### The memory aid

> **"The key, the whole key, and nothing but the key, so help me Codd."**

- **The key** → 1NF (atomic values keyed properly)
- **The whole key** → 2NF (no partial dependency)
- **Nothing but the key** → 3NF (no transitive dependency)

### Higher normal forms, briefly

| Form | Removes |
|---|---|
| **4NF** | Multivalued dependencies |
| **5NF** | Join dependencies |
| **6NF** | Rarely used; temporal databases |

### Denormalization

Normalizing to 3NF means more tables and therefore more joins, which can be
slower. **Denormalization** deliberately reintroduces redundancy for read
performance — common in data warehouses and reporting systems, which you meet
in Semester V's Business Intelligence course.

Normalize first; denormalize only when measurement shows you need to.

---

## Worked example — normalize to 3NF

**Given** this unnormalized table:

| order_id | cust_id | cust_name | cust_city | product_id | product_name | price | qty |
|---|---|---|---|---|---|---|---|

with `{order_id, product_id}` as the primary key.

**Step 1 — 1NF.** All values are already atomic, so the table is in 1NF.

**Step 2 — Identify the functional dependencies.**

- `{order_id, product_id} → qty` — full dependency ✓
- `order_id → cust_id` — **partial** (depends on part of the key)
- `cust_id → cust_name, cust_city` — **transitive**
- `product_id → product_name, price` — **partial**

**Step 3 — 2NF.** Remove the partial dependencies:

```
ORDER(order_id PK, cust_id, cust_name, cust_city)
PRODUCT(product_id PK, product_name, price)
ORDER_ITEM(order_id FK, product_id FK, qty, PRIMARY KEY(order_id, product_id))
```

**Step 4 — 3NF.** `ORDER` still has `order_id → cust_id → cust_name`, a
transitive dependency. Remove it:

```
CUSTOMER(cust_id PK, cust_name, cust_city)
ORDER(order_id PK, cust_id FK)
PRODUCT(product_id PK, product_name, price)
ORDER_ITEM(order_id FK, product_id FK, qty, PRIMARY KEY(order_id, product_id))
```

**Result:** four tables in 3NF. Every anomaly is gone — a customer can exist
without an order, a product without a sale, and a customer's city is stored
exactly once.

---

## Exam questions from this unit

**Two marks**

1. Define degree and cardinality of a relation.
2. State the entity integrity rule.
3. Distinguish `σ` from `π` in relational algebra.
4. What is a partial functional dependency?
5. State two limitations of relational algebra.

**Five marks**

1. Explain the integrity constraints of the relational model.
2. Explain the basic operations of relational algebra with examples.
3. Explain 1NF, 2NF and 3NF with examples.
4. Explain the insertion, update and deletion anomalies with one table.
5. Explain BCNF and how it differs from 3NF.

**Ten marks**

1. Explain Codd's rules.
2. Normalize a given unnormalized table to 3NF, showing every step and the
   dependencies removed.
3. Explain functional dependencies, their types, Armstrong's axioms, and the
   normal forms.

## Mistakes that cost marks

- Swapping degree (columns) and cardinality (rows)
- Confusing select (rows) with project (columns)
- Jumping straight to 3NF without showing 1NF and 2NF — the marks are in the
  **steps**
- Forgetting that 2NF only applies when the key is composite
- Not stating the functional dependencies before decomposing
- Losing information in a decomposition — the join of the pieces must reproduce
  the original
- Claiming every table should be in BCNF; 3NF is often the practical stopping
  point, because BCNF decomposition can lose dependencies
