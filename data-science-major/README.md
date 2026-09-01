# B.Sc. (Hons) Data Science — Major

Study material for the **Model Syllabus for 4-Year UG Honours in B.Sc.
(Data Science) as Major**, effective AY 2025-26, prepared by Adikavi Nannaya
University.

This repository contains a **review** of the official syllabus and **study
material** built from it — unit notes, worked examples, practice problems with
solutions, and every lab program as runnable code.

---

## ⚠ Four topics are examined but missing from the syllabus

Read these before you start revising, because studying the unit lists alone
will leave you unprepared for all four.

### 1. Bayes' theorem — Course 4, Statistics

Unit 1 lists only "conditional probability". Bayes appears in the prescribed
activities quiz and in lab experiment 2, but in **no unit**.

→ Covered in Course 4 Unit 1

### 2. Database triggers — Course 5, DBMS

Unit 5 lists control structures, procedures and functions — **no triggers**.
Yet Course Objective 5 names them, the activities require them, and **two of the
six PL/SQL lab questions are trigger problems**.

→ Covered in Course 5 Unit 5

### 3 and 4. GridFS and transactions — Course 10, Document Oriented Database

Unit 5's topic list ends at "Replica sets, failover, consistency" — **neither
GridFS nor transactions appears in it, or in any other unit**. Yet Course
Outcome 4 names both, and **lab experiments 18 and 19 are exactly those two
problems**. The course objective that would have introduced them is itself
truncated to the fragment "4. replication, and transactions." (finding
**D13**), which is probably how they went missing.

→ Covered in Course 10 Unit 5, and in lab experiments 18 and 19

**Thirty further findings** are in [`SYLLABUS-REVIEW.md`](SYLLABUS-REVIEW.md),
including damaged bibliographies in all five Semester III–IV courses, a
Semester V objective that stops mid-sentence, and a course with three
objectives against four outcomes against five units.

**And a pattern worth naming:** **ten of the thirty-three findings are the same
defect** — text lost or inserted at a word or sentence boundary, **fourteen
instances in all**, across every one of the four documents: D3 (three
instances), D13, D14, D17, D23, D24 (two), D25, D26, D28 (two) and D29. That is
a production problem, not a scattering of typos.

---

**Published site:** https://nrstatlab.github.io/Data-Science-Major-2025/

## Start here

| Document | What it is |
|---|---|
| [`SYLLABUS-MAP.md`](SYLLABUS-MAP.md) | The full Sem I–VI structure, elective tracks, and unit-level topics |
| [`SYLLABUS-REVIEW.md`](SYLLABUS-REVIEW.md) | **33 findings** from checking the four official documents |
| [`STUDY-PLAN.md`](STUDY-PLAN.md) | Week-by-week schedules for **Semesters I–VI**, the track decision, revision cycles, progress checklist |

## Course notes

| Sem | Course | Notes |
|:---:|---|---|
| I | 1 — Computer Fundamentals and Office Automation | notes |
| I | 2 — Problem Solving Using C | notes |
| II | 3 — Python Programming and Data Structures | notes |
| II | 4 — Statistical Foundations for Data Science | notes |
| III | 5 — Database Management Systems | notes |
| III | 6 — Data Science with R | notes |
| III | 7 — Web Technologies | notes |
| IV | 8 — Data Mining | notes |
| IV | 9 — Python for Data Analysis and Visualization | notes |
| IV | 10 — Document Oriented Database | notes |
| V | 11 — Business Intelligence Tools *(core)* | notes |
| V | 12 A — Machine Learning *(Track A)* | notes |
| V | 13 A — Artificial Intelligence *(Track A)* | notes |
| V | 12 B — Big Data Technologies *(Track B)* | notes |
| V | 13 B — Cloud Computing for Data Science *(Track B)* | notes |
| VI | 14 A — Neural Networks and Deep Learning *(Track A)* | notes |
| VI | 15 A — Natural Language Processing *(Track A)* | notes |
| VI | 14 B — Time Series Analysis and Forecasting *(Track B)* | notes |
| VI | 15 B — Data Engineering and MLOps *(Track B)* | notes |

Each course folder holds a `README.md`, five unit notes, a `practice.md` with
worked solutions, and a `lab.md`. Course 4 also has a
formula sheet.

## Lab code

