# Course 10 — Document Oriented Database (MongoDB)

**Semester IV**

---

## The one thing to understand before anything else

**MongoDB is not a better relational database. It is a different trade.**

Course 5 taught you to normalise: split data across tables, eliminate
redundancy, join at read time, and let the database enforce consistency.
MongoDB inverts almost every one of those decisions — it stores related data
**together** in one document, accepts redundancy, avoids joins, and pushes
consistency decisions to the application.

Neither is correct in general. Each is correct for a different access pattern,
and the whole course is about telling which one you have.

| | Relational (Course 5) | Document (here) |
|---|---|---|
| Unit of storage | A **row**, split across tables | A **document**, whole |
| Schema | Fixed, enforced on write | **Flexible**, optional validation |
| Redundancy | Eliminated by normalisation | **Accepted** for read speed |
| Joins | The core operation | Avoided; `$lookup` exists but is a last resort |
| Scaling | Vertically — a bigger machine | **Horizontally** — more machines |
| Guarantees | ACID across the whole database | ACID per document; transactions since 4.0 |
| Best when | Relationships matter and are queried many ways | You read one whole entity at a time |

## Where it sits in the degree

| From | You have | Used here |
|---|---|---|
| **Course 5** | SQL, keys, normalisation, ACID, transactions | Every unit — as the *contrast*. §1.5 and §3.9 map operation to operation |
| **Course 7** | JSON syntax, nested objects and arrays | A MongoDB document **is** a JSON object; Unit 1's BSON is its typed cousin |
| **Course 9** | `pd.json_normalize` | How you get MongoDB documents into a DataFrame |
| **Course 8** | Aggregation concepts | Unit 4's pipeline is `GROUP BY` with more stages |

**If you learned Course 5 properly, you already know 70% of this course** — you
just have to learn where the answers differ and why.

## Course objectives (verbatim)

1. To introduce students to the concepts of NoSQL databases and their
   significance compared to traditional relational databases.
2. To provide hands-on experience with MongoDB for performing CRUD operations,
   querying, and advanced data handling.
3. To develop skills in schema design, data modeling, and working with embedded
   and referenced documents.
4. replication, and transactions.
5. To prepare students for real-world applications of MongoDB in scalable,
   high-performance data-driven applications.

> **Objective 4 is printed exactly as shown** — the verb is missing, and the
> sentence is incomplete in the source document. From Course Outcome 4 it was
> presumably meant to read "To utilise advanced features such as indexing,
> aggregation, GridFS, replication, and transactions." Recorded as a finding in
> [SYLLABUS-REVIEW.md](../../../SYLLABUS-REVIEW.md).

## Units

| Unit | Topic | Notes | Difficulty | Weeks |
|:---:|---|---|---|:---:|
| 1 | NoSQL and MongoDB fundamentals | [unit-1.md](unit-1.md) | Easy | 2 |
| 2 | Architecture and data modeling | [unit-2.md](unit-2.md) | Easy | 2 |
| 3 | CRUD and querying | [unit-3.md](unit-3.md) | Moderate | 3 |
| 4 | Data modelling and aggregation | [unit-4.md](unit-4.md) | **Hard** | 3 |
| 5 | Query optimization, indexing, replication | [unit-5.md](unit-5.md) | **Hard** | 3 |

Units 1 and 2 overlap considerably — both cover MongoDB's architecture, and
Unit 4 repeats Unit 2's embedded-versus-referenced material almost exactly.
That is the syllabus's structure, not a mistake in these notes; §4.1 says where
the repetition falls so you do not study it twice.

## Also here

- [practice.md](practice.md) — exam questions with worked solutions
- [lab.md](lab.md) — all 20 experiments
- `labs/course-10-mongodb/` — code
- `data/course-10-mongodb/` — **practice datasets**, CSV: `courses.csv`, `students.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.

> **On the lab code.** `mongod` cannot be installed here — the Debian
> repositories are blocked by the egress policy — so each experiment has two
> halves:
>
> - **The `mongosh` script** you would actually run, marked **NOT EXECUTED** in
>   its own header. That is what the lab examiner will ask you to demonstrate.
> - **A Python equivalent that runs**, executing the same query logic through
>   **mongomock** and asserting the results, verified by
>   `tools/run_mongo_labs.py`.
>
> **Sixteen of the twenty experiments have a runnable half.** Experiment 1 is
> installation, with no query logic to run; and mongomock, faithful as it is
> to the query and aggregation language, is not a server, so **replication
> (17), GridFS (18) and transactions (19) genuinely cannot be executed**.
> Those four are documented only. Every one of the twenty `mongosh` scripts
> says NOT EXECUTED regardless, because none of them ran. Nothing here implies
> a test that did not run.

## Textbooks

- Bradshaw, Brazil & Chodorow, *MongoDB: The Definitive Guide*, O'Reilly —
  Chodorow was a MongoDB engineer; this is the reference.
- Chellappan & Ganesan, *MongoDB Recipes*, Apress
- Kyle Banker, *MongoDB in Action*, 2nd ed., Manning, 2016

**Web:** the [official documentation](https://www.mongodb.com/docs/) is
genuinely good and is what practitioners use; **MongoDB University**
(learn.mongodb.com) runs free courses with a real cluster.

## How to study this course

1. **Install it and type the queries.** MongoDB Atlas has a free tier that
   needs no local install, and `mongosh` is the same shell the exam uses.
2. **Translate everything back to SQL.** For every MongoDB operation you learn,
   write the SQL you would have used in Course 5. That single habit makes the
   whole course click, and it is what the ten-mark comparison questions want.
3. **Learn the operators cold** — `$gt`, `$in`, `$and`, `$set`, `$inc`,
   `$match`, `$group`, `$lookup`, `$unwind`. They are short and they are
   examined every year.
4. **Decide embed-or-reference deliberately, every time.** §2.6 gives the rule.
   It is the single most consequential design decision in the course, and the
   most common ten-mark question.
