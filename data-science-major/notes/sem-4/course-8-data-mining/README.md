# Course 8 — Data Mining

**Semester IV**

---

## What this course actually is

Data mining is finding patterns in data that nobody put there deliberately.
A supermarket's till system was built to take payments; the fact that nappies
and beer sell together on Friday evenings is a pattern *hiding in the exhaust*
of that system. Course 8 is the set of algorithms for extracting such patterns
at scale.

It is the most **algorithmic** course in the programme. Where Course 6 taught
you to call `lm()` and Course 9 will teach `df.groupby()`, this course asks
you to trace Apriori by hand, compute an information gain, and run K-Means to
convergence on paper. **That is deliberate, and it is what the exam tests.**
An algorithm you can trace by hand is one you can debug when a library gives
you a wrong answer.

## Where it sits in the degree

| From | You already have | Used here for |
|---|---|---|
| Course 4 | Mean, variance, probability, Bayes | Naïve Bayes, evaluation metrics |
| Course 5 | SQL, schemas, normalisation | Unit 1's star schema — deliberately *de*normalised |
| Course 6 | K-Means, TF-IDF, confusion matrices | Revisited properly, with the arithmetic |
| Course 9 (parallel) | NumPy and Pandas | The lab equivalents are written in them |

Unit 1 is the surprise: it is not mining at all but **data warehousing**, and
it exists because you cannot mine what you cannot assemble. It also directly
contradicts Course 5's normalisation teaching, on purpose — §1.6 explains why.

## Course objectives (verbatim)

1. Provide an understanding of data warehousing concepts, architecture, and
   OLAP operations for effective storage, modeling, and analysis.
2. Develop knowledge of data mining fundamentals, tasks, and preprocessing
   techniques to prepare data for mining.
3. Introduce students to association rule mining algorithms for discovering
   hidden patterns and relationships in large datasets.
4. Enable learners to apply classification techniques (decision trees,
   Bayesian, nearest neighbor, rule-based) for predictive modeling.
5. Equip students with knowledge of clustering paradigms and algorithms
   (partitioning, hierarchical, density-based, categorical) for data grouping
   and pattern discovery.

## Units

| Unit | Topic | Notes | Difficulty | Weeks |
|:---:|---|---|---|:---:|
| 1 | Data Warehousing and OLAP | [unit-1.md](unit-1.md) | Easy | 2 |
| 2 | Data Mining and Preprocessing | [unit-2.md](unit-2.md) | Moderate | 3 |
| 3 | Association Analysis | [unit-3.md](unit-3.md) | **Hard** | 3 |
| 4 | Classification | [unit-4.md](unit-4.md) | **Hard** | 4 |
| 5 | Clustering | [unit-5.md](unit-5.md) | **Hard** | 3 |

Units 3, 4 and 5 are each a set of named algorithms you must be able to
*trace*, not merely describe. Budget accordingly: this is not a course you can
revise in the last week.

## Also here

- [practice.md](practice.md) — exam questions with fully worked numeric solutions
- [lab.md](lab.md) — all 15 experiments
- `labs/course-8-datamining/` — code
- `data/course-8-datamining/` — **practice datasets**, CSV: `cluster-points.csv`, `market-basket.csv`, `warehouse-facts.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.
  Also `sales-transactions.csv`, `flowers.csv` in `data/shared/`, which several courses
  analyse so their answers can be compared.

> **On the lab code.** The syllabus prescribes **WEKA**, which cannot be
> installed here — it needs a host the egress policy blocks. So every
> experiment comes in two halves: the **WEKA click-path** documented step by
> step (panel, filter name, parameters) for the lab exam, and a
> **scikit-learn or mlxtend equivalent that actually runs** and is asserted by
> `tools/run_data_labs.py`.
>
> The WEKA halves are marked "NOT EXECUTED" in their own headers. Nothing here
> implies a test that did not run.

## Textbooks

- **Arun K. Pujari, *Data Mining Techniques*, 3rd ed., Universities Press** —
  this is the one the syllabus follows. The unusual algorithms (Pincer-Search,
  STIRR, CACTUS) are in Pujari and almost nowhere else.
- Han, Kamber & Pei, *Data Mining: Concepts and Techniques*, 3rd ed., Morgan
  Kaufmann — better written, and the standard reference worldwide.

**Reference:** Soman, Diwakar & Ajay, *Insight into Data Mining Theory and
Practice*, PHI; Tan, Steinbach, Karpatne & Kumar, *Introduction to Data
Mining*, 2nd ed.

## How to study this course

1. **Trace every algorithm by hand once.** Apriori on five transactions, ID3
   on fourteen rows, K-Means on eight points. It takes an afternoon each and
   it is the difference between passing and understanding.
2. **Learn the formulas cold** — support, confidence, lift, entropy,
   information gain, Gini, the distance measures. They are short, they are
   examined every year, and the ten-mark questions are arithmetic.
3. **Then run the code.** Once you can trace it, `mlxtend.apriori` stops being
   magic and starts being a faster version of what you did on paper.
4. **Watch the vocabulary.** Supervised versus unsupervised, classification
   versus clustering, KDD versus data mining — these distinctions carry marks
   and students routinely blur them.
