# Course 9 — Python for Data Analysis and Visualization

**Semester IV**

---

## Why this is the most important course in the degree

Every other course teaches you *about* data science. This one teaches the tools
you will actually use, every day, in any data job you take.

NumPy and Pandas are not one option among several. They are **the** foundation:
scikit-learn takes NumPy arrays, matplotlib plots them, every deep learning
framework mirrors their API, and essentially every Python data pipeline written
in the last decade passes through a DataFrame. Course 8's `mlxtend` and
`sklearn` labs are Pandas code underneath.

**This is also where finding [D8](../../../SYLLABUS-REVIEW.md) finally closes.**
Course 1 taught spreadsheet analysis and Course 4 taught statistics by hand;
neither connected to the programming in Courses 2 and 3. Course 9 is the join:
everything you computed with a formula in Course 4 becomes one method call
here, and §5.7 recomputes Course 4's worked examples in Pandas to prove the two
agree.

## Where it sits

| From | You have | Used here for |
|---|---|---|
| Course 3 | Python, lists, dicts, comprehensions, files | The language itself; Unit 1 contrasts lists with arrays |
| Course 4 | Mean, variance, correlation, distributions | Unit 1's statistical functions; Unit 5's `groupby` |
| Course 5 | SQL SELECT, WHERE, GROUP BY, JOIN | Unit 5's merge and groupby are the same operations |
| Course 6 | dplyr's five verbs, ggplot2 | The direct R counterpart — §5.8 maps them |
| Course 8 | Preprocessing theory | Unit 3 is that theory, executed |

### The three languages of one idea

The single most useful thing to notice in this course is that **SQL, dplyr and
Pandas express the same operations**:

| Operation | SQL | dplyr (Course 6) | Pandas (here) |
|---|---|---|---|
| Filter rows | `WHERE` | `filter()` | `df[df.x > 5]` |
| Pick columns | `SELECT` | `select()` | `df[["a", "b"]]` |
| New column | `AS` | `mutate()` | `df.assign(...)` |
| Sort | `ORDER BY` | `arrange()` | `df.sort_values()` |
| Aggregate | `GROUP BY` | `group_by() + summarise()` | `df.groupby().agg()` |
| Join | `JOIN` | `left_join()` | `pd.merge()` |

Learn one column and you have learned three.

## Course objectives (verbatim)

1. Introduce foundational concepts of NumPy arrays and array operations for
   efficient numerical computing.
2. Teach key data structures and manipulation techniques using Pandas.
3. Enable students to perform data input/output operations and implement basic
   data cleaning workflows.
4. Explore string processing methods and feature engineering strategies in
   Pandas.
5. Guide learners in advanced data wrangling tasks including merging,
   reshaping, hierarchical indexing and visualization.

## Units

| Unit | Topic | Notes | Difficulty | Weeks |
|:---:|---|---|---|:---:|
| 1 | NumPy Essentials | [unit-1.md](unit-1.md) | Moderate | 3 |
| 2 | Pandas Basics and Data Structures | [unit-2.md](unit-2.md) | Moderate | 3 |
| 3 | Data Input, Output and Cleaning | [unit-3.md](unit-3.md) | Easy | 2 |
| 4 | String Operations and Feature Engineering | [unit-4.md](unit-4.md) | Moderate | 2 |
| 5 | Wrangling, Reshaping and Visualization | [unit-5.md](unit-5.md) | **Hard** | 4 |

**Unit 5 is overloaded**, and it is worth saying so plainly: merging,
concatenation, pivot/stack/unstack, hierarchical indexing, grouped statistics
**and** three plotting libraries, in one unit. Treat reshaping and
visualization as two separate topics and give each its own week — the same
flag as Course 3 Unit 4 and Course 6 Unit 5.

## Also here

- [practice.md](practice.md) — exam questions with worked solutions
- [lab.md](lab.md) — all 18 practicals
- `labs/course-9-python-da/` — code
- `data/course-9-python-da/` — **practice datasets**, CSV: `messy-customers.csv`, `monthly-sales.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.
  Also `sales-transactions.csv` in `data/shared/`, which several courses
  analyse so their answers can be compared.

> **Everything here runs.** This is the one Semester IV course whose prescribed
> tools install cleanly, so nothing is desk-checked and nothing says "not
> executed". All 18 practicals are executed and asserted by
> `tools/run_data_labs.py`, on
> NumPy 2.4 and Pandas 3.0.

## Textbooks

- **Wes McKinney, *Python for Data Analysis*, 3rd ed., O'Reilly** — McKinney
  wrote Pandas, this course's syllabus follows his book chapter by chapter,
  and **the whole text is free at wesmckinney.com/book**. Read it.
- Anita Goel, *Python Programming — An Object Oriented Approach*, Universities
  Press
- Yuli Vasiliev, *Python for Data Science For Dummies*, 2nd ed., Wiley, 2022

**Reference:** Jake VanderPlas, *Python Data Science Handbook* — also free
online, and the better reference for NumPy specifically.

## How to study this course

1. **Type every example.** Reading Pandas code and writing it are different
   skills, and only one of them is examined in the lab.
2. **Learn to read the error messages.** `SettingWithCopyWarning`,
   `KeyError`, and shape-mismatch errors are the three you will meet
   constantly; §2.9 and §3.3 explain what each actually means.
3. **Think in whole arrays, not loops.** The single biggest shift from Course 3
   is that `for i in range(len(df))` is almost always the wrong answer here.
   §1.5 shows the 50× difference this makes.
4. **Keep the docs open.** `df.<TAB>` in Jupyter and `help(pd.merge)` are how
   professionals work; nobody memorises the parameter lists.
