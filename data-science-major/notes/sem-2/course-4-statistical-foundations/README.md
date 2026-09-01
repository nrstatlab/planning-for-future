# Course 4 — Statistical Foundations for Data Science

**Semester II**

---

## Why this is the most important course in the degree

Strip away the programming and data science *is* statistics. Every model you
meet later — Data Mining in Semester IV, Machine Learning or Time Series in
Year III — is applied statistics with a library wrapped around it.

A model that reports 95% accuracy on a dataset where 95% of cases are one class
has learned nothing. Knowing that is statistics, not programming. This course
is where you learn to tell a real result from a plausible-looking one.

## Two things you must know before you start

**1. Bayes' theorem is examined but is not in the syllabus units.** Unit 1
lists only "conditional probability". Bayes appears in the prescribed
activities quiz and in lab experiment 2 — but never as a unit topic. Study it
anyway; it is covered in [unit-1.md](unit-1.md). See
[`SYLLABUS-REVIEW.md`](../../../SYLLABUS-REVIEW.md) finding **D1**.

**2. The lab never uses Python.** All 15 experiments are Excel/PSPP, even
though you are learning Python in Course 3 the same semester. Do them in Excel
for the exam and again in Python for the skill — both versions are provided.
See finding **D8**.

## Course objectives (verbatim)

1. To introduce the fundamental concepts of probability and statistics for
   quantifying and analyzing uncertainty in real-world problems.
2. To develop an understanding of random variables, expectations, and common
   probability distributions.
3. To build the ability to summarize and describe data using measures of
   central tendency, dispersion, correlation, and visualization.
4. To equip students with statistical tools for modeling relationships using
   correlation and regression analysis.
5. To provide knowledge of estimation and hypothesis testing for making valid
   inferences from sample data about populations.

## Units

| Unit | Topic | Notes | Difficulty | Weeks |
|:---:|---|---|---|:---:|
| 1 | Probability and basic statistics | [unit-1.md](unit-1.md) | Moderate | 3 |
| 2 | Random variables, expectation, variance | [unit-2.md](unit-2.md) | Moderate | 2 |
| 3 | Probability distributions | [unit-3.md](unit-3.md) | **Hard** | 3 |
| 4 | Correlation and regression | [unit-4.md](unit-4.md) | **Hard** | 3 |
| 5 | Inference and hypothesis testing | [unit-5.md](unit-5.md) | **Hard** | 3 |

Units 3, 4 and 5 carry the difficulty. They also carry the marks.

## Also here

- [formula-sheet.md](formula-sheet.md) — every formula in one place, for revision
- [practice.md](practice.md) — problems with full worked solutions
- [lab.md](lab.md) — all 15 experiments
- `labs/course-4-stats/` — Excel walkthroughs
  and runnable Python
- `data/course-4-stats/` — **practice datasets**, CSV: `before-after.csv`, `fertiliser-yield.csv`, `heights.csv`, `preference-survey.csv`, `study-hours-marks.csv`, `treatment-groups.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.

## Textbooks

- Ronald E. Walpole, *Probability and Statistics for Engineers and Scientists*, Wiley
- Sheldon M. Ross, *Introduction to Probability and Statistics for Engineers and Scientists*
- Montgomery & Runger, *Applied Statistics and Probability for Engineers*

**References:** D. C. Agarwal, *Statistics for Data Science and AI* ·
Larry J. Stephens, *Excel Data Analysis*

## How to study statistics

1. **Understand before you memorise.** A formula you understand can be
   reconstructed when you forget it. A formula you memorised is simply gone.
2. **Always ask what the number means.** Computing r = 0.87 earns some marks;
   saying "a strong positive linear relationship, though this does not
   establish causation" earns the rest.
3. **Do the arithmetic by hand at least once** for each technique. Excel hides
   the mechanism, and exams test the mechanism.
4. **Watch the sample-versus-population distinction.** Dividing by n instead of
   n−1 is the most common arithmetic error in this course.
5. **Draw the picture.** A sketched normal curve with the rejection region
   shaded prevents most hypothesis-testing errors.