| Course | Contents | Status |
|---|---|---|
| 1 — Office | 14 experiments + 2 unit checks | 8 spreadsheet computations run and asserted, plus every number-system conversion and text-function result in the notes; 6 experiments produce documents, with nothing to compute |
| 2 — C | 15 programs | Compiled `-Wall -Wextra`, no warnings, run |
| 3 — Python | 18 experiments, 22 files | 20 files run; the 2 Tkinter programs syntax-checked only |
| 4 — Statistics | 15 Excel walkthroughs + Python equivalents | Python run; `statlib` checked against tables |
| 5 — SQL | 3 experiments + PL/SQL | SQL executed; PL/SQL desk-checked only |
| 6 — R | 18 R scripts + 14 Python equivalents | R structurally checked (uninstallable here); equivalents run |
| 7 — Web | 16 experiments, HTML/CSS/JS | Run under jsdom, **184 assertions** on the resulting DOM |
| 8 — Data Mining | 15 experiments | WEKA click-paths documented; scikit-learn/mlxtend equivalents run |
| 9 — Pandas | 18 practicals | **All run**, outputs asserted |
| 10 — MongoDB | 20 experiments | 16 executed through mongomock; 4 have no runnable half — installation, replication, GridFS, transactions. All 20 `mongosh` scripts say **NOT EXECUTED** |
| 11 — BI | 15 experiments | Every DAX, Power Query and LOD figure computed; tool click-paths **NOT EXECUTED** |
| 12 A — ML | 12 practicals | **All run** under scikit-learn. Nothing in this course is marked NOT EXECUTED |
| 13 A — AI | 19 experiments | 16 Prolog programs **NOT EXECUTED**; 7 Python halves run, **five as real logic programs** |
| 12 B — Big Data | 17 experiments | 14 run, including **real Apache Spark, Avro and Parquet**; 15 tool files **NOT EXECUTED** |
| 13 B — Cloud | 15 experiments | 7 run, including a **real web server, a real ETL and a real REST endpoint**; 14 console files **NOT EXECUTED** |
| 14 A — Deep Learning | 12 experiments | **10 run against real MNIST, Fashion-MNIST, IMDb and real MobileNetV2/VGG16 ImageNet weights**; 2 **NOT EXECUTED** |
| 14 B — Time Series | 13 experiments | **All 13 run.** No file in this course is marked NOT EXECUTED |
| 15 A — NLP | 14 experiments | **11 run against real NLTK corpora and real spaCy models**, every result scored against hand-labelled truth; 3 **NOT EXECUTED** |
| 15 B — MLOps | 16 experiments | **11 run against real MLflow, git, DVC and Flask**; 5 **NOT EXECUTED** |

---

## Scope

**Four** source documents, all extracted verbatim. The extracted text is
committed under `docs/` and is what every claim here is checked against:

| Source document | Covers | Extracted to |
|---|---|---|
| Semester I–II syllabus | Programme structure for Semesters I–VI, plus full syllabi for Courses 1–5 | `syllabus-extracted.md` |
| Semester III–IV syllabus | Full syllabi for Courses 6–10 | `syllabus-extracted-sem3-4.md` |
| Semester V syllabus | Full syllabi for Course 11 and **both** Semester V elective pairs — 12 A/B and 13 A/B | `syllabus-extracted-sem5.md` |
| Semester VI syllabus | Full syllabi for **both** Semester VI elective pairs — 14 A/B and 15 A/B | `syllabus-extracted-sem6.md` |

Together they give **all 15 major courses at unit level**, across four source
documents. Nothing in the programme is now a title and nothing else.

**Semester V is a fork.** Course 11 is compulsory; you then take either
**12 A + 13 A** (Machine Learning → Artificial Intelligence) or **12 B + 13 B**
(Big Data → Cloud Computing), and that choice binds you for Semester VI as
well — **14 A + 15 A** (Deep Learning → NLP) or **14 B + 15 B** (Time Series →
Data Engineering & MLOps). **Both tracks are covered here in full**, because
you cannot choose well without seeing what is in each.

---

## Verifying everything

Nothing here is asserted without being checked.

```bash
bash tools/verify_all.sh          # every suite
python3 tools/check_coverage.py   # every syllabus topic has notes
```

| Suite | What it proves |
|---|---|
| `run_office_labs.py` | Course 1's 8 computable experiments, plus every number-system conversion and text-function result the notes quote |
| `run_c_labs.sh` | 15 C programs compile warning-free and produce correct output |
| `run_python_labs.sh` | 20 Python files run; 2 Tkinter files syntax-check |
| `run_stats_labs.sh` | `statlib` matches 23 published table values; 5 experiment scripts run |
| `run_sql_labs.py` | 118 SQL statements execute; 9 constraints correctly reject bad data |
| `run_r_equivalents.py` | 14 Python equivalents run; 18 R scripts structurally checked |
| `run_web_labs.js` | 184 assertions on the DOM after each Course 7 lab script, under jsdom |
| `run_data_labs.py` | 33 Course 8 and 9 programs run, each asserting the notes' own figures |
| `run_mongo_labs.py` | 16 Course 10 experiments executed through mongomock; the other 4 audited for their NOT EXECUTED marker |
| `run_ml_labs.py` | Course 12 A's 12 practicals run under scikit-learn |
| `run_ai_labs.py` | Course 13 A's search and logic programs; 5 run as real Prolog |
| `run_bigdata_labs.py` | 14 of 17 Course 12 B experiments, including real Spark, Avro and Parquet |
| `run_cloud_labs.py` | Course 13 B's runnable halves, and 14 NOT EXECUTED markers audited |
| `run_deeplearning_labs.py` | Course 14 A on **real MNIST, Fashion-MNIST, IMDb and real ImageNet weights**; 2 markers audited |
| `run_timeseries_labs.py` | **All 13** Course 14 B experiments; no NOT EXECUTED file exists |
| `run_nlp_labs.py` | Course 15 A on **real NLTK corpora and real spaCy models**, every result scored; 3 markers audited |
| `run_mlops_labs.py` | Course 15 B against **real MLflow, git, DVC and Flask**; 5 markers audited |
| `check_datasets.py` | **117 checks over 50 practice datasets** — the regression slope, the AR(2) coefficients, the cluster centres, the Granger direction and the drift score are all recovered from the CSV on disk, and the 266-question answer key is rebuilt and compared |
| `extract_syllabus.py` | Every page of every source document yields text |
| `check_coverage.py` | **1,273 syllabus topics across 95 unit files** all map to a notes section |
| `audit_content.py` | The documents' own **stated counts match the files on disk**; every course has its full note set; no malformed table; every link resolves |

