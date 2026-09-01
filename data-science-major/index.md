---
layout: note
title: "B.Sc. (Hons) Data Science — Major"
section: "Data Science Major"
---

# B.Sc. (Hons) Data Science — Major

Study material for the **APSCHE Model Syllabus for 4-Year UG Honours in B.Sc.
(Data Science) as Major**, effective AY 2025-26, prepared by Adikavi Nannaya
University.

This repository contains a **review** of the official syllabus and **study
material** built from it — unit notes, worked examples, practice problems with
solutions, and every lab program as runnable code.

---

## ⚠ Two topics are examined but missing from the syllabus

Read these before you start revising, because studying the unit lists alone
will leave you unprepared for both.

### 1. Bayes' theorem — Course 4, Statistics

Unit 1 lists only "conditional probability". Bayes appears in the prescribed
activities quiz and in lab experiment 2, but in **no unit**.

→ Covered in [Course 4 Unit 1](notes/sem-2/course-4-statistical-foundations/unit-1.html#16-bayes-theorem--examined-but-not-in-the-syllabus)

### 2. Database triggers — Course 5, DBMS

Unit 5 lists control structures, procedures and functions — **no triggers**.
Yet Course Objective 5 names them, the activities require them, and **two of the
six PL/SQL lab questions are trigger problems**.

→ Covered in [Course 5 Unit 5](notes/sem-3/course-5-dbms/unit-5.html#58-triggers--off-syllabus-but-examined)

Nine further findings are in [`SYLLABUS-REVIEW.md`](SYLLABUS-REVIEW.html).

---

## Start here

| Document | What it is |
|---|---|
| [`SYLLABUS-MAP.md`](SYLLABUS-MAP.html) | The full Sem I–VI structure, elective tracks, and unit-level topics |
| [`SYLLABUS-REVIEW.md`](SYLLABUS-REVIEW.html) | 11 findings from checking the official document |
| [`STUDY-PLAN.md`](STUDY-PLAN.html) | Week-by-week schedule, revision cycles, progress checklist |

## Course notes

| Sem | Course | Notes |
|:---:|---|---|
| I | 1 — Computer Fundamentals and Office Automation | [notes](notes/sem-1/course-1-computer-fundamentals/) |
| I | 2 — Problem Solving Using C | [notes](notes/sem-1/course-2-problem-solving-c/) |
| II | 3 — Python Programming and Data Structures | [notes](notes/sem-2/course-3-python-data-structures/) |
| II | 4 — Statistical Foundations for Data Science | [notes](notes/sem-2/course-4-statistical-foundations/) |
| III | 5 — Database Management Systems | [notes](notes/sem-3/course-5-dbms/) |

Each course folder holds a `README.md`, five unit notes, a `practice.md` with
worked solutions, and a `lab.md`. Course 4 also has a
[formula sheet](notes/sem-2/course-4-statistical-foundations/formula-sheet.html).

## Lab code

| Course | Contents | Status |
|---|---|---|
| [C](labs/course-2-c/) | 15 programs | Compiled `-Wall -Wextra`, no warnings, run |
| [Python](labs/course-3-python/) | 18 programs | 16 run; 2 Tkinter syntax-checked only |
| [Statistics](labs/course-4-stats/) | 15 Excel walkthroughs + Python equivalents | Python run; `statlib` checked against tables |
| [SQL](labs/course-5-dbms/) | 3 experiments + PL/SQL | SQL executed; PL/SQL desk-checked only |

---

## Scope

The source document ([`docs/Data-Science-Major-Sem1-2.pdf`](docs/Data-Science-Major-Sem1-2.pdf),
37 pages) contains the **full programme structure for Semesters I–VI** but
detailed syllabi for only **five courses** — the two in Semester I, the two in
Semester II, and Database Management Systems from Semester III.

Courses 6–15 appear as titles and credits only. Supply the Semester III–VI
document and they can be added the same way.

**Credits verified:** every course is 3 credits theory + 1 credit lab. Semester
totals are 8, 8, 12, 12, 12, 8 — a **60-credit major**.

---

## Verifying everything

Nothing here is asserted without being checked.

```bash
bash tools/verify_all.sh          # every suite
python3 tools/check_coverage.py   # every syllabus topic has notes
```

| Suite | What it proves |
|---|---|
| `run_c_labs.sh` | 15 C programs compile warning-free and produce correct output |
| `run_python_labs.sh` | 20 Python files run; 2 Tkinter files syntax-check |
| `run_stats_labs.sh` | `statlib` matches 23 published table values; 5 experiment scripts run |
| `run_sql_labs.py` | 118 SQL statements execute; 9 constraints correctly reject bad data |
| `extract_syllabus.py` | All 37 PDF pages yield text |
| `check_coverage.py` | 329 syllabus topics all map to a notes section |

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

The official PDF is published at
`apsche.ap.gov.in/Pdf/major_minor1/Data%20Science%20Major.pdf`.

It has defects — truncated sentences, broken question numbering, and the two
missing-but-examined topics above. Where the notes reconstruct something, it is
**marked as a reconstruction** so you can tell it from the official text.
Always check against your own copy and your department's guidance.
