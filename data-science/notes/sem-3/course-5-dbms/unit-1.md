# Unit 1 — Overview of Database Management Systems

**Syllabus topics:** Introduction to data, information, database, database
management systems, file-based system, drawbacks of file-based system, database
approach, classification of database management systems, advantages of database
approach, various data models, components of database management system,
three-schema architecture of database, costs and risks of the database
approach.

---

## 1.1 Data, information and database

| Term | Meaning |
|---|---|
| **Data** | Raw, unprocessed facts — `24001`, `Ananya`, `85` |
| **Information** | Data processed into something meaningful — "Ananya scored 85" |
| **Knowledge** | Information plus context and experience — "85 is a first class" |
| **Database** | An organised, shared collection of logically related data |
| **DBMS** | Software for defining, creating, querying and administering a database |

Data becomes information when it is given structure and context. That
distinction is a reliable two-mark question.

## 1.2 The file-based system and why it failed

Before databases, each application kept its own files.

```
Sales department    →  sales_customers.dat
Accounts department →  accounts_customers.dat
Despatch department →  despatch_customers.dat
```

Three copies of the same customer, maintained by three programs that know
nothing about each other.

### Drawbacks of the file-based approach — a guaranteed exam question

1. **Data redundancy** — the same data stored in several places
2. **Data inconsistency** — a customer changes address; only one file is
   updated, and now the copies disagree
3. **Difficulty accessing data** — every new question needs a new program
   written
4. **Data isolation** — data scattered across files in different formats
5. **Integrity problems** — constraints are buried in program code, not
   declared once
6. **Atomicity problems** — a transfer that debits one account and crashes
   before crediting the other leaves money destroyed
7. **Concurrent access anomalies** — two users updating the same record
   simultaneously corrupt it
8. **Security problems** — no fine-grained control over who sees what
9. **Program–data dependence** — change a file's structure and every program
   reading it must be rewritten

### The database approach

A single shared repository, managed by a DBMS, with the data described **once**
in a central catalogue.

### Advantages

1. **Controlled redundancy** — data stored once
2. **Consistency** — one copy means no disagreement
3. **Data sharing** — many users and applications, one database
4. **Integrity enforcement** — constraints declared in the schema, applied
   everywhere
5. **Security** — access control per user, per table, per column
6. **Backup and recovery** — built into the DBMS
7. **Concurrency control** — the DBMS serialises conflicting operations
8. **Program–data independence** — programs are insulated from storage details
9. **Standards enforcement** — one definition of what a "customer" is

### Costs and risks — the part students forget

The syllabus lists these explicitly, so know them:

1. **New specialised personnel** — you need a DBA
2. **Installation and management cost** — licences, hardware, training
3. **Conversion cost** — migrating from legacy systems
4. **Need for explicit backup and recovery** procedures
5. **Organisational conflict** — departments must agree on shared definitions
6. **A single point of failure** — everything now depends on one system
7. **Overhead** — a DBMS is slower than a raw file for very simple tasks

## 1.3 Classification of DBMS

**By data model:** hierarchical, network, relational, object-oriented,
object-relational, NoSQL

**By number of users:** single-user, multi-user

**By number of sites:** centralised, distributed, parallel

**By cost:** open source (PostgreSQL, MySQL, SQLite), commercial (Oracle, SQL
Server, DB2)

**By architecture:**

| Tier | Structure |
|---|---|
| **1-tier** | Database and application on the same machine — a local SQLite file |
| **2-tier** | Client application talks directly to the database server |
| **3-tier** | Client → application server → database server |

3-tier is the standard for web applications: the browser never touches the
database, which is better for both security and scalability.

## 1.4 Data models

A data model is a set of concepts for describing data, relationships, semantics
and constraints.

| Model | Structure | Example |
|---|---|---|
| **Hierarchical** | Tree; each child has one parent | IBM IMS |
| **Network** | Graph; a child may have several parents | IDMS |
| **Relational** | Tables of rows and columns | Oracle, MySQL, PostgreSQL |
| **Object-oriented** | Objects with attributes and methods | ObjectStore |
| **Object-relational** | Tables plus object features | Oracle, PostgreSQL |
| **Document (NoSQL)** | JSON-like documents | MongoDB |

The **relational model**, proposed by **E. F. Codd in 1970**, dominates because
it is founded on set theory, is declarative (you say *what* you want, not
*how*), and supports a standard query language.

*(You meet the document model again in Semester IV, Course 10.)*

### Categories by level of abstraction

- **High-level / conceptual** — ER model; close to how users think
- **Representational / implementation** — relational; close to how it is stored
- **Low-level / physical** — how bytes sit on disk