Statistical results are additionally self-checked: regression output via
**R² = r²** and **t² = F**, and every critical value in the formula sheet
against `statlib`. Number-system conversions are verified by round-trip.

### What is *not* verified, and why

Honest limits, stated rather than hidden:

- **Tkinter programs** — `tkinter` is not installed in the verification
  environment and a GUI needs a display. Syntax-checked only; say so.
- **PL/SQL** — Oracle-specific. SQLite cannot run it and no Oracle instance was
  available. Written to Oracle syntax and reviewed by hand; run it on your
  college's installation before relying on it.
- **Excel walkthroughs** — not executable. The Python equivalents of the same 15
  experiments were run.
- **R, WEKA and `mongod`** — none can be installed here: the Debian
  repositories that host them are blocked by this environment's egress policy.
  Course 6 ships the `.R` script beside an executed Python equivalent, and
  Course 10 the `mongosh` script beside a mongomock one; both native files
  declare in their first lines that they were not run. WEKA has no script to
  ship, so Course 8 documents the **click-path** in its lab notes instead and
  runs a scikit-learn equivalent.
- **Four Course 10 experiments have no runnable equivalent** — replication
  (17), GridFS (18) and transactions (19) need a running server and mongomock
  is a library; experiment 1 is installing the server, which has no query
  logic to run. `tools/run_mongo_labs.py` names those four with a reason and
  fails if a fifth quietly joins them. **All twenty `mongosh` scripts** carry
  the NOT EXECUTED marker, not just those four, because none of them ran.

---

## Repository layout

```
docs/                    the source PDF and its extracted text
notes/sem-N/course-N-*/  README, unit-1..5, practice, lab
labs/course-N-*/         runnable programs
tools/                   extraction and verification scripts
SYLLABUS-MAP.md          structure and topics
SYLLABUS-REVIEW.md       the findings
STUDY-PLAN.md            the schedule
```

## Rebuilding the website

The site is generated from these Markdown notes into the same house style as
[nrstatlab/Statistics-Major](https://github.com/nrstatlab/Statistics-Major) —
`css/styles.css` is adopted from that repository unchanged, so the two sites
read as one family.

```bash
pip install -r tools/requirements.txt
python3 tools/build_site.py
```

## Practice data

`data/` holds **50 CSV files**, at least one per course, covering the methods
the programme teaches — descriptive statistics and every hypothesis test,
regression, Apriori, decision trees, k-Means and DBSCAN, SQL joins and
normalisation, document modelling, a star schema, MapReduce, search and CSP,
IAM evaluation, ARIMA, SARIMA and VAR, sentiment and NER, and drift detection.

**Every file was generated from a known truth** — the regression file from a
slope of 6.0, the AR(2) series from φ = (0.6, −0.3), the three clusters from
centres the generator chose — so a student can *score* an answer rather than
merely produce one. `data/README.md` says what each file was built from, and
`tools/check_datasets.py` recovers every one of those truths from the CSV
itself.

`data/PRACTICE-QUESTIONS.md` sets **266 questions** across those files, graded
warm-up → core → stretch, with an answer key that is **computed from the CSV
when the page is generated** rather than written from memory. Three figures I
did write from memory while building the datasets turned out wrong, which is
why none of the 266 is typed by hand.

```bash
python3 tools/make_datasets.py     # regenerate; deterministic, seeded
python3 tools/make_questions.py    # rebuild the answer key from the data
python3 tools/check_datasets.py    # 117 checks over 50 datasets
```

Markdown stays the source of truth: edit `notes/**/*.md`, re-run the build, and
commit both. `.nojekyll` is present, so Pages serves the generated HTML verbatim
rather than running Jekyll over it.

## Regenerating the extracted syllabus

```bash
python3 tools/extract_syllabus.py docs/Data-Science-Major-Sem1-2.pdf \
    > docs/syllabus-extracted.md
```

The extractor uses only the Python standard library, since neither `pdftotext`
nor `pypdf` was available. Note that two pages reference their content as an
*indirect array* of streams rather than a stream directly; a naive extractor
returns those pages blank and silently drops DBMS Units 2–5 and the Python
textbook list. `resolve_contents()` handles both forms.

---

## A note on the source

The official syllabus document has defects — truncated sentences, broken question numbering, and the two
missing-but-examined topics above. Where the notes reconstruct something, it is
**marked as a reconstruction** so you can tell it from the official text.
Always check against your own copy and your department's guidance.