## 1.5 Components of a DBMS

| Component | Role |
|---|---|
| **DDL compiler** | Processes schema definitions, stores them in the catalogue |
| **DML compiler / query parser** | Parses and validates queries |
| **Query optimiser** | Chooses the cheapest execution plan |
| **Query evaluation engine** | Executes the plan |
| **Storage manager** | Manages files, buffers and indexes |
| **Transaction manager** | Ensures ACID properties |
| **Buffer manager** | Moves pages between disk and memory |
| **Authorisation manager** | Enforces access control |
| **Data dictionary / catalogue** | Metadata — the schema, describing the data |

### People involved

| Role | Responsibility |
|---|---|
| **Database Administrator (DBA)** | Schema, security, backup, tuning |
| **Database designer** | Identifies data and designs the schema |
| **Application programmer** | Writes programs that use the database |
| **End user** | Naive (uses forms), sophisticated (writes queries) |

## 1.6 The three-schema architecture

Proposed by ANSI/SPARC in 1975 — **the most examined topic in this unit**.

```
        ┌─────────────────────────────────────┐
        │   EXTERNAL LEVEL (many views)       │   what each user sees
        │   View 1     View 2     View 3      │
        └─────────────────────────────────────┘
                         ↕   logical data independence
        ┌─────────────────────────────────────┐
        │   CONCEPTUAL LEVEL (one schema)     │   the whole database,
        │   entities, relationships,          │   logically
        │   constraints                       │
        └─────────────────────────────────────┘
                         ↕   physical data independence
        ┌─────────────────────────────────────┐
        │   INTERNAL LEVEL (one schema)       │   how it is actually stored:
        │   file organisation, indexes,       │   files, indexes, pages
        │   storage structures                │
        └─────────────────────────────────────┘
```

| Level | Also called | Describes | How many |
|---|---|---|---|
| **External** | View level | What a particular user or application sees | Many |
| **Conceptual** | Logical level | The whole database, logically | One |
| **Internal** | Physical level | How data is physically stored | One |

### Data independence — the whole point of the architecture

> **Physical data independence:** you can change the internal schema (add an
> index, reorganise files) **without** changing the conceptual schema.
>
> **Logical data independence:** you can change the conceptual schema (add a
> column, split a table) **without** changing the external schemas or the
> applications.

**Physical independence is easier to achieve than logical independence**, and
exams like this observation. Adding an index genuinely affects nobody; adding a
column may require views to be redefined.

**Mappings** connect the levels: external/conceptual and conceptual/internal.
When one level changes, only the mapping needs updating — not everything above
it.

## 1.7 Database languages

| Language | Purpose | Commands |
|---|---|---|
| **DDL** — Data Definition | Define structure | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` |
| **DML** — Data Manipulation | Manipulate data | `INSERT`, `UPDATE`, `DELETE` |
| **DQL** — Data Query | Retrieve data | `SELECT` |
| **DCL** — Data Control | Permissions | `GRANT`, `REVOKE` |
| **TCL** — Transaction Control | Transactions | `COMMIT`, `ROLLBACK`, `SAVEPOINT` |

Some texts fold DQL into DML. If asked, mention both conventions.

## 1.8 Transactions and ACID

A **transaction** is a logical unit of work — all of it happens, or none of it
does.

| Property | Meaning |
|---|---|
| **A**tomicity | All operations complete, or none do |
| **C**onsistency | The database moves from one valid state to another |
| **I**solation | Concurrent transactions do not interfere |
| **D**urability | Once committed, changes survive a crash |

The classic example: transferring ₹1000 between accounts is a debit *and* a
credit. Atomicity guarantees that a crash between the two cannot destroy the
money.

---

## Exam questions from this unit

**Two marks**

1. Distinguish data from information.
2. What is a data dictionary?
3. State any four drawbacks of the file-based system.
4. Define physical and logical data independence.
5. Expand ACID.

**Five marks**

1. Explain the drawbacks of the file-based system and how the database approach
   addresses them.
2. Explain the advantages **and the costs and risks** of the database approach.
3. Explain the components of a DBMS.
4. Explain the classification of DBMS by architecture (1-, 2- and 3-tier).

**Ten marks**

1. Explain the three-schema architecture with a diagram, and explain data
   independence.
2. Explain the various data models with their structures, advantages and
   examples.

## Mistakes that cost marks

- Listing only the advantages when the question asks for costs and risks too
- Confusing the conceptual level (one, logical) with the external level (many,
  per-user)
- Saying the relational model was invented by Oracle — it was **E. F. Codd**,
  1970
- Reversing physical and logical data independence
- Forgetting that a database is the *data* and a DBMS is the *software*
